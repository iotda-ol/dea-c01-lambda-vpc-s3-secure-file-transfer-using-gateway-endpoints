#!/bin/bash
# Script to deploy infrastructure with Terraform

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TERRAFORM_DIR="$PROJECT_ROOT/terraform"

echo "Deploying Secure File Transfer Solution..."

# Build Lambda package
echo "Step 1: Building Lambda deployment package..."
bash "$SCRIPT_DIR/build_lambda.sh"

# Initialize Terraform
echo "Step 2: Initializing Terraform..."
cd "$TERRAFORM_DIR"
terraform init

# Validate Terraform configuration
echo "Step 3: Validating Terraform configuration..."
terraform validate

# Plan deployment
echo "Step 4: Planning deployment..."
terraform plan -out=tfplan

# Apply deployment
echo "Step 5: Applying deployment..."
read -p "Do you want to apply this plan? (yes/no): " confirm
if [ "$confirm" = "yes" ]; then
    terraform apply tfplan
    rm -f tfplan
    
    echo ""
    echo "Deployment completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Update SFTP credentials in AWS Secrets Manager"
    echo "2. Test the Lambda function"
    echo "3. Enable the EventBridge schedule if needed"
else
    echo "Deployment cancelled."
    rm -f tfplan
fi
