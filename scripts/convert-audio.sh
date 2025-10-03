#!/bin/bash
# Convert audio files to AIFF format for macOS

echo "Converting audio files to AIFF..."

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ Error: ffmpeg is not installed!"
    echo "Install with: brew install ffmpeg"
    exit 1
fi

# Convert all OGG files in media directory to AIFF
for file in media/*.ogg; do
    if [ -f "$file" ]; then
        basename=$(basename "$file" .ogg)
        output="media/${basename}.aiff"
        
        if [ -f "$output" ]; then
            echo "Skipping $basename (already converted)"
        else
            echo "Converting $basename..."
            ffmpeg -i "$file" -acodec pcm_s16be "$output" -loglevel error
            
            if [ $? -eq 0 ]; then
                echo "✅ Converted $basename"
            else
                echo "❌ Failed to convert $basename"
            fi
        fi
    fi
done

echo "Done!"