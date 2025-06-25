#!/usr/bin/env python3
"""
Multi-Format Video and Audio Downloader

A script to download videos and audio from various platforms in different formats.
Uses yt-dlp, a powerful fork of youtube-dl with additional features.

Usage:
    python multi_downloader.py [options] URL [URL...]

Options:
    -h, --help                      Show this help message and exit
    -f, --format FORMAT             Specify output format (mp4, webm, mp3, m4a, etc.)
    -q, --quality QUALITY           Specify quality (best, worst, 1080, 720, etc.)
    -o, --output TEMPLATE           Output filename template
    -a, --audio-only                Download audio only
    -p, --playlist                  Download all videos in a playlist
    -s, --subtitles LANGS           Download subtitles (comma separated language codes)
    -l, --list-formats              List available formats instead of downloading
    -i, --info                      Display video info instead of downloading
    --proxy URL                     Use the specified HTTP/HTTPS/SOCKS proxy
    --random-proxy                  Use a random proxy for YouTube downloads
    --limit-rate RATE               Maximum download rate (e.g. 50K, 4.2M)
    --no-mtime                      Don't use the Last-modified header to set the file modification time
    --cookies FILE                  Path to cookies file (Netscape or browser cookies.txt format)
    --browser-cookies BROWSER       Extract cookies from browser (chrome, firefox, safari, edge, opera)
    --user-agent AGENT              Specify a custom user agent
    --referer URL                   Specify a custom referer, useful for bypassing some restrictions
    --headers JSON                  Specify custom HTTP headers as a JSON string
    --auth-token TOKEN              Specify an OAuth token for authentication
    --auth-token-type TYPE          Specify the OAuth token type (Bearer, Basic, etc.)
"""

import argparse
import os
import sys
import subprocess
import shutil
import logging

# Import proxy management module
try:
    from proxies import get_random_proxy, is_youtube_url
    PROXY_SUPPORT = True
except ImportError:
    PROXY_SUPPORT = False
    logging.warning("Proxy module not found. Random proxy feature will be disabled.")

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

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Download videos and audio in various formats')
    
    parser.add_argument('urls', nargs='+', help='URLs to download')
    
    parser.add_argument('-f', '--format', 
                        help='Specify output format (mp4, webm, mp3, m4a, etc.)')
    
    parser.add_argument('-q', '--quality', 
                        help='Specify quality (best, worst, 1080, 720, etc.)')
    
    parser.add_argument('-o', '--output', 
                        help='Output filename template')
    
    parser.add_argument('-a', '--audio-only', action='store_true',
                        help='Download audio only')
    
    parser.add_argument('-p', '--playlist', action='store_true',
                        help='Download all videos in a playlist')
    
    parser.add_argument('-s', '--subtitles', 
                        help='Download subtitles (comma separated language codes)')
    
    parser.add_argument('-l', '--list-formats', action='store_true',
                        help='List available formats instead of downloading')
    
    parser.add_argument('-i', '--info', action='store_true',
                        help='Display video info instead of downloading')
    
    parser.add_argument('--proxy', 
                        help='Use the specified HTTP/HTTPS/SOCKS proxy')
    
    parser.add_argument('--random-proxy', action='store_true',
                        help='Use a random proxy for YouTube downloads')
    
    parser.add_argument('--limit-rate', 
                        help='Maximum download rate (e.g. 50K, 4.2M)')
    
    parser.add_argument('--no-mtime', action='store_true',
                        help='Don\'t use the Last-modified header to set the file modification time')
    
    parser.add_argument('--cookies', 
                        help='Path to cookies file (Netscape or browser cookies.txt format)')
    
    parser.add_argument('--browser-cookies', choices=['chrome', 'firefox', 'safari', 'edge', 'opera'],
                        help='Extract cookies from browser (chrome, firefox, safari, edge, opera)')
    
    parser.add_argument('--user-agent',
                        help='Specify a custom user agent')
    
    parser.add_argument('--referer',
                        help='Specify a custom referer, useful for bypassing some restrictions')
    
    parser.add_argument('--headers',
                        help='Specify custom HTTP headers as a JSON string')
    
    parser.add_argument('--auth-token',
                        help='Specify an OAuth token for authentication')
    
    parser.add_argument('--auth-token-type',
                        default='Bearer',
                        help='Specify the OAuth token type (Bearer, Basic, etc.)')
    
    return parser.parse_args()

