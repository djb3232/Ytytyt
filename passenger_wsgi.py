#!/usr/bin/env python3
"""
Passenger WSGI configuration for Multi-Format Downloader web application.
This file is used by Passenger to serve the application.
"""

import sys
import os

# If using a virtual environment with Passenger
VENV_PATH = os.path.join(os.getcwd(), 'venv')
if os.path.exists(VENV_PATH):
    INTERP = os.path.join(VENV_PATH, 'bin', 'python')
    if sys.executable != INTERP:
        os.execl(INTERP, INTERP, *sys.argv)

# Add the directory containing the app to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the app
from web_downloader import app as application