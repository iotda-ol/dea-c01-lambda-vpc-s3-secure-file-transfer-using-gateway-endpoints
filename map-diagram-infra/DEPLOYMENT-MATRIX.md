# Multi-Cloud Deployment Matrix

This guide provides step-by-step deployment instructions for deploying the Secure File Transfer architecture on AWS, GCP, and Azure.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [AWS Deployment](#aws-deployment)
3. [GCP Deployment](#gcp-deployment)
4. [Azure Deployment](#azure-deployment)
5. [Post-Deployment Configuration](#post-deployment-configuration)
6. [Testing & Validation](#testing--validation)
7. [Migration Guide](#migration-guide)

---

## Prerequisites

### General Requirements (All Clouds)

- [ ] Active cloud provider account with billing enabled
- [ ] Admin or sufficient IAM permissions
- [ ] Terraform >= 1.0 installed
- [ ] Git installed
- [ ] Python >= 3.11 installed
- [ ] SFTP server credentials available
- [ ] Basic understanding of VPC/networking concepts

### Cloud-Specific CLI Tools

#### AWS
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region, Output format
```

#### GCP
```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Authenticate
gcloud auth login
gcloud auth application-default login

# Set project
gcloud config set project YOUR_PROJECT_ID
```

#### Azure
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login

# Set subscription
az account set --subscription YOUR_SUBSCRIPTION_ID
```

---

## AWS Deployment

### Step 1: Clone Repository

```bash
git clone https://github.com/your-org/secure-file-transfer.git
cd secure-file-transfer/terraform/aws
```

### Step 2: Configure Variables

Create `terraform.tfvars`:

```hcl
# terraform.tfvars for AWS

# General
project_name = "file-transfer"
environment  = "dev"
aws_region   = "us-east-1"

# VPC Configuration
vpc_cidr             = "10.0.0.0/16"
private_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
availability_zones   = ["us-east-1a", "us-east-1b"]

# Lambda Configuration
lambda_runtime     = "python3.11"
lambda_memory_size = 512
lambda_timeout     = 300

# SFTP Configuration (will be stored in Secrets Manager)
sftp_host        = "sftp.example.com"
sftp_port        = 22
sftp_remote_path = "/incoming/files"

# Scheduling
lambda_schedule_enabled    = true
lambda_schedule_expression = "rate(1 hour)"

# Tags
tags = {
  Project     = "SecureFileTransfer"
  Environment = "dev"
  ManagedBy   = "Terraform"
  CostCenter  = "DataEngineering"
}
```

### Step 3: Initialize Terraform

```bash
terraform init
```

### Step 4: Plan Deployment

```bash
terraform plan -out=tfplan
```

**Review the plan to ensure:**
- VPC and 2 private subnets will be created
- S3 bucket with versioning and lifecycle policies
- VPC Gateway Endpoint (FREE) for S3
- Lambda function with VPC configuration
- IAM roles with least privilege policies
- Secrets Manager secret
- CloudWatch log group

### Step 5: Deploy Infrastructure

```bash
terraform apply tfplan
```

**Expected deployment time:** 3-5 minutes

### Step 6: Store SFTP Credentials

```bash
# Get the secret ARN
SECRET_ARN=$(terraform output -raw sftp_secret_arn)

# Update with actual credentials
aws secretsmanager put-secret-value \
  --secret-id $SECRET_ARN \
  --secret-string '{
    "username": "your-sftp-username",
    "password": "your-sftp-password",
    "host": "sftp.example.com",
    "port": 22
  }'
```

### Step 7: Deploy Lambda Code

```bash
# Package Lambda function
cd ../../lambda
zip -r ../terraform/aws/lambda_function.zip .

# Update Lambda function
cd ../terraform/aws
aws lambda update-function-code \
  --function-name $(terraform output -raw lambda_function_name) \
  --zip-file fileb://lambda_function.zip
```

### Step 8: Test Deployment

```bash
# Invoke Lambda function
aws lambda invoke \
  --function-name $(terraform output -raw lambda_function_name) \
  --payload '{"test": true}' \
  response.json

# Check response
cat response.json

# View logs
aws logs tail $(terraform output -raw cloudwatch_log_group) --follow
```

### AWS Cost Breakdown

| Component | Monthly Cost | Note |
|-----------|--------------|------|
| Lambda (1K invocations) | $0.25 | Pay per execution |
| S3 (100GB with lifecycle) | $2.30 | With tiering |
| VPC Gateway Endpoint | **$0.00** | FREE! |
| Secrets Manager | $0.40 | Per secret |
| CloudWatch Logs | $0.50 | 7-day retention |
| **Total** | **$3.45** | **Very cost-effective** |

---

## GCP Deployment

### Step 1: Enable Required APIs

```bash
gcloud services enable \
  cloudfunctions.googleapis.com \
  cloudscheduler.googleapis.com \
  secretmanager.googleapis.com \
  storage-api.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com
```

### Step 2: Clone Repository

```bash
git clone https://github.com/your-org/secure-file-transfer.git
cd secure-file-transfer/terraform/gcp
```

### Step 3: Configure Variables

Create `terraform.tfvars`:

```hcl
# terraform.tfvars for GCP

# General
project_id   = "your-gcp-project-id"
project_name = "file-transfer"
environment  = "dev"
region       = "us-central1"

# VPC Configuration
vpc_cidr        = "10.0.0.0/16"
subnet_cidr     = "10.0.1.0/24"

# Cloud Function Configuration
function_runtime     = "python311"
function_memory      = "512Mi"
function_timeout     = "300s"
function_entry_point = "file_transfer_handler"

# SFTP Configuration
sftp_host        = "sftp.example.com"
sftp_port        = 22
sftp_remote_path = "/incoming/files"

# Scheduling
scheduler_enabled  = true
scheduler_schedule = "0 * * * *"  # Every hour
scheduler_timezone = "UTC"

# Labels
labels = {
  project     = "secure-file-transfer"
  environment = "dev"
  managed_by  = "terraform"
}
```

### Step 4: Initialize Terraform

```bash
terraform init
```

### Step 5: Plan Deployment

```bash
terraform plan -out=tfplan
```

**Review the plan to ensure:**
- VPC with custom subnet
- Cloud Storage bucket with lifecycle policies
- VPC Connector for Cloud Functions
- Cloud Function (2nd gen) with VPC connector
- Service Account with IAM bindings
- Secret Manager secret
- Cloud Scheduler job

### Step 6: Deploy Infrastructure

```bash
terraform apply tfplan
```

**Expected deployment time:** 5-7 minutes (VPC Connector takes longer)

### Step 7: Store SFTP Credentials

```bash
# Create secret version
gcloud secrets versions add $(terraform output -raw secret_id) \
  --data-file=- <<EOF
{
  "username": "your-sftp-username",
  "password": "your-sftp-password",
  "host": "sftp.example.com",
  "port": 22
}
EOF
```

### Step 8: Deploy Function Code

```bash
# Package and deploy function
cd ../../lambda
gcloud functions deploy $(terraform output -raw function_name) \
  --gen2 \
  --runtime=python311 \
  --region=$(terraform output -raw region) \
  --source=. \
  --entry-point=file_transfer_handler \
  --trigger-http \
  --vpc-connector=$(terraform output -raw vpc_connector_name)
```

### Step 9: Test Deployment

```bash
# Invoke function
gcloud functions call $(terraform output -raw function_name) \
  --region=$(terraform output -raw region) \
  --data='{"test": true}'

# View logs
gcloud functions logs read $(terraform output -raw function_name) \
  --region=$(terraform output -raw region) \
  --limit=50
```

### GCP Cost Breakdown

| Component | Monthly Cost | Note |
|-----------|--------------|------|
| Cloud Functions (1K invocations) | $0.40 | Pay per execution |
| Cloud Storage (100GB) | $2.00 | With tiering |
| Private Google Access | **$0.00** | FREE! |
| Secret Manager | $0.06 | Cheapest! |
| Cloud Logging | **$0.00** | 50GB free tier |
| VPC Connector | ~$0.10 | Minimal usage |
| **Total** | **$2.46** | **Most cost-effective** |

---

## Azure Deployment

### Step 1: Create Resource Group

```bash
az group create \
  --name rg-file-transfer-dev \
  --location eastus
```

### Step 2: Clone Repository

```bash
git clone https://github.com/your-org/secure-file-transfer.git
cd secure-file-transfer/terraform/azure
```

### Step 3: Configure Variables

Create `terraform.tfvars`:

```hcl
# terraform.tfvars for Azure

# General
project_name        = "file-transfer"
environment         = "dev"
location            = "eastus"
resource_group_name = "rg-file-transfer-dev"

# VNet Configuration
vnet_address_space = ["10.0.0.0/16"]
subnet_address_prefix = "10.0.1.0/24"

# Function App Configuration
function_runtime         = "python"
function_runtime_version = "3.11"
function_timeout         = 300

# SFTP Configuration
sftp_host        = "sftp.example.com"
sftp_port        = 22
sftp_remote_path = "/incoming/files"

# Scheduling
timer_schedule = "0 0 * * * *"  # Every hour

# Tags
tags = {
  Project     = "SecureFileTransfer"
  Environment = "dev"
  ManagedBy   = "Terraform"
}
```

### Step 4: Initialize Terraform

```bash
terraform init
```

### Step 5: Plan Deployment

```bash
terraform plan -out=tfplan
```

**Review the plan to ensure:**
- Virtual Network with subnet
- Storage Account with blob container
- Private Endpoint for Blob Storage
- Function App with VNet integration
- Managed Identity
- Key Vault with secrets
- Application Insights

### Step 6: Deploy Infrastructure

```bash
terraform apply tfplan
```

**Expected deployment time:** 8-10 minutes

### Step 7: Store SFTP Credentials

```bash
# Get Key Vault name
VAULT_NAME=$(terraform output -raw key_vault_name)

# Store credentials as separate secrets
az keyvault secret set \
  --vault-name $VAULT_NAME \
  --name sftp-credentials \
  --value '{
    "username": "your-sftp-username",
    "password": "your-sftp-password",
    "host": "sftp.example.com",
    "port": 22
  }'
```

### Step 8: Deploy Function Code

```bash
# Create deployment package
cd ../../lambda
zip -r ../terraform/azure/function.zip .

# Deploy to Function App
cd ../terraform/azure
FUNCTION_APP=$(terraform output -raw function_app_name)

az functionapp deployment source config-zip \
  --resource-group rg-file-transfer-dev \
  --name $FUNCTION_APP \
  --src function.zip
```

### Step 9: Test Deployment

```bash
# Invoke function (via HTTP trigger)
FUNCTION_URL=$(az functionapp function show \
  --resource-group rg-file-transfer-dev \
  --name $FUNCTION_APP \
  --function-name FileTransfer \
  --query "invokeUrlTemplate" -o tsv)

curl -X POST $FUNCTION_URL -d '{"test": true}'

# View logs
az monitor app-insights query \
  --app $(terraform output -raw application_insights_id) \
  --analytics-query "traces | where timestamp > ago(1h) | order by timestamp desc | limit 50"
```

### Azure Cost Breakdown

| Component | Monthly Cost | Note |
|-----------|--------------|------|
| Function App (1K executions) | $0.20 | Consumption plan |
| Blob Storage (100GB) | $2.05 | With tiering |
| Private Endpoint | **$7.20** | Expensive! |
| Key Vault | $0.03 | Per secret |
| Application Insights | $2.30 | Log ingestion |
| **Total** | **$11.78** | **Most expensive** |

---

## Post-Deployment Configuration

### 1. Configure SFTP Firewall Rules

If your SFTP server has IP allowlisting, add cloud provider NAT IPs:

#### AWS
```bash
# Lambda functions use NAT Gateway IPs for internet access
# Get NAT Gateway Elastic IPs
aws ec2 describe-nat-gateways \
  --filter "Name=vpc-id,Values=$(terraform output -raw vpc_id)" \
  --query 'NatGateways[*].NatGatewayAddresses[*].PublicIp' \
  --output text
```

#### GCP
```bash
# Cloud Functions use Cloud NAT for egress
# Get Cloud NAT external IPs
gcloud compute routers nats describe cloud-nat \
  --router=cloud-router \
  --region=us-central1 \
  --format="value(natIps)"
```

#### Azure
```bash
# Function App uses outbound IPs
az functionapp show \
  --resource-group rg-file-transfer-dev \
  --name $(terraform output -raw function_app_name) \
  --query "possibleOutboundIpAddresses" \
  --output tsv
```

### 2. Configure Monitoring Alerts

#### AWS
```bash
# Create SNS topic for alerts
aws sns create-topic --name file-transfer-alerts

# Subscribe to topic
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:ACCOUNT:file-transfer-alerts \
  --protocol email \
  --notification-endpoint your-email@example.com
```

#### GCP
```bash
# Create notification channel
gcloud alpha monitoring channels create \
  --display-name="File Transfer Alerts" \
  --type=email \
  --channel-labels=email_address=your-email@example.com
```

#### Azure
```bash
# Create action group
az monitor action-group create \
  --resource-group rg-file-transfer-dev \
  --name file-transfer-alerts \
  --short-name ft-alerts \
  --email-receiver name=admin email=your-email@example.com
```

### 3. Test End-to-End Transfer

Create a test file on your SFTP server and trigger the function:

#### AWS
```bash
aws lambda invoke \
  --function-name $(terraform output -raw lambda_function_name) \
  --payload '{"remote_path": "/test/sample.txt"}' \
  response.json
```

#### GCP
```bash
gcloud functions call $(terraform output -raw function_name) \
  --region=$(terraform output -raw region) \
  --data='{"remote_path": "/test/sample.txt"}'
```

#### Azure
```bash
# Trigger via HTTP
curl -X POST "https://${FUNCTION_APP}.azurewebsites.net/api/FileTransfer" \
  -H "Content-Type: application/json" \
  -d '{"remote_path": "/test/sample.txt"}'
```

---

## Testing & Validation

### Validation Checklist

- [ ] Function can connect to SFTP server
- [ ] Function can retrieve credentials from secret manager
- [ ] Function can download files from SFTP
- [ ] Function can upload files to object storage via private endpoint
- [ ] Files are encrypted at rest in storage
- [ ] Lifecycle policies are applied to storage
- [ ] Logs are visible in centralized logging
- [ ] Metrics are being collected
- [ ] Alerts are configured and working
- [ ] Scheduler is triggering function on schedule
- [ ] VPC/VNet isolation is working (no internet for storage)

### Performance Testing

```bash
# Test with various file sizes
for size in 1M 10M 100M; do
  echo "Testing with ${size} file..."
  # Create test file
  dd if=/dev/urandom of=test_${size}.dat bs=1M count=${size%M}
  # Upload to SFTP
  # Trigger function
  # Measure duration
done
```

### Cost Monitoring

#### AWS
```bash
# View cost by service
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '30 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

#### GCP
```bash
# View billing for project
gcloud billing projects describe YOUR_PROJECT_ID
```

#### Azure
```bash
# View cost analysis
az consumption usage list \
  --start-date $(date -d '30 days ago' +%Y-%m-%d) \
  --end-date $(date +%Y-%m-%d)
```

---

## Migration Guide

### AWS → GCP

1. Export SFTP credentials from AWS Secrets Manager
2. Create GCP Secret Manager secret with same data
3. Deploy GCP infrastructure
4. Update DNS/firewall rules if needed
5. Test GCP deployment
6. Switch scheduler/trigger to GCP
7. Monitor for 24-48 hours
8. Decommission AWS resources

**Cost Impact**: Save ~29% ($3.45 → $2.46)

### AWS → Azure

1. Export SFTP credentials from AWS Secrets Manager
2. Create Azure Key Vault secret with same data
3. Deploy Azure infrastructure
4. Update DNS/firewall rules if needed
5. Test Azure deployment
6. Switch scheduler/trigger to Azure
7. Monitor for 24-48 hours
8. Decommission AWS resources

**Cost Impact**: Increase ~241% ($3.45 → $11.78) due to Private Endpoint costs

### GCP → Azure

1. Export secrets from GCP Secret Manager
2. Create Azure Key Vault secret
3. Deploy Azure infrastructure
4. Update DNS/firewall rules
5. Test Azure deployment
6. Switch scheduler to Azure
7. Monitor for 24-48 hours
8. Decommission GCP resources

**Cost Impact**: Increase ~379% ($2.46 → $11.78)

---

## Troubleshooting

### Common Issues

#### Issue: Function times out connecting to S3/Storage
**Solution**: Verify VPC Gateway Endpoint / Private Endpoint is attached to route table

#### Issue: Function cannot retrieve secrets
**Solution**: Check IAM permissions for secret access

#### Issue: SFTP connection refused
**Solution**: Check security group egress rules allow port 22

#### Issue: High costs
**Solution**: 
- Review storage lifecycle policies
- Check function timeout (reduce if possible)
- Review log retention (reduce to 7 days)
- For Azure, consider using Storage Service Endpoint instead of Private Endpoint

---

## Summary

### Best Choice by Criteria

| Criteria | Winner | Reason |
|----------|--------|--------|
| **Lowest Cost** | **GCP** | $2.46/month (29% cheaper than AWS) |
| **Best Features** | **AWS** | FREE S3 Gateway Endpoint, mature VPC |
| **Simplest Deployment** | **GCP** | Fewer components, automatic logging |
| **Enterprise Integration** | **Azure** | Best if already in Microsoft ecosystem |

### Recommendation

- **Choose AWS** if you need the most mature VPC integration and FREE private storage access
- **Choose GCP** if cost is the primary concern and you want simplicity
- **Choose Azure** if you're already invested in Microsoft ecosystem (despite higher costs)

For most use cases, **AWS offers the best balance** of features and cost, with the FREE S3 Gateway Endpoint being a major advantage.
