# Troubleshooting Guide

## Common Issues and Solutions

### Local Development Issues

#### 1. SFTP Connection Failed

**Problem:** Cannot connect to local SFTP server

**Symptoms:**
```
Failed to connect to SFTP server: [Errno 61] Connection refused
```

**Solutions:**

1. **Check if SFTP server is running:**
```bash
docker ps | grep sftp
```

2. **Start SFTP server if not running:**
```bash
./scripts/start_local_sftp.sh
```

3. **Check port availability:**
```bash
lsof -i :2222
netstat -an | grep 2222
```

4. **Verify credentials:**
- Username: `testuser`
- Password: `testpass`
- Port: `2222`

5. **Test connection manually:**
```bash
sftp -P 2222 testuser@localhost
```

#### 2. LocalStack S3 Issues

**Problem:** Cannot connect to LocalStack S3

**Solutions:**

1. **Check LocalStack status:**
```bash
localstack status
```

2. **Restart LocalStack:**
```bash
localstack stop
localstack start -d
```

3. **Verify endpoint:**
```bash
aws --endpoint-url=http://localhost:4566 s3 ls
```

4. **Create bucket if missing:**
```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://test-file-transfer-bucket
```

#### 3. Import Errors

**Problem:** `ModuleNotFoundError` when running tests

**Solutions:**

1. **Ensure virtual environment is activated:**
```bash
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. **Check Python path:**
```python
import sys
print(sys.path)
```

4. **Add project to PYTHONPATH:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### AWS Deployment Issues

#### 4. Lambda Timeout

**Problem:** Lambda function times out when accessing S3

**Symptoms:**
```
Task timed out after 30.00 seconds
```

**Solutions:**

1. **Check VPC Gateway Endpoint:**
```bash
aws ec2 describe-vpc-endpoints --vpc-endpoint-ids vpce-xxxxx
```

2. **Verify route table association:**
```bash
aws ec2 describe-route-tables --route-table-ids rtb-xxxxx
```

3. **Check Lambda timeout setting:**
```bash
aws lambda get-function-configuration --function-name sftp-to-s3-transfer
```

4. **Increase timeout:**
```bash
aws lambda update-function-configuration \
    --function-name sftp-to-s3-transfer \
    --timeout 300
```

5. **Verify security group rules:**
```bash
# Allow outbound HTTPS
aws ec2 authorize-security-group-egress \
    --group-id sg-xxxxx \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0
