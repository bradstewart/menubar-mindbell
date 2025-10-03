#!/bin/bash
# Initial setup for MindBell development

echo "Setting up MindBell development environment..."

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create virtual environment
echo "Creating Python virtual environment..."
uv venv

# Install dependencies
echo "Installing dependencies..."
uv sync

# Convert audio files if needed
if [ -f "media/jap-rin-1.ogg" ] && [ ! -f "media/jap-rin-1.aiff" ]; then
    echo "Converting audio files..."
    ffmpeg -i media/jap-rin-1.ogg -acodec pcm_s16be media/jap-rin-1.aiff
fi

echo "✅ Setup complete!"
echo ""
echo "To run in development mode:"
echo "  ./scripts/run.sh"
echo ""
echo "To build the app:"
echo "  ./scripts/build.sh"