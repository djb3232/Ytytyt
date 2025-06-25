#!/bin/bash
# Installation script for multi_downloader

echo "Installing Multi-Format Video and Audio Downloader..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install -r "$SCRIPT_DIR/requirements.txt"

# Make scripts executable
chmod +x "$SCRIPT_DIR/multi_downloader.py" "$SCRIPT_DIR/download.sh" "$SCRIPT_DIR/gui_downloader.py" "$SCRIPT_DIR/web_downloader.py" "$SCRIPT_DIR/run_web_server.sh" "$SCRIPT_DIR/run_production.sh"

# Install desktop entry for Linux users
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing desktop entry..."
    DESKTOP_DIR="$HOME/.local/share/applications"
    mkdir -p "$DESKTOP_DIR"
    
    # Create desktop entry with correct path
    sed "s|/path/to|$SCRIPT_DIR|g" "$SCRIPT_DIR/multi-downloader.desktop" > "$DESKTOP_DIR/multi-downloader.desktop"
    
    echo "Desktop entry installed. You can now find 'Multi-Format Downloader' in your applications menu."
fi

echo "Installation completed successfully!"
echo ""
echo "You can use the downloader in the following ways:"
echo ""
echo "1. Command Line Interface:"
echo "  $SCRIPT_DIR/download.sh [options] URL [URL...]"
echo "  or"
echo "  python3 $SCRIPT_DIR/multi_downloader.py [options] URL [URL...]"
echo ""
echo "2. Graphical User Interface:"
echo "  python3 $SCRIPT_DIR/gui_downloader.py"
echo ""
echo "3. Web Interface:"
echo "  $SCRIPT_DIR/run_web_server.sh"
echo "  Then open http://localhost:12000 in your browser"
echo ""
echo "For production web server:"
echo "  $SCRIPT_DIR/run_production.sh"
echo ""
echo "For help and options, run:"
echo "  $SCRIPT_DIR/download.sh --help"