```

#### 5. S3 Access Denied

**Problem:** Lambda cannot upload to S3 bucket

**Symptoms:**
```
botocore.exceptions.ClientError: Access Denied
```

**Solutions:**

1. **Check Lambda IAM role:**
```bash
aws iam get-role --role-name lambda-sftp-s3-role
```

2. **Verify S3 policy attachment:**
```bash
aws iam list-attached-role-policies --role-name lambda-sftp-s3-role
```

3. **Check bucket policy:**
```bash
aws s3api get-bucket-policy --bucket your-bucket-name
```

4. **Test IAM permissions:**
```bash
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::ACCOUNT:role/lambda-sftp-s3-role \
    --action-names s3:PutObject \
    --resource-arns arn:aws:s3:::your-bucket/*
```

5. **Review VPC endpoint policy:**
```bash
aws ec2 describe-vpc-endpoints --vpc-endpoint-ids vpce-xxxxx
```

#### 6. Lambda ENI Issues

**Problem:** Lambda cannot create network interfaces

**Symptoms:**
```
The provided execution role does not have permissions to call CreateNetworkInterface
```

**Solutions:**

1. **Attach VPC execution policy:**
```bash
aws iam attach-role-policy \
    --role-name lambda-sftp-s3-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
```

2. **Check subnet availability:**
```bash
aws ec2 describe-subnets --subnet-ids subnet-xxxxx
```

3. **Verify security group exists:**
```bash
aws ec2 describe-security-groups --group-ids sg-xxxxx
```

### Configuration Issues

#### 7. Environment Variables Not Loading

**Problem:** Configuration values are missing or incorrect

**Solutions:**

1. **Check .env file exists:**
```bash
ls -la .env
cat .env
```

2. **Load environment variables:**
```python
from dotenv import load_dotenv
load_dotenv()
```

3. **For Lambda, verify environment variables:**
```bash
aws lambda get-function-configuration \
    --function-name sftp-to-s3-transfer \
    --query 'Environment.Variables'
```

4. **Update Lambda environment variables:**
```bash
aws lambda update-function-configuration \
    --function-name sftp-to-s3-transfer \
    --environment Variables="{S3_BUCKET_NAME=my-bucket,SFTP_HOST=example.com}"
```

#### 8. Secrets Manager Access Issues

**Problem:** Cannot retrieve credentials from Secrets Manager

**Solutions:**

1. **Check secret exists:**
```bash
aws secretsmanager describe-secret --secret-id sftp-credentials
```

2. **Verify IAM permissions:**
```bash
aws iam attach-role-policy \
    --role-name lambda-sftp-s3-role \
    --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite
```

3. **Test secret retrieval:**
```bash
aws secretsmanager get-secret-value --secret-id sftp-credentials
```

### Test Issues

#### 9. Tests Failing

**Problem:** Unit or integration tests fail

**Solutions:**

1. **Run tests verbosely:**
```bash
python -m pytest tests/unit/test_s3_client.py -v -s
```

2. **Check test dependencies:**
```bash
pip install pytest pytest-cov moto
```

3. **Clear pytest cache:**
```bash
rm -rf .pytest_cache
```

4. **Run specific test:**
```bash
python -m pytest tests/unit/test_s3_client.py::TestS3Client::test_upload_file_success -v
```

#### 10. Mock Issues

**Problem:** Mocks not working as expected

**Solutions:**

1. **Check mock path:**
```python
# Correct
@patch('src.utils.s3_client.boto3.client')

# Incorrect
@patch('boto3.client')
```

2. **Verify mock is being called:**
```python
mock_client.upload_fileobj.assert_called_once()
```

3. **Reset mocks between tests:**
```python
def setUp(self):
    self.mock.reset_mock()
```

### Performance Issues

#### 11. Slow File Transfers

**Problem:** File transfers are slower than expected

**Solutions:**

1. **Check file size and Lambda memory:**
```bash
aws lambda update-function-configuration \
    --function-name sftp-to-s3-transfer \
    --memory-size 1024
```

2. **Enable S3 Transfer Acceleration:**
```bash
aws s3api put-bucket-accelerate-configuration \
    --bucket your-bucket \
    --accelerate-configuration Status=Enabled
```

3. **Use multipart upload for large files**
4. **Monitor network latency**
5. **Consider regional proximity**

#### 12. High Lambda Costs

**Problem:** Lambda costs are higher than expected

**Solutions:**

1. **Optimize memory allocation:**
   - Test different memory sizes
   - Monitor execution time vs cost

2. **Reduce execution time:**
   - Optimize code
   - Use connection pooling
   - Batch operations

3. **Use scheduled execution instead of continuous polling**

4. **Set up cost alerts:**
```bash
aws cloudwatch put-metric-alarm \
    --alarm-name lambda-cost-alert \
    --metric-name EstimatedCharges \
    --namespace AWS/Billing
```

## Debugging Tips

### Enable Debug Logging

```bash
export LOG_LEVEL=DEBUG
```

Or in Lambda:
```bash
aws lambda update-function-configuration \
    --function-name sftp-to-s3-transfer \
    --environment Variables="{LOG_LEVEL=DEBUG}"
```

### View Lambda Logs

```bash
# Tail logs
aws logs tail /aws/lambda/sftp-to-s3-transfer --follow

# Get specific log stream
aws logs get-log-events \
    --log-group-name /aws/lambda/sftp-to-s3-transfer \
    --log-stream-name 2024/01/01/[$LATEST]xxxxx
```

### Enable X-Ray Tracing

```bash
aws lambda update-function-configuration \
    --function-name sftp-to-s3-transfer \
    --tracing-config Mode=Active
```

### Test Lambda Locally

```bash
# Using SAM CLI
sam local invoke sftp-to-s3-transfer -e examples/test-event.json

# Using Python directly
python -c "
from src.lambda.handler import lambda_handler
import json
with open('examples/test-event.json') as f:
    event = json.load(f)
print(lambda_handler(event, None))
"
```

## Getting Additional Help

1. **Check CloudWatch Logs** - Most errors are logged
2. **Review AWS CloudTrail** - For API call issues
3. **Enable VPC Flow Logs** - For network issues
4. **Use AWS X-Ray** - For performance analysis
5. **Check GitHub Issues** - Community solutions
6. **AWS Support** - For AWS-specific issues

## Common Error Messages

### "No module named 'src'"
- Add project to PYTHONPATH
- Ensure running from project root

### "Access Denied" (S3)
- Check IAM policies
- Verify bucket policy
- Check VPC endpoint policy

### "Connection timeout" (SFTP)
- Verify SFTP server is accessible
- Check security group rules
- Verify network connectivity

### "Task timed out"
- Increase Lambda timeout
- Check VPC Gateway Endpoint
- Verify route table configuration

### "Unable to import module 'src.lambda.handler'"
- Verify Lambda package structure
- Check handler path is correct
- Ensure dependencies are included
