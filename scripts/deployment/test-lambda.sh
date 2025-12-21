#!/bin/bash
# Lambda Function Test Script
# Purpose: Test Lambda function with sample event

set -e

# Configuration
FUNCTION_NAME="${1:-secure-transfer-dev-function}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "====================================="
echo "Lambda Function Test"
echo "Function: $FUNCTION_NAME"
echo "====================================="

# Create test event
TEST_EVENT=$(cat <<EOF
{
  "remote_file_path": "/test/sample.txt",
  "s3_key": "test/sample-$(date +%s).txt",
  "metadata": {
    "source": "test-script",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  }
}
EOF
)

echo ""
echo "Test Event:"
echo "$TEST_EVENT" | jq .

# Invoke Lambda
echo ""
echo "Invoking Lambda function..."
RESPONSE=$(aws lambda invoke \
  --function-name "$FUNCTION_NAME" \
  --payload "$TEST_EVENT" \
  --cli-binary-format raw-in-base64-out \
  --output json \
  /tmp/lambda-response.json)

# Check response
echo ""
echo "Lambda Response:"
echo "$RESPONSE" | jq .

echo ""
echo "Function Result:"
cat /tmp/lambda-response.json | jq .

# Get logs
echo ""
echo "Recent Logs:"
aws logs tail "/aws/lambda/$FUNCTION_NAME" --since 1m

# Cleanup
rm -f /tmp/lambda-response.json

echo ""
echo "====================================="
echo "Test completed!"
echo "====================================="

exit 0
