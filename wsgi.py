#!/usr/bin/env python3
"""
WSGI configuration for Multi-Format Downloader web application.
This file is used by WSGI servers to serve the application.
"""

import sys
import os

# Add the directory containing the app to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the app
from web_downloader import app as application

# For debugging
if __name__ == '__main__':
    application.run()