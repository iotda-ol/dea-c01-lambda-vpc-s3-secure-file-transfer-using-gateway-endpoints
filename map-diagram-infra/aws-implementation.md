# AWS Implementation Guide

## Overview

This guide provides step-by-step instructions for deploying the secure file transfer architecture on Amazon Web Services (AWS).

---

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI v2.x installed and configured
- Terraform >= 1.0
- Python >= 3.11
- Git

---

## Architecture Components (AWS-Specific)

| Component | AWS Service | Notes |
|-----------|-------------|-------|
| Virtual Network | Amazon VPC | CIDR: 10.0.0.0/16 |
| Serverless Compute | AWS Lambda | Python 3.11 runtime |
| Object Storage | Amazon S3 | With versioning & lifecycle |
| Private Endpoint | VPC Gateway Endpoint | **FREE for S3** |
| Secrets Vault | AWS Secrets Manager | $0.40/secret/month |
| IAM | AWS IAM | Roles and policies |
| Logging | CloudWatch Logs | 7-day retention |
| Monitoring | CloudWatch Metrics | Standard metrics |
| Scheduler | Amazon EventBridge | Cron-based rules |
| Network Security | Security Groups | Stateful firewall |

---

## Deployment Steps

### Step 1: Clone Repository

```bash
git clone https://github.com/iotda-ol/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints.git
cd dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints
```

### Step 2: Configure AWS CLI

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter default region (e.g., us-east-1)
# Enter output format (json recommended)

# Verify configuration
aws sts get-caller-identity
```

### Step 3: Set Up Terraform Backend (Optional but Recommended)

```bash
# Create S3 bucket for Terraform state
aws s3 mb s3://my-terraform-state-bucket --region us-east-1

# Create DynamoDB table for state locking
aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1

# Update terraform/main.tf backend configuration
```

```hcl
# terraform/main.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "file-transfer/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

### Step 4: Package Lambda Function

```bash
chmod +x scripts/deployment/package-lambda.sh
./scripts/deployment/package-lambda.sh

# This creates lambda_function.zip in the terraform directory
```

### Step 5: Configure Terraform Variables

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars
nano terraform.tfvars
```

**terraform.tfvars**:
```hcl
# Project Configuration
project_name = "secure-transfer"
environment  = "dev"
aws_region   = "us-east-1"

# VPC Configuration
vpc_cidr             = "10.0.0.0/16"
private_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
availability_zones   = ["us-east-1a", "us-east-1b"]

# SFTP Configuration
sftp_host        = "sftp.example.com"
sftp_port        = 22
sftp_username    = "transfer_user"
sftp_remote_path = "/incoming"

# Lambda Configuration
lambda_schedule_enabled    = true
lambda_schedule_expression = "cron(0 2 * * ? *)"  # Daily at 2 AM UTC

# Tags
tags = {
  Project     = "SecureFileTransfer"
  Environment = "dev"
  ManagedBy   = "Terraform"
  CostCenter  = "DataEngineering"
}
```

### Step 6: Initialize Terraform

```bash
terraform init
# Downloads AWS provider
# Configures backend
# Initializes modules
```

### Step 7: Review Infrastructure Plan

```bash
terraform plan -out=tfplan

# Review the plan output
# Verify all resources to be created
# Check for any errors
```

Expected resources:
- 1 VPC
- 2 Private Subnets
- 1 Route Table
- 1 VPC Gateway Endpoint (S3)
- 1 Security Group
- 1 S3 Bucket
- 1 Lambda Function
- 1 IAM Role + 4 IAM Policies
- 1 Secrets Manager Secret
- 1 CloudWatch Log Group
- 1 EventBridge Rule
- 1 Lambda Permission

### Step 8: Deploy Infrastructure

```bash
terraform apply tfplan
# Review and confirm deployment
# Deployment takes 2-3 minutes
```

### Step 9: Configure SFTP Credentials

```bash
# Get the secret ARN from Terraform outputs
SECRET_ARN=$(terraform output -raw sftp_secret_arn)

