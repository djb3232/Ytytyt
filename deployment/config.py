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
