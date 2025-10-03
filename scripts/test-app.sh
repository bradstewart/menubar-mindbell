#!/bin/bash
# Test the built MindBell.app

echo "Testing MindBell.app..."

if [ ! -d "dist/MindBell.app" ]; then
    echo "❌ Error: dist/MindBell.app not found!"
    echo "Run ./scripts/build.sh first"
    exit 1
fi

# Run the app directly to see console output
echo "Running app with console output..."
echo "Press Ctrl+C to stop"
echo ""

dist/MindBell.app/Contents/MacOS/MindBell