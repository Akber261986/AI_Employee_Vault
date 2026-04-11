#!/bin/bash
# Silver Tier AI Employee - Master Orchestrator Startup (Mac/Linux)

echo "========================================"
echo "  Silver Tier AI Employee"
echo "  Starting Master Orchestrator"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found"
    exit 1
fi

# Check dependencies
python3 -c "import watchdog, google.auth, playwright" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing Silver Tier dependencies..."
    pip3 install -e .
    playwright install chromium
    echo ""
fi

echo "Starting Orchestrator..."
echo ""
echo "This will start:"
echo "- Gmail Watcher"
echo "- File System Watcher"
echo ""
echo "Press Ctrl+C to stop all watchers"
echo "========================================"
echo ""

python3 orchestrator.py
