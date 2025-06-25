#!/usr/bin/env python3
"""
Web Multi-Format Video and Audio Downloader

A web interface for downloading videos and audio from various platforms in different formats.
Uses yt-dlp, a powerful fork of youtube-dl with additional features.
"""

import os
import sys
import json
import uuid
import shutil
import subprocess
import threading
import time
import logging
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, session, g
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SelectField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL, Optional

# Import proxy management module
try:
    from proxies import get_random_proxy, is_youtube_url
    PROXY_SUPPORT = True
except ImportError:
    PROXY_SUPPORT = False
    logging.warning("Proxy module not found. Random proxy feature will be disabled.")

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max upload size
app.config['DOWNLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
csrf = CSRFProtect(app)

# Ensure download directory exists
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# Global variables
active_downloads = {}
completed_downloads = {}

# Check if yt-dlp is installed
def check_dependencies():
    """Check if yt-dlp is installed, if not, install it."""
    if shutil.which('yt-dlp') is None:
        print("yt-dlp not found. Installing...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yt-dlp'])
            print("yt-dlp installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install yt-dlp. Please install it manually.")
            sys.exit(1)

# Form for download options
class DownloadForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL()])
    format = SelectField('Format', choices=[
        ('auto', 'Auto'),
        ('mp4', 'MP4'),
        ('webm', 'WebM'),
        ('mkv', 'MKV'),
        ('mp3', 'MP3'),
        ('m4a', 'M4A'),
        ('opus', 'Opus'),
        ('wav', 'WAV'),
        ('flac', 'FLAC')
    ])
    quality = SelectField('Quality', choices=[
        ('best', 'Best'),
        ('1080', '1080p'),
        ('720', '720p'),
        ('480', '480p'),
        ('360', '360p'),
        ('worst', 'Worst')
    ])
    audio_only = BooleanField('Audio Only')
    playlist = BooleanField('Download Playlist')
    subtitles = StringField('Subtitles (comma separated language codes, e.g., en,fr)', validators=[Optional()])
    
    # Cookie and browser options
    cookies = StringField('Cookies (paste cookies in Netscape format)', validators=[Optional()])
    browser_cookies = SelectField('Extract cookies from browser', choices=[
        ('none', 'None'),
        ('chrome', 'Chrome'),
        ('firefox', 'Firefox'),
        ('safari', 'Safari'),
        ('edge', 'Edge'),
        ('opera', 'Opera')
    ], default='none')
    
    # Advanced options
    user_agent = StringField('User Agent', validators=[Optional()])
    referer = StringField('Referer URL', validators=[Optional()])
    custom_headers = TextAreaField('Custom Headers (JSON format)', validators=[Optional()])
    proxy = StringField('Proxy URL (HTTP/HTTPS/SOCKS)', validators=[Optional()])
    use_random_proxy = BooleanField('Use Random Proxy for YouTube')
    
    # OAuth options
    auth_token = StringField('OAuth Token', validators=[Optional()])
    auth_token_type = SelectField('OAuth Token Type', choices=[
        ('Bearer', 'Bearer'),
        ('Basic', 'Basic'),
        ('Digest', 'Digest'),
        ('OAuth', 'OAuth')
    ], default='Bearer')
    
    submit = SubmitField('Download')

