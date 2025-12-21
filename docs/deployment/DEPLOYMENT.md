# Deployment Guide

## Prerequisites

### Required Tools
- AWS CLI v2.x
- Terraform v1.0+
- Python 3.11+
- Git

### AWS Account Setup
1. AWS account with appropriate permissions
2. IAM user with programmatic access
3. MFA enabled (recommended)

### Required Permissions
The IAM user/role needs permissions for:
- VPC (create VPC, subnets, endpoints)
- EC2 (create security groups, manage ENIs)
- Lambda (create functions, manage configurations)
- S3 (create buckets, manage policies)
- IAM (create roles, attach policies)
- CloudWatch (create log groups, alarms)
- Secrets Manager (create secrets)

## Step 1: Clone Repository

```bash
git clone https://github.com/iotda-ol/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints.git
cd dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints
```

## Step 2: Configure AWS Credentials

```bash
aws configure
# Enter: Access Key ID
# Enter: Secret Access Key  
# Enter: Default region (e.g., us-east-1)
# Enter: Default output format (json)
```

Verify:
```bash
aws sts get-caller-identity
```

## Step 3: Create SFTP Credentials Secret

```bash
# Create secret in AWS Secrets Manager
aws secretsmanager create-secret \
  --name dev/sftp-credentials \
  --description "SFTP credentials for file transfer" \
  --secret-string '{
    "username": "your_sftp_username",
    "password": "your_sftp_password"
  }'

# Note the ARN from the output
```

## Step 4: Package Lambda Function

```bash
cd lambda

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create deployment package
cd src
zip -r ../../lambda_function.zip . -x "*.pyc" -x "__pycache__/*"
cd ../..

# Verify package
unzip -l lambda_function.zip
```

## Step 5: Configure Terraform Variables

```bash
cd terraform/environments/dev

# Copy example variables
cp terraform.tfvars.example terraform.tfvars

# Edit variables
nano terraform.tfvars
```

Update these critical values:
```hcl
s3_bucket_name   = "your-globally-unique-bucket-name"  # Must be unique!
sftp_host        = "your-sftp-server.com"
sftp_username    = "your_username"
sftp_secret_name = "dev/sftp-credentials"
sftp_secret_arn  = "arn:aws:secretsmanager:us-east-1:123456789012:secret:dev/sftp-credentials-AbCdEf"
```

## Step 6: Initialize Terraform

```bash
terraform init
```

Expected output:
```
Terraform has been successfully initialized!
```

## Step 7: Plan Deployment

```bash
terraform plan -out=tfplan
```

Review the plan carefully:
- VPC and subnets
- Security groups
- Gateway endpoint
- S3 bucket
- IAM role
- Lambda function

## Step 8: Deploy Infrastructure

```bash
terraform apply tfplan
```

Type `yes` when prompted.

Deployment takes ~5-10 minutes.

## Step 9: Verify Deployment

### Check VPC
```bash
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=secure-transfer-dev-vpc"
```

### Check S3 Bucket
```bash
aws s3 ls | grep secure-transfer
aws s3api get-bucket-encryption --bucket <your-bucket-name>
```

### Check Lambda Function
```bash
aws lambda get-function --function-name secure-transfer-dev-function
aws lambda get-function-configuration --function-name secure-transfer-dev-function
```

### Check Gateway Endpoint
```bash
aws ec2 describe-vpc-endpoints --filters "Name=vpc-id,Values=<vpc-id>"
```

## Step 10: Test Lambda Function

Create test event:
```bash
cat > test-event.json <<EOF
{
  "remote_file_path": "/path/to/file.txt",
  "s3_key": "test/file.txt",
  "metadata": {
    "source": "sftp",
    "environment": "dev"
  }
}
EOF
```

Invoke Lambda:
```bash
aws lambda invoke \
  --function-name secure-transfer-dev-function \
  --payload file://test-event.json \
  --cli-binary-format raw-in-base64-out \
  response.json

cat response.json
```

Check CloudWatch Logs:
```bash
aws logs tail /aws/lambda/secure-transfer-dev-function --follow
```

## Step 11: Verify File Transfer

```bash
# Check S3 for uploaded file
aws s3 ls s3://<your-bucket-name>/test/

# Download and verify
aws s3 cp s3://<your-bucket-name>/test/file.txt ./downloaded-file.txt
```

## Step 12: Set Up Monitoring (Optional)

### Create CloudWatch Dashboard
```bash
aws cloudwatch put-dashboard \
  --dashboard-name secure-transfer-dev \
  --dashboard-body file://../../docs/examples/dashboard.json
```

### Configure SNS for Alarms
```bash
aws sns create-topic --name lambda-alerts-dev
aws sns subscribe --topic-arn <topic-arn> --protocol email --notification-endpoint your-email@example.com
```

## Troubleshooting

### Issue: Lambda timeout
**Solution**: 
- Increase timeout in `terraform/environments/dev/variables.tf`
- Check SFTP server connectivity
- Verify file size is within limits

### Issue: S3 access denied
**Solution**:
- Verify IAM role has S3 permissions
- Check S3 bucket policy
- Verify VPC endpoint policy

### Issue: SFTP connection failed
**Solution**:
- Verify security group allows outbound port 22
- Check SFTP server is reachable
- Verify credentials in Secrets Manager

### Issue: Terraform apply fails
**Solution**:
- Check AWS credentials are valid
- Verify S3 bucket name is unique
- Review error message and adjust configuration

## Rolling Back

```bash
# Destroy infrastructure
cd terraform/environments/dev
terraform destroy

# Delete Lambda package
rm -f ../../../lambda_function.zip

# Delete S3 bucket (if needed)
aws s3 rb s3://<your-bucket-name> --force
```

## Next Steps

1. Review CloudWatch logs for any errors
2. Set up scheduled invocation with EventBridge
3. Configure S3 lifecycle policies
4. Enable VPC Flow Logs for troubleshooting
5. Document your specific SFTP configuration
6. Plan for production deployment

## Production Deployment

For production:
1. Use separate AWS account or VPC
2. Enable VPC Flow Logs
3. Use KMS for S3 encryption
4. Enable S3 access logging
5. Configure Terraform remote state
6. Set up CI/CD pipeline
7. Implement blue-green deployment
8. Configure backup and disaster recovery

See `terraform/environments/prod/` for production configuration.
