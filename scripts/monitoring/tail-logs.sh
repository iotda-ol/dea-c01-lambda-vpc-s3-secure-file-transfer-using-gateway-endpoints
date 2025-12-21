#!/bin/bash
# CloudWatch Logs Monitor Script
# Purpose: Monitor Lambda function logs in real-time

set -e

# Configuration
FUNCTION_NAME="${1:-secure-transfer-dev-function}"
LOG_GROUP="/aws/lambda/$FUNCTION_NAME"

echo "====================================="
echo "CloudWatch Logs Monitor"
echo "Function: $FUNCTION_NAME"
echo "====================================="
echo ""
echo "Monitoring logs (Ctrl+C to exit)..."
echo ""

# Tail logs
aws logs tail "$LOG_GROUP" --follow --format short

exit 0
