#!/bin/bash
# Clean build artifacts and temporary files

echo "Cleaning build artifacts..."

# Remove build directories
rm -rf build dist

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Remove .DS_Store files
find . -type f -name ".DS_Store" -delete

echo "✅ Cleaned!"