# Function to build yt-dlp command
def build_command(form_data, download_id):
    """Build the yt-dlp command based on the form data."""
    cmd = ['yt-dlp']
    
    # Set output directory and filename template
    output_dir = os.path.join(app.config['DOWNLOAD_FOLDER'], download_id)
    os.makedirs(output_dir, exist_ok=True)
    cmd.extend(['-o', os.path.join(output_dir, '%(title)s.%(ext)s')])
    
    # Handle format and quality
    if form_data.get('audio_only'):
        if form_data.get('format') != 'auto' and form_data.get('format') in ['mp3', 'm4a', 'opus', 'wav', 'flac']:
            cmd.extend(['-x', '--audio-format', form_data.get('format')])
        else:
            cmd.extend(['-x', '--audio-format', 'mp3'])  # Default to mp3
    elif form_data.get('format') != 'auto':
        if form_data.get('quality') in ['best', 'worst']:
            quality_prefix = 'b' if form_data.get('quality') == 'best' else 'w'
            cmd.extend(['-f', f'{quality_prefix}v[ext={form_data.get("format")}]+{quality_prefix}a'])
        else:
            # For numeric quality like 1080, 720, etc.
            cmd.extend(['-f', f'bestvideo[height<={form_data.get("quality")}][ext={form_data.get("format")}]+bestaudio'])
    elif form_data.get('quality') not in ['best', 'worst']:
        # For numeric quality like 1080, 720, etc.
        cmd.extend(['-f', f'bestvideo[height<={form_data.get("quality")}]+bestaudio'])
    
    # Handle playlist
    if not form_data.get('playlist'):
        cmd.append('--no-playlist')
    
    # Handle subtitles
    subtitles = form_data.get('subtitles', '').strip()
    if subtitles:
        cmd.extend(['--write-sub', '--sub-langs', subtitles])
    
    # Handle cookies
    cookies = form_data.get('cookies', '').strip()
    if cookies:
        # Create a cookies file
        cookies_file = os.path.join(output_dir, 'cookies.txt')
        with open(cookies_file, 'w') as f:
            f.write(cookies)
        cmd.extend(['--cookies', cookies_file])
    
    # Handle browser cookies
    browser_cookies = form_data.get('browser_cookies')
    if browser_cookies and browser_cookies != 'none':
        cmd.extend(['--cookies-from-browser', browser_cookies])
    
    # Handle user agent
    user_agent = form_data.get('user_agent', '').strip()
    if user_agent:
        cmd.extend(['--user-agent', user_agent])
    
    # Handle referer
    referer = form_data.get('referer', '').strip()
    if referer:
        cmd.extend(['--referer', referer])
    
    # Handle proxy
    proxy = form_data.get('proxy', '').strip()
    use_random_proxy = form_data.get('use_random_proxy', False)
    
    if proxy:
        cmd.extend(['--proxy', proxy])
    elif use_random_proxy and PROXY_SUPPORT:
        # Check if URL is from YouTube
        url = form_data.get('url', '')
        if is_youtube_url(url):
            # Get a random proxy for YouTube URL
            random_proxy = get_random_proxy(url)
            if random_proxy:
                print(f"Using random proxy: {random_proxy}")
                cmd.extend(['--proxy', random_proxy])
    
    # Handle custom headers and OAuth token
    custom_headers = form_data.get('custom_headers', '').strip()
    auth_token = form_data.get('auth_token', '').strip()
    auth_token_type = form_data.get('auth_token_type', 'Bearer')
    
    if auth_token:
        # Create Authorization header with the token
        auth_header = f'Authorization: {auth_token_type} {auth_token}'
        
        if custom_headers:
            try:
                # Parse existing headers
                headers_dict = json.loads(custom_headers)
                # Add Authorization header
                headers_dict['Authorization'] = f'{auth_token_type} {auth_token}'
                # Convert back to JSON
                cmd.extend(['--add-headers', json.dumps(headers_dict)])
            except json.JSONDecodeError:
                # If not valid JSON, create a new headers dict
                headers_dict = {'Authorization': f'{auth_token_type} {auth_token}'}
                cmd.extend(['--add-headers', json.dumps(headers_dict)])
        else:
            # No existing headers, just add the Authorization header
            headers_dict = {'Authorization': f'{auth_token_type} {auth_token}'}
            cmd.extend(['--add-headers', json.dumps(headers_dict)])
    elif custom_headers:
        try:
            # Validate JSON format
            json.loads(custom_headers)
            cmd.extend(['--add-headers', custom_headers])
        except json.JSONDecodeError:
            # If not valid JSON, ignore
            pass
    
    # Add URL
    cmd.append(form_data.get('url'))
    
    return cmd, output_dir

