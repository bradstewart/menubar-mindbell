# MindBell Scripts

This directory contains all the build and deployment scripts for MindBell.

## Development Scripts

- **setup.sh** - Initial project setup (install dependencies, create venv)
- **run.sh** - Run MindBell in development mode
- **clean.sh** - Clean build artifacts and cache files

## Build Scripts

- **build.sh** - Build the MindBell.app bundle
- **test-app.sh** - Test the built app with console output

## Installation Scripts

- **install.sh** - Install MindBell.app to /Applications
- **install-launchagent.sh** - Install as LaunchAgent (auto-start at login)
- **uninstall-launchagent.sh** - Remove LaunchAgent

## Utility Scripts

- **convert-audio.sh** - Convert OGG audio files to AIFF format

## Quick Start

```bash
# First time setup
./scripts/setup.sh

# Run in development
./scripts/run.sh

# Build the app
./scripts/build.sh

# Install to Applications
./scripts/install.sh
```

## Auto-start Options

### Option 1: Login Items (Recommended)
After running `./scripts/install.sh`, manually add MindBell to Login Items in System Settings.

### Option 2: LaunchAgent
```bash
./scripts/install-launchagent.sh
```