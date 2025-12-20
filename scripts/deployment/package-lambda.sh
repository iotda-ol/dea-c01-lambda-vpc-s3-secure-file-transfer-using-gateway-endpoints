#!/bin/bash
# Lambda Deployment Package Creation Script
# Purpose: Package Lambda function with dependencies

set -e

echo "====================================="
echo "Lambda Package Builder"
echo "====================================="

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAMBDA_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$LAMBDA_DIR/src"
BUILD_DIR="$LAMBDA_DIR/build"
PACKAGE_NAME="lambda_function.zip"
OUTPUT_PATH="$LAMBDA_DIR/$PACKAGE_NAME"

# Clean build directory
echo "Cleaning build directory..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Install dependencies
echo "Installing dependencies..."
pip install -r "$LAMBDA_DIR/requirements.txt" -t "$BUILD_DIR" --quiet

# Copy source code
echo "Copying source code..."
cp -r "$SRC_DIR"/* "$BUILD_DIR/"

# Remove unnecessary files
echo "Removing unnecessary files..."
cd "$BUILD_DIR"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Create ZIP package
echo "Creating deployment package..."
rm -f "$OUTPUT_PATH"
zip -r "$OUTPUT_PATH" . -q

# Calculate package size
PACKAGE_SIZE=$(du -h "$OUTPUT_PATH" | cut -f1)

echo "====================================="
echo "Package created successfully!"
echo "Location: $OUTPUT_PATH"
echo "Size: $PACKAGE_SIZE"
echo "====================================="

# Verify package contents
echo ""
echo "Package contents:"
unzip -l "$OUTPUT_PATH" | head -20
echo "..."
echo "(showing first 20 files)"

exit 0
