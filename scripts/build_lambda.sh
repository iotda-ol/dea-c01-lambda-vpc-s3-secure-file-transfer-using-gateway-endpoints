#!/bin/bash
# Script to build Lambda deployment package

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LAMBDA_DIR="$PROJECT_ROOT/lambda"
BUILD_DIR="$PROJECT_ROOT/build"
OUTPUT_ZIP="$PROJECT_ROOT/lambda_function.zip"

echo "Building Lambda deployment package..."

# Clean up previous build
rm -rf "$BUILD_DIR"
rm -f "$OUTPUT_ZIP"

# Create build directory
mkdir -p "$BUILD_DIR"

# Install dependencies
echo "Installing Python dependencies..."
pip install -r "$LAMBDA_DIR/requirements.txt" -t "$BUILD_DIR" --quiet

# Copy Lambda function
echo "Copying Lambda function..."
cp "$LAMBDA_DIR/lambda_function.py" "$BUILD_DIR/"

# Create zip file
echo "Creating deployment package..."
cd "$BUILD_DIR"
zip -r "$OUTPUT_ZIP" . -q

echo "Lambda deployment package created: $OUTPUT_ZIP"
echo "Size: $(du -h "$OUTPUT_ZIP" | cut -f1)"
