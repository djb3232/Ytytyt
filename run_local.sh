#!/bin/bash
# Script to run the Multi-Format Video and Audio Downloader locally

# Create downloads directory if it doesn't exist
mkdir -p downloads

# Set environment variables
export PORT=12000
export SECRET_KEY="local-dev-key"

# Run the application
python web_downloader.py