# Update the secret with actual SFTP credentials
# Option 1: Password authentication
aws secretsmanager put-secret-value \
  --secret-id $SECRET_ARN \
  --secret-string '{
    "username": "your-sftp-username",
    "password": "your-sftp-password",
    "host": "sftp.example.com",
    "port": 22
  }'

# Option 2: SSH key authentication
aws secretsmanager put-secret-value \
  --secret-id $SECRET_ARN \
  --secret-string '{
    "username": "your-sftp-username",
    "private_key": "-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----",
    "host": "sftp.example.com",
    "port": 22
  }'
```

### Step 10: Test Lambda Function

```bash
# Get Lambda function name
LAMBDA_NAME=$(terraform output -raw lambda_function_name)

# Invoke function manually
aws lambda invoke \
  --function-name $LAMBDA_NAME \
  --payload '{"test": true}' \
  response.json

# View response
cat response.json

# View logs
LOG_GROUP=$(terraform output -raw cloudwatch_log_group)
aws logs tail $LOG_GROUP --follow
```

### Step 11: Verify S3 Upload

```bash
# Get S3 bucket name
BUCKET_NAME=$(terraform output -raw s3_bucket_name)

# List uploaded files
aws s3 ls s3://$BUCKET_NAME/ --recursive

# Download a file for verification (optional)
aws s3 cp s3://$BUCKET_NAME/path/to/file.txt ./downloaded-file.txt
```

---

## Terraform Outputs Reference

After deployment, Terraform provides these outputs:

```bash
# View all outputs
terraform output

# Specific outputs
terraform output lambda_function_name
terraform output lambda_function_arn
terraform output s3_bucket_name
terraform output s3_bucket_arn
terraform output sftp_secret_arn
terraform output cloudwatch_log_group
terraform output vpc_id
terraform output private_subnet_ids
terraform output security_group_id
terraform output s3_gateway_endpoint_id
```

---

## Monitoring & Operations

### View Lambda Logs

```bash
# Tail logs in real-time
aws logs tail /aws/lambda/secure-transfer-dev-file-transfer --follow

# Get specific log streams
aws logs describe-log-streams \
  --log-group-name /aws/lambda/secure-transfer-dev-file-transfer \
  --order-by LastEventTime \
  --descending

# Query logs with CloudWatch Insights
aws logs start-query \
  --log-group-name /aws/lambda/secure-transfer-dev-file-transfer \
  --start-time $(date -u -d '1 hour ago' +%s) \
  --end-time $(date +%s) \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/'
```

### View Lambda Metrics

```bash
# Get invocation count
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=secure-transfer-dev-file-transfer \
  --start-time $(date -u -d '1 day ago' --iso-8601) \
  --end-time $(date -u --iso-8601) \
  --period 3600 \
  --statistics Sum

# Get error count
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=secure-transfer-dev-file-transfer \
  --start-time $(date -u -d '1 day ago' --iso-8601) \
  --end-time $(date -u --iso-8601) \
  --period 3600 \
  --statistics Sum
```

### Create CloudWatch Alarms

```bash
# Error rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name secure-transfer-lambda-errors \
  --alarm-description "Alert on Lambda function errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 1 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=FunctionName,Value=secure-transfer-dev-file-transfer
