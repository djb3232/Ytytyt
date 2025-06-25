#!/bin/bash
# Simple wrapper script for multi_downloader.py

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Run the Python script with all arguments passed to this script
python3 "$SCRIPT_DIR/multi_downloader.py" "$@"