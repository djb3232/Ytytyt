#!/usr/bin/env python3
"""
FastCGI script for Multi-Format Downloader web application.
This file is used by FastCGI-enabled web servers to serve the application.
"""

import sys
import os

# Add the directory containing the app to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Try to import flup for FastCGI
try:
    from flup.server.fcgi import WSGIServer
except ImportError:
    print("Error: flup package is required for FastCGI.")
    print("Install it with: pip install flup")
    sys.exit(1)

# Import the app
from web_downloader import app

if __name__ == '__main__':
    WSGIServer(app).run()