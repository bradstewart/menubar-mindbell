#!/bin/bash
# Install MindBell.app to Applications

echo "Installing MindBell to /Applications..."

# Check if app bundle exists
if [ ! -d "dist/MindBell.app" ]; then
    echo "❌ Error: dist/MindBell.app not found!"
    echo "Run ./scripts/build.sh first"
    exit 1
fi

# Copy to Applications
cp -r dist/MindBell.app /Applications/

if [ $? -eq 0 ]; then
    echo "✅ MindBell installed to /Applications"
    echo ""
    echo "To add to Login Items (auto-start):"
    echo "  1. Open System Settings"
    echo "  2. Go to General → Login Items"
    echo "  3. Click + and add MindBell from Applications"
else
    echo "❌ Installation failed!"
    exit 1
fi