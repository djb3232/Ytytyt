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
    --limit-rate RATE               Maximum download rate (e.g. 50K, 4.2M)
    --no-mtime                      Don't use the Last-modified header to set the file modification time
"""

import argparse
import os
import sys
import subprocess
import shutil

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
    
    parser.add_argument('--limit-rate', 
                        help='Maximum download rate (e.g. 50K, 4.2M)')
    
    parser.add_argument('--no-mtime', action='store_true',
                        help='Don\'t use the Last-modified header to set the file modification time')
    
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
    
    # Handle rate limit
    if args.limit_rate:
        cmd.extend(['--limit-rate', args.limit_rate])
    
    # Handle mtime
    if args.no_mtime:
        cmd.append('--no-mtime')
    
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