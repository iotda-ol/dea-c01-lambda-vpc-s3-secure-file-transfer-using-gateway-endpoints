#!/bin/bash
# Package Lambda function for deployment

echo "Starting Lambda packaging process..."

# Create temp directory
rm -rf /tmp/lambda-package
mkdir -p /tmp/lambda-package

# Copy source code
echo "Copying source code..."
cp -r src /tmp/lambda-package/

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -t /tmp/lambda-package/

# Create ZIP file
echo "Creating deployment package..."
cd /tmp/lambda-package
zip -r lambda-package.zip .

# Move to project root
mv lambda-package.zip /home/runner/work/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints/

echo "Lambda package created: lambda-package.zip"
echo "Package size:"
ls -lh /home/runner/work/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints/lambda-package.zip
