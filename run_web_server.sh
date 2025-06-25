#!/bin/bash
# Script to run the web server

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Install dependencies if needed
if ! python3 -c "import flask" &> /dev/null; then
    echo "Installing dependencies..."
    python3 -m pip install -r "$SCRIPT_DIR/requirements.txt"
fi

# Create downloads directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/downloads"

# Get port from environment or use default
PORT=${PORT:-12000}

# Run the web server
echo "Starting web server on port $PORT..."
echo "You can access the downloader at http://localhost:$PORT"
echo "Press Ctrl+C to stop the server."

# Run with Flask development server
python3 "$SCRIPT_DIR/web_downloader.py"