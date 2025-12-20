#!/bin/bash
# Terraform Deployment Script
# Purpose: Deploy infrastructure with validation

set -e

# Configuration
ENVIRONMENT="${1:-dev}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
TF_DIR="$REPO_ROOT/terraform/environments/$ENVIRONMENT"

echo "====================================="
echo "Infrastructure Deployment"
echo "Environment: $ENVIRONMENT"
echo "====================================="

# Validate environment
if [ ! -d "$TF_DIR" ]; then
    echo "Error: Environment '$ENVIRONMENT' not found"
    echo "Available environments:"
    ls -1 "$REPO_ROOT/terraform/environments/"
    exit 1
fi

# Check if terraform.tfvars exists
if [ ! -f "$TF_DIR/terraform.tfvars" ]; then
    echo "Error: terraform.tfvars not found"
    echo "Please copy terraform.tfvars.example to terraform.tfvars and update values"
    exit 1
fi

# Change to Terraform directory
cd "$TF_DIR"

# Initialize Terraform
echo ""
echo "Step 1: Initializing Terraform..."
terraform init

# Validate configuration
echo ""
echo "Step 2: Validating configuration..."
terraform validate

# Format check
echo ""
echo "Step 3: Checking formatting..."
terraform fmt -check -recursive || {
    echo "Warning: Terraform files need formatting"
    echo "Run: terraform fmt -recursive"
}

# Plan
echo ""
echo "Step 4: Creating execution plan..."
terraform plan -out=tfplan

# Apply
echo ""
echo "Step 5: Applying changes..."
read -p "Do you want to apply these changes? (yes/no): " CONFIRM

if [ "$CONFIRM" = "yes" ]; then
    terraform apply tfplan
    
    echo ""
    echo "====================================="
    echo "Deployment completed successfully!"
    echo "====================================="
    
    # Show outputs
    echo ""
    echo "Outputs:"
    terraform output
else
    echo "Deployment cancelled"
    rm -f tfplan
    exit 0
fi

# Cleanup
rm -f tfplan

exit 0
