#!/bin/bash
# Build MindBell.app bundle

echo "Building MindBell.app..."

# Clean previous builds
rm -rf build dist

# Build the app
uv run python setup.py py2app

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "App bundle created at: dist/MindBell.app"
    echo ""
    echo "To test the app:"
    echo "  open dist/MindBell.app"
else
    echo "❌ Build failed!"
    exit 1
fi