```

---

## Cost Management

### View Current Costs

```bash
# Get cost for the last 30 days
aws ce get-cost-and-usage \
  --time-period Start=$(date -u -d '30 days ago' +%Y-%m-%d),End=$(date -u +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "BlendedCost" \
  --filter file://filter.json

# filter.json
{
  "Tags": {
    "Key": "Project",
    "Values": ["SecureFileTransfer"]
  }
}
```

### Enable Cost Allocation Tags

```bash
# Activate cost allocation tags
aws ce update-cost-allocation-tags-status \
  --cost-allocation-tags-status TagKey=Project,Status=Active \
  --cost-allocation-tags-status TagKey=Environment,Status=Active
```

---

## Maintenance

### Update Lambda Code

```bash
# Update Lambda function code
cd /path/to/project
./scripts/deployment/package-lambda.sh

cd terraform
terraform apply -target=aws_lambda_function.file_transfer
```

### Rotate SFTP Credentials

```bash
# Update secret value
aws secretsmanager put-secret-value \
  --secret-id <secret-arn> \
  --secret-string '{"username":"new-user","password":"new-pass",...}'

# Test function with new credentials
aws lambda invoke --function-name <function-name> response.json
```

### Scale Function

```bash
# Update memory/timeout in terraform/variables.tf or terraform.tfvars
# Then apply changes
terraform apply
```

---

## Troubleshooting

### Issue: Lambda Times Out

**Symptom**: Function execution exceeds timeout

**Solution**:
1. Check VPC Gateway Endpoint is attached to route table
2. Verify security group allows HTTPS egress
3. Increase function timeout if needed

```bash
# Verify endpoint
aws ec2 describe-vpc-endpoints \
  --filters "Name=vpc-id,Values=<vpc-id>"

# Check route table associations
aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=<vpc-id>"
```

### Issue: Access Denied to S3

**Symptom**: S3 PutObject operation fails

**Solution**:
1. Check IAM role has S3 permissions
2. Verify VPC endpoint policy allows operation
3. Check bucket policy

```bash
# List role policies
aws iam list-attached-role-policies \
  --role-name <lambda-role-name>

# Get policy document
aws iam get-policy-version \
  --policy-arn <policy-arn> \
  --version-id v1
```

### Issue: SFTP Connection Failed

**Symptom**: Cannot connect to SFTP server

**Solution**:
1. Verify SFTP credentials in Secrets Manager
2. Check security group allows SSH/SFTP egress (port 22)
3. Verify SFTP server is accessible from AWS

```bash
# Test from Lambda VPC (using EC2 in same VPC)
telnet sftp.example.com 22
```

---

## Cleanup

To destroy all resources:

```bash
cd terraform
terraform destroy

# Confirm destruction
# Type 'yes' when prompted
```

**Warning**: This will delete:
- All uploaded files in S3
- Lambda function and logs
- VPC and networking components
- Secrets (after 7-day recovery window)

---

## Security Hardening (Production)

### Enable S3 Bucket Encryption with KMS

```hcl
# terraform/s3.tf
resource "aws_kms_key" "s3" {
  description             = "KMS key for S3 bucket encryption"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "file_transfer" {
  bucket = aws_s3_bucket.file_transfer.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
    bucket_key_enabled = true
  }
}
```

### Enable VPC Flow Logs

```hcl
# terraform/vpc.tf
resource "aws_flow_log" "vpc" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  iam_role_arn    = aws_iam_role.vpc_flow_logs.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_logs.arn
}
```

### Enable AWS Config

```bash
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=<config-role-arn> \
  --recording-group allSupported=true,includeGlobalResourceTypes=true
```

---

## Additional Resources

- [AWS Lambda VPC Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html)
- [S3 VPC Gateway Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)
- [AWS Secrets Manager Best Practices](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

## Estimated Monthly Costs (AWS)

| Resource | Cost |
|----------|------|
| Lambda (1,000 invocations/month) | $0.25 |
| S3 Storage (100 GB) | $2.30 |
| S3 Requests (1,000 PUTs) | $0.01 |
| VPC Gateway Endpoint (S3) | **$0.00** |
| Secrets Manager | $0.40 |
| CloudWatch Logs (1 GB) | $0.50 |
| **Total** | **~$3.46/month** |

**Savings vs EC2 + NAT Gateway**: ~$65/month (95% reduction)