def build_command(args):
    """Build the yt-dlp command based on the arguments."""
    cmd = ['yt-dlp']
    
    # Handle format and quality
    if args.audio_only:
        if args.format in ['mp3', 'm4a', 'opus', 'wav', 'flac']:
            cmd.extend(['-x', '--audio-format', args.format])
        else:
            cmd.extend(['-x', '--audio-format', 'mp3'])  # Default to mp3
    elif args.format:
        if args.quality:
            if args.quality in ['best', 'worst']:
                quality_prefix = 'b' if args.quality == 'best' else 'w'
                cmd.extend(['-f', f'{quality_prefix}v[ext={args.format}]+{quality_prefix}a'])
            else:
                # For numeric quality like 1080, 720, etc.
                cmd.extend(['-f', f'bestvideo[height<={args.quality}][ext={args.format}]+bestaudio'])
        else:
            cmd.extend(['-f', f'bestvideo[ext={args.format}]+bestaudio'])
    elif args.quality:
        if args.quality in ['best', 'worst']:
            quality_prefix = 'b' if args.quality == 'best' else 'w'
            cmd.extend(['-f', f'{quality_prefix}v+{quality_prefix}a'])
        else:
            # For numeric quality like 1080, 720, etc.
            cmd.extend(['-f', f'bestvideo[height<={args.quality}]+bestaudio'])
    
    # Handle output template
    if args.output:
        cmd.extend(['-o', args.output])
    
    # Handle playlist
    if not args.playlist:
        cmd.append('--no-playlist')
    
    # Handle subtitles
    if args.subtitles:
        cmd.extend(['--write-sub', '--sub-langs', args.subtitles])
    
    # Handle list formats
    if args.list_formats:
        cmd.append('--list-formats')
    
    # Handle info
    if args.info:
        cmd.append('--dump-json')
    
    # Handle proxy
    if args.proxy:
        cmd.extend(['--proxy', args.proxy])
    elif args.random_proxy and PROXY_SUPPORT:
        # Check if any URL is from YouTube
        youtube_urls = [url for url in args.urls if is_youtube_url(url)]
        if youtube_urls:
            # Get a random proxy for YouTube URLs
            random_proxy = get_random_proxy(youtube_urls[0])
            if random_proxy:
                print(f"Using random proxy: {random_proxy}")
                cmd.extend(['--proxy', random_proxy])
    
    # Handle rate limit
    if args.limit_rate:
        cmd.extend(['--limit-rate', args.limit_rate])
    
    # Handle mtime
    if args.no_mtime:
        cmd.append('--no-mtime')
    
    # Handle cookies
    if args.cookies:
        cmd.extend(['--cookies', args.cookies])
    
    # Handle browser cookies
    if args.browser_cookies:
        cmd.extend(['--cookies-from-browser', args.browser_cookies])
    
    # Handle user agent
    if args.user_agent:
        cmd.extend(['--user-agent', args.user_agent])
    
    # Handle referer
    if args.referer:
        cmd.extend(['--referer', args.referer])
    
    # Handle custom headers
    if args.headers:
        cmd.extend(['--add-headers', args.headers])
    
    # Handle OAuth token
    if args.auth_token:
        # Create Authorization header with the token
        auth_header = f'Authorization: {args.auth_token_type} {args.auth_token}'
        
        if args.headers:
            # If headers already exist, we need to append to them
            import json
            try:
                # Parse existing headers
                existing_headers = json.loads(args.headers)
                # Add Authorization header
                existing_headers['Authorization'] = f'{args.auth_token_type} {args.auth_token}'
                # Convert back to JSON
                cmd.extend(['--add-headers', json.dumps(existing_headers)])
            except json.JSONDecodeError:
                # If headers are not in JSON format, just add the Authorization header
                cmd.extend(['--add-headers', auth_header])
        else:
            # No existing headers, just add the Authorization header
            cmd.extend(['--add-headers', auth_header])
    
    # Add URLs
    cmd.extend(args.urls)
    
    return cmd

def main():
    """Main function."""
    # Check if yt-dlp is installed
    check_dependencies()
    
    # Parse arguments
    args = parse_arguments()
    
    # Build command
    cmd = build_command(args)
    
    # Print the command for debugging
    print(f"Executing: {' '.join(cmd)}")
    
    # Execute command
    try:
        subprocess.run(cmd, check=True)
        print("Download completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during download: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()