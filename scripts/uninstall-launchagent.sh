#!/bin/bash
# Uninstall MindBell LaunchAgent

PLIST_NAME="art.bstew.mindbell.plist"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "Uninstalling MindBell LaunchAgent..."

# Unload the agent if it exists
if [ -f "$PLIST_PATH" ]; then
    launchctl unload $PLIST_PATH
    rm $PLIST_PATH
    echo "✅ MindBell LaunchAgent uninstalled"
else
    echo "LaunchAgent not found at $PLIST_PATH"
fi