# Deployment Guide

## Prerequisites

### Required Tools
- **Terraform**: >= 1.0 ([Installation Guide](https://learn.hashicorp.com/tutorials/terraform/install-cli))
- **AWS CLI**: >= 2.0 ([Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
- **Python**: >= 3.11 ([Installation Guide](https://www.python.org/downloads/))
- **pip**: Python package installer
- **zip**: For creating Lambda deployment packages
- **bash**: For running deployment scripts

### AWS Account Requirements
- Active AWS account with appropriate permissions
- AWS CLI configured with credentials (`aws configure`)
- IAM permissions to create:
  - VPC resources (VPC, subnets, route tables, security groups)
  - S3 buckets and endpoints
  - Lambda functions
  - IAM roles and policies
  - Secrets Manager secrets
  - CloudWatch log groups
  - EventBridge rules

### Verify Prerequisites
```bash
# Check Terraform version
terraform version

# Check AWS CLI version
aws --version

# Check Python version
python3 --version

# Verify AWS credentials
aws sts get-caller-identity
```

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/iotda-ol/dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints.git
cd dea-c01-lambda-vpc-s3-secure-file-transfer-using-gateway-endpoints
```

### 2. Configure Variables
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your values:
```hcl
aws_region = "us-east-1"
project_name = "secure-file-transfer"
environment = "dev"

# SFTP Configuration
sftp_host = "your-sftp-server.com"
sftp_port = 22
sftp_username = "your-username"
sftp_remote_path = "/path/to/files"
```

### 3. Build Lambda Package
```bash
cd ..
bash scripts/build_lambda.sh
```

### 4. Deploy Infrastructure
```bash
bash scripts/deploy.sh
```

Or manually:
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### 5. Update SFTP Credentials
After deployment, update the Secrets Manager secret with actual credentials:

```bash
# Get secret ARN from Terraform output
SECRET_ARN=$(terraform output -raw sftp_secret_arn)

# Update with password authentication
aws secretsmanager put-secret-value \
  --secret-id $SECRET_ARN \
  --secret-string '{
    "username": "your-username",
    "password": "your-password",
    "host": "sftp.example.com",
    "port": 22
  }'

# Or update with private key authentication
aws secretsmanager put-secret-value \
  --secret-id $SECRET_ARN \
  --secret-string '{
    "username": "your-username",
    "private_key": "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----",
    "host": "sftp.example.com",
    "port": 22
  }'
```

## Detailed Deployment Steps

### Step 1: Build Lambda Deployment Package

The Lambda function requires Python dependencies that must be packaged together:

```bash
cd lambda

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create deployment package
cd ..
mkdir -p build
pip install -r lambda/requirements.txt -t build/
cp lambda/lambda_function.py build/
cd build
zip -r ../lambda_function.zip .
cd ..
```

**Result**: `lambda_function.zip` file in project root

### Step 2: Initialize Terraform

```bash
cd terraform
terraform init
```

This will:
- Download required provider plugins (AWS)
- Initialize backend configuration
- Create `.terraform` directory

### Step 3: Review and Customize Configuration

**Review variables.tf:**
- Adjust default values if needed
- Customize CIDR blocks for VPC and subnets
- Set appropriate region and availability zones

**Review IAM policies:**
- Confirm least-privilege permissions
- Adjust based on organizational requirements

**Review S3 lifecycle policies:**
- Customize transition periods
- Adjust based on data retention requirements

### Step 4: Plan Deployment

```bash
terraform plan -out=tfplan
```

Review the plan carefully:
- Verify resource counts
- Check resource names and tags
- Confirm network configuration
- Validate IAM policies

### Step 5: Apply Configuration

```bash
terraform apply tfplan
```

**Deployment Time**: Approximately 3-5 minutes

Resources created:
- 1 VPC
- 2 Private subnets
- 1 Route table
- 1 S3 Gateway Endpoint
- 1 S3 bucket
- 1 Lambda function
- 1 Security group
- 4 IAM policies
- 1 IAM role
- 1 Secrets Manager secret
- 1 CloudWatch log group
- 1 EventBridge rule (disabled)

### Step 6: Capture Outputs

```bash
# View all outputs
terraform output

# Get specific values
terraform output s3_bucket_name
terraform output lambda_function_name
terraform output sftp_secret_arn
```

Save important values:
```bash
# Export for later use
export S3_BUCKET_NAME=$(terraform output -raw s3_bucket_name)
export LAMBDA_FUNCTION_NAME=$(terraform output -raw lambda_function_name)
export SECRET_ARN=$(terraform output -raw sftp_secret_arn)
```

## Post-Deployment Configuration

### 1. Update SFTP Credentials

See Quick Start Step 5 above.

### 2. Test Lambda Function

**Manual Test:**
```bash
aws lambda invoke \
  --function-name $LAMBDA_FUNCTION_NAME \
  --payload '{}' \
  response.json

cat response.json
```

**View Logs:**
```bash
# Get log group name
LOG_GROUP=$(terraform output -raw cloudwatch_log_group)

# View recent logs
aws logs tail $LOG_GROUP --follow
```

### 3. Enable Scheduled Execution (Optional)

```bash
# Enable EventBridge rule
aws events enable-rule \
  --name secure-file-transfer-dev-file-transfer-schedule

# Adjust schedule if needed
aws events put-rule \
  --name secure-file-transfer-dev-file-transfer-schedule \
  --schedule-expression "rate(1 hour)"
```

### 4. Configure CloudWatch Alarms

**Lambda Error Alarm:**
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "lambda-file-transfer-errors" \
  --alarm-description "Alert on Lambda function errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 1 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=FunctionName,Value=$LAMBDA_FUNCTION_NAME
```

## Verification

### 1. Verify VPC Configuration

```bash
# Get VPC ID
VPC_ID=$(terraform output -raw vpc_id)

# Check VPC endpoints
aws ec2 describe-vpc-endpoints \
  --filters "Name=vpc-id,Values=$VPC_ID"

# Verify route tables
aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=$VPC_ID"
```

### 2. Verify S3 Bucket Configuration

```bash
# Check encryption
aws s3api get-bucket-encryption --bucket $S3_BUCKET_NAME

# Check versioning
aws s3api get-bucket-versioning --bucket $S3_BUCKET_NAME

# Check public access block
aws s3api get-public-access-block --bucket $S3_BUCKET_NAME

# Check lifecycle configuration
aws s3api get-bucket-lifecycle-configuration --bucket $S3_BUCKET_NAME
```

### 3. Verify Lambda Configuration

```bash
# Get function configuration
aws lambda get-function-configuration \
  --function-name $LAMBDA_FUNCTION_NAME

# Check VPC configuration
aws lambda get-function-configuration \
  --function-name $LAMBDA_FUNCTION_NAME \
  --query 'VpcConfig'
```

### 4. Verify IAM Permissions

```bash
# Get Lambda role ARN
ROLE_ARN=$(terraform output -raw lambda_role_arn)

# List attached policies
aws iam list-attached-role-policies \
  --role-name $(echo $ROLE_ARN | cut -d'/' -f2)
```

## Troubleshooting

### Lambda Timeout Issues

**Problem**: Lambda times out connecting to SFTP or S3

**Solution**:
1. Verify VPC Gateway Endpoint is attached to route table
2. Check security group egress rules
3. Verify SFTP server is reachable from VPC
4. Increase Lambda timeout if needed

```bash
aws lambda update-function-configuration \
  --function-name $LAMBDA_FUNCTION_NAME \
  --timeout 600
```

### S3 Access Denied

**Problem**: Lambda cannot write to S3 bucket

**Solution**:
1. Verify IAM role has correct policies
2. Check S3 bucket policy
3. Verify VPC endpoint policy

```bash
# Test IAM permissions
aws iam simulate-principal-policy \
  --policy-source-arn $ROLE_ARN \
  --action-names s3:PutObject \
  --resource-arns "arn:aws:s3:::$S3_BUCKET_NAME/*"
```

### SFTP Connection Failed

**Problem**: Cannot connect to SFTP server

**Solution**:
1. Verify credentials in Secrets Manager
2. Check security group allows port 22 egress
3. Verify SFTP server hostname resolution
4. Check Lambda VPC configuration

```bash
# View CloudWatch Logs for details
aws logs tail $LOG_GROUP --follow --format short
```

### Secrets Manager Access Denied

**Problem**: Lambda cannot retrieve SFTP credentials

**Solution**:
1. Verify IAM policy allows secretsmanager:GetSecretValue
2. Check secret ARN is correct
3. Verify secret exists

```bash
aws secretsmanager describe-secret --secret-id $SECRET_ARN
```

## Updating the Deployment

### Update Lambda Code

```bash
# Make changes to lambda/lambda_function.py
# Rebuild package
bash scripts/build_lambda.sh

# Update Lambda function
cd terraform
terraform apply
```

### Update Infrastructure

```bash
# Make changes to Terraform files
cd terraform

# Review changes
terraform plan

# Apply changes
terraform apply
```

### Update Configuration

```bash
# Update terraform.tfvars
# Apply changes
cd terraform
terraform apply
```

## Cleanup

### Delete All Resources

```bash
cd terraform

# Preview deletion
terraform plan -destroy

# Delete resources
terraform destroy
```

**Note**: This will delete:
- All infrastructure resources
- S3 bucket (must be empty)
- Lambda function
- CloudWatch logs (after retention period)

**Before destroying:**
1. Backup any important data from S3
2. Save CloudWatch Logs if needed
3. Document any custom configurations

### Manual Cleanup (if needed)

If `terraform destroy` fails:

```bash
# Empty S3 bucket first
aws s3 rm s3://$S3_BUCKET_NAME --recursive

# Then retry
terraform destroy
```

## Security Considerations

### Secrets Management
- Never commit `terraform.tfvars` with sensitive data
- Use AWS Secrets Manager for SFTP credentials
- Rotate credentials regularly
- Enable audit logging with CloudTrail

### Network Security
- Lambda runs in private subnets only
- No public IPs assigned
- Security groups restrict traffic
- VPC endpoints keep traffic within AWS

### Access Control
- Use least-privilege IAM policies
- Enable MFA for AWS Console access
- Review IAM policies regularly
- Use AWS Organizations SCPs if applicable

## Cost Management

### Monitor Costs

```bash
# Check current month costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "1 day ago" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity DAILY \
  --metrics UnblendedCost \
  --filter file://cost-filter.json
```

### Set Up Budget Alerts

```bash
aws budgets create-budget \
  --account-id $(aws sts get-caller-identity --query Account --output text) \
  --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

## Next Steps

1. **Test file transfer functionality thoroughly**
2. **Set up monitoring and alerting**
3. **Document operational procedures**
4. **Train operators on the system**
5. **Plan for disaster recovery**
6. **Schedule regular security reviews**
7. **Optimize based on actual usage patterns**

## Support and Documentation

- **Architecture**: See [docs/ARCHITECTURE.md](ARCHITECTURE.md)
- **Security**: See [docs/SECURITY.md](SECURITY.md)
- **Cost Optimization**: See [docs/COST_OPTIMIZATION.md](COST_OPTIMIZATION.md)
- **AWS Lambda**: [AWS Documentation](https://docs.aws.amazon.com/lambda/)
- **Terraform AWS Provider**: [Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
