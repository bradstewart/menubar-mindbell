#!/bin/bash
# Install MindBell as a LaunchAgent (auto-start alternative)

PLIST_NAME="art.bstew.mindbell.plist"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "Installing MindBell LaunchAgent..."

# Check if app bundle exists
if [ ! -d "dist/MindBell.app" ]; then
    echo "❌ Error: dist/MindBell.app not found!"
    echo "Run ./scripts/build.sh first"
    exit 1
fi

# Create LaunchAgents directory if it doesn't exist
mkdir -p ~/Library/LaunchAgents

# Copy plist file
cp $PLIST_NAME ~/Library/LaunchAgents/

# Load the agent
launchctl load $PLIST_PATH

if [ $? -eq 0 ]; then
    echo "✅ MindBell LaunchAgent installed and loaded"
    echo ""
    echo "MindBell will now start automatically at login"
    echo ""
    echo "To uninstall LaunchAgent:"
    echo "  ./scripts/uninstall-launchagent.sh"
else
    echo "❌ LaunchAgent installation failed!"
    exit 1
fi