# Function to run download in background
def run_download(download_id, cmd, output_dir):
    """Run the download command in a background thread."""
    active_downloads[download_id] = {
        'status': 'running',
        'progress': 0,
        'output_dir': output_dir,
        'log': [],
        'files': [],
        'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': None
    }
    
    try:
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        for line in process.stdout:
            # Parse progress information
            if '[download]' in line and '%' in line:
                try:
                    progress_str = line.split('%')[0].split()[-1]
                    progress = float(progress_str)
                    active_downloads[download_id]['progress'] = progress
                except (ValueError, IndexError):
                    pass
            
            # Add to log
            active_downloads[download_id]['log'].append(line.strip())
            
            # Limit log size
            if len(active_downloads[download_id]['log']) > 100:
                active_downloads[download_id]['log'] = active_downloads[download_id]['log'][-100:]
        
        process.wait()
        
        # Find downloaded files
        files = []
        for root, _, filenames in os.walk(output_dir):
            for filename in filenames:
                if not filename.endswith('.part'):
                    files.append(os.path.join(root, filename))
        
        if process.returncode == 0:
            active_downloads[download_id]['status'] = 'completed'
            active_downloads[download_id]['files'] = files
            active_downloads[download_id]['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Move to completed downloads
            completed_downloads[download_id] = active_downloads[download_id].copy()
            del active_downloads[download_id]
        else:
            active_downloads[download_id]['status'] = 'failed'
            active_downloads[download_id]['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Move to completed downloads
            completed_downloads[download_id] = active_downloads[download_id].copy()
            del active_downloads[download_id]
    
    except Exception as e:
        active_downloads[download_id]['status'] = 'failed'
        active_downloads[download_id]['log'].append(f"Error: {str(e)}")
        active_downloads[download_id]['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Move to completed downloads
        completed_downloads[download_id] = active_downloads[download_id].copy()
        del active_downloads[download_id]

# Context processor for templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Routes
@app.route('/')
def index():
    """Home page with download form."""
    form = DownloadForm()
    return render_template('index.html', form=form, active_downloads=active_downloads, completed_downloads=completed_downloads)

@app.route('/download', methods=['POST'])
def download():
    """Handle download form submission."""
    form = DownloadForm()
    
    if form.validate_on_submit():
        # Generate unique ID for this download
        download_id = str(uuid.uuid4())
        
        # Build command
        form_data = {
            'url': form.url.data,
            'format': form.format.data,
            'quality': form.quality.data,
            'audio_only': form.audio_only.data,
            'playlist': form.playlist.data,
            'subtitles': form.subtitles.data,
            'cookies': form.cookies.data,
            'browser_cookies': form.browser_cookies.data,
            'user_agent': form.user_agent.data,
            'referer': form.referer.data,
            'custom_headers': form.custom_headers.data,
            'auth_token': form.auth_token.data,
            'auth_token_type': form.auth_token_type.data
        }
        
        cmd, output_dir = build_command(form_data, download_id)
        
        # Start download in background thread
        thread = threading.Thread(target=run_download, args=(download_id, cmd, output_dir))
        thread.daemon = True
        thread.start()
        
        flash('Download started!', 'success')
        return redirect(url_for('download_status', download_id=download_id))
    
    flash('Invalid form submission. Please check the URL.', 'danger')
    return redirect(url_for('index'))

@app.route('/status/<download_id>')
def download_status(download_id):
    """Show status of a specific download."""
    if download_id in active_downloads:
        download = active_downloads[download_id]
        return render_template('status.html', download_id=download_id, download=download, status='active')
    elif download_id in completed_downloads:
        download = completed_downloads[download_id]
        return render_template('status.html', download_id=download_id, download=download, status='completed')
    else:
        flash('Download not found.', 'danger')
        return redirect(url_for('index'))

@app.route('/api/status/<download_id>')
def api_download_status(download_id):
    """API endpoint to get download status."""
    if download_id in active_downloads:
        return jsonify(active_downloads[download_id])
    elif download_id in completed_downloads:
        return jsonify(completed_downloads[download_id])
    else:
        return jsonify({'error': 'Download not found'}), 404

@app.route('/download/<download_id>/<path:filename>')
def download_file(download_id, filename):
    """Download a completed file."""
    if download_id in completed_downloads:
        download = completed_downloads[download_id]
        for file_path in download['files']:
            if os.path.basename(file_path) == filename:
                return send_file(file_path, as_attachment=True)
    
    flash('File not found.', 'danger')
    return redirect(url_for('index'))

@app.route('/clear/<download_id>')
def clear_download(download_id):
    """Clear a completed download."""
    if download_id in completed_downloads:
        # Remove files
        download = completed_downloads[download_id]
        output_dir = download['output_dir']
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        
        # Remove from completed downloads
        del completed_downloads[download_id]
        
        flash('Download cleared.', 'success')
    
    return redirect(url_for('index'))

# Cleanup function to remove old downloads
def cleanup_old_downloads():
    """Remove downloads older than 24 hours."""
    while True:
        now = datetime.now()
        
        # Check completed downloads
        for download_id in list(completed_downloads.keys()):
            download = completed_downloads[download_id]
            end_time = datetime.strptime(download['end_time'], '%Y-%m-%d %H:%M:%S')
            
            # If older than 24 hours, remove
            if (now - end_time).total_seconds() > 24 * 60 * 60:
                output_dir = download['output_dir']
                if os.path.exists(output_dir):
                    shutil.rmtree(output_dir)
                
                del completed_downloads[download_id]
        
        # Sleep for 1 hour
        time.sleep(60 * 60)

# Check dependencies
check_dependencies()

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_downloads)
cleanup_thread.daemon = True
cleanup_thread.start()

if __name__ == '__main__':
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Web Multi-Format Video and Audio Downloader')
    parser.add_argument('--port', type=int, default=int(os.environ.get('PORT', 12000)),
                        help='Port to run the server on')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help='Host to run the server on')
    parser.add_argument('--debug', action='store_true',
                        help='Run in debug mode')
    args = parser.parse_args()
    
    # Determine if we're running in production or development
    is_production = os.environ.get('RENDER', False) or os.environ.get('PRODUCTION', False)
    
    # Run app
    app.run(host=args.host, port=args.port, debug=args.debug or not is_production)