#!/bin/bash

# Define variables
ADDON_DIR="mastered"
OUTPUT_FILE="mastered_release.ankiaddon"

# Remove old release if it exists
rm -f "$OUTPUT_FILE"

# Zip the contents of the mastered directory
# Start inside the directory to avoid including the folder itself in the zip root
cd "$ADDON_DIR" || exit
zip -r "../$OUTPUT_FILE" . -x "*.DS_Store" "*__pycache__*"

echo "Successfully built $OUTPUT_FILE"
