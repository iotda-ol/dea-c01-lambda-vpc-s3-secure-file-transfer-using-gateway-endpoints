#!/bin/bash
# Infrastructure Cleanup Script
# Purpose: Destroy all Terraform-managed resources

set -e

# Configuration
ENVIRONMENT="${1:-dev}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
TF_DIR="$REPO_ROOT/terraform/environments/$ENVIRONMENT"

echo "====================================="
echo "Infrastructure Cleanup"
echo "Environment: $ENVIRONMENT"
echo "====================================="
echo ""
echo "WARNING: This will destroy all resources!"
echo ""

# Validate environment
if [ ! -d "$TF_DIR" ]; then
    echo "Error: Environment '$ENVIRONMENT' not found"
    exit 1
fi

# Confirm destruction
read -p "Are you sure you want to destroy all resources in $ENVIRONMENT? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Cleanup cancelled"
    exit 0
fi

# Change to Terraform directory
cd "$TF_DIR"

# Show what will be destroyed
echo ""
echo "Planning destruction..."
terraform plan -destroy

# Final confirmation
echo ""
read -p "Proceed with destruction? (yes/no): " FINAL_CONFIRM

if [ "$FINAL_CONFIRM" = "yes" ]; then
    terraform destroy -auto-approve
    
    echo ""
    echo "====================================="
    echo "Cleanup completed!"
    echo "====================================="
else
    echo "Cleanup cancelled"
    exit 0
fi

exit 0
