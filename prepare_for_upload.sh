#!/bin/bash
# Script to prepare the Multi-Format Downloader for upload to a shared web host

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DEPLOY_DIR="$SCRIPT_DIR/deployment"

# Create deployment directory if it doesn't exist
mkdir -p "$DEPLOY_DIR"

# Clean up any previous deployment files
rm -rf "$DEPLOY_DIR"/*

# Copy all necessary files to the deployment directory
echo "Copying files to deployment directory..."
cp -r "$SCRIPT_DIR/static" "$DEPLOY_DIR/"
cp -r "$SCRIPT_DIR/templates" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/web_downloader.py" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/multi_downloader.py" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/requirements.txt" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/README.md" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/UPLOAD_GUIDE.md" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/wsgi.py" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/app.fcgi" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/passenger_wsgi.py" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/.htaccess" "$DEPLOY_DIR/"

# Create downloads directory in the deployment folder
mkdir -p "$DEPLOY_DIR/downloads"

# Make scripts executable
chmod +x "$DEPLOY_DIR/web_downloader.py"
chmod +x "$DEPLOY_DIR/multi_downloader.py"
chmod +x "$DEPLOY_DIR/wsgi.py"
chmod +x "$DEPLOY_DIR/app.fcgi"
chmod +x "$DEPLOY_DIR/passenger_wsgi.py"

# Create a shared hosting configuration file
cat > "$DEPLOY_DIR/config.py" << 'EOF'
"""
Configuration file for shared hosting environments.
Modify these settings according to your hosting provider's requirements.
"""

# Secret key for session encryption (change this to a random string)
SECRET_KEY = 'change-this-to-a-random-string'

# Path where downloaded files will be stored
# For shared hosting, this should be an absolute path
# Example: '/home/username/public_html/ytytyt/downloads'
DOWNLOAD_DIR = 'downloads'

# Maximum file age in seconds (24 hours by default)
MAX_FILE_AGE = 86400

# Debug mode (set to False in production)
DEBUG = False

# Host and port settings
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 8080       # Default port (your host may require a specific port)

# Allowed file formats
VIDEO_FORMATS = ['auto', 'mp4', 'webm', 'mkv']
AUDIO_FORMATS = ['mp3', 'm4a', 'opus', 'wav', 'flac']

# Maximum concurrent downloads
MAX_CONCURRENT_DOWNLOADS = 3
EOF

# Create a simple PHP info file to check PHP configuration
cat > "$DEPLOY_DIR/info.php" << 'EOF'
<?php
// Show PHP configuration
phpinfo();
EOF

# Create a simple test script
cat > "$DEPLOY_DIR/test.py" << 'EOF'
#!/usr/bin/env python3
"""
Test script to verify Python is working correctly on the server.
"""
import sys
import os

def main():
    """Print system information for debugging."""
    print("Content-Type: text/plain\n")
    print("Python Test Script")
    print("=================")
    print(f"Python Version: {sys.version}")
    print(f"Python Path: {sys.executable}")
    print(f"Current Directory: {os.getcwd()}")
    print(f"Script Directory: {os.path.dirname(os.path.abspath(__file__))}")
    print("\nEnvironment Variables:")
    for key, value in sorted(os.environ.items()):
        print(f"  {key}: {value}")
    print("\nInstalled Packages:")
    try:
        import pkg_resources
        for pkg in sorted([f"{d.project_name}=={d.version}" for d in pkg_resources.working_set]):
            print(f"  {pkg}")
    except ImportError:
        print("  pkg_resources not available")

if __name__ == "__main__":
    main()
EOF

chmod +x "$DEPLOY_DIR/test.py"

# Create a ZIP archive for easy upload
echo "Creating ZIP archive..."
cd "$SCRIPT_DIR"
zip -r "$DEPLOY_DIR/ytytyt_web.zip" deployment/

echo "Deployment package created successfully!"
echo "Files are available in: $DEPLOY_DIR"
echo "ZIP archive: $DEPLOY_DIR/ytytyt_web.zip"
echo ""
echo "Please refer to UPLOAD_GUIDE.md for instructions on how to upload to your shared host."