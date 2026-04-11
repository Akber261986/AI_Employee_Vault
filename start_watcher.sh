#!/bin/bash
# Bronze Tier AI Employee - Startup Script for Mac/Linux

echo "========================================"
echo "  Bronze Tier AI Employee"
echo "  Starting File System Watcher"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.13+ from python.org"
    exit 1
fi

# Check if watchdog is installed
python3 -c "import watchdog" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required dependencies..."
    pip3 install watchdog
    echo ""
fi

echo "Starting File System Watcher..."
echo "Monitoring: $(pwd)/Inbox"
echo ""
echo "Press Ctrl+C to stop"
echo "========================================"
echo ""

# Start the watcher
python3 filesystem_watcher.py
