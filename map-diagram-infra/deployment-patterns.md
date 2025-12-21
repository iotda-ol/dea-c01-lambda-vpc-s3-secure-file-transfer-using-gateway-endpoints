# Deployment Patterns

Deployment architecture patterns for AWS, GCP, and Azure implementations of the secure file transfer solution.

## Table of Contents

1. [AWS Deployment Pattern](#aws-deployment-pattern)
2. [GCP Deployment Pattern](#gcp-deployment-pattern)
3. [Azure Deployment Pattern](#azure-deployment-pattern)
4. [Multi-Cloud Comparison](#multi-cloud-comparison)
5. [Environment Strategies](#environment-strategies)

---

## AWS Deployment Pattern

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS Account                              │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  VPC (10.0.0.0/16)                                         │ │
│  │                                                             │ │
│  │  ┌──────────────────────┐  ┌──────────────────────┐       │ │
│  │  │  us-east-1a          │  │  us-east-1b          │       │ │
│  │  │  Private Subnet      │  │  Private Subnet      │       │ │
│  │  │  10.0.1.0/24         │  │  10.0.2.0/24         │       │ │
│  │  │                      │  │                      │       │ │
│  │  │  ┌─────────────┐    │  │  ┌─────────────┐    │       │ │
│  │  │  │  Lambda     │    │  │  │  Lambda     │    │       │ │
│  │  │  │  (Warm)     │    │  │  │  (Standby)  │    │       │ │
│  │  │  └──────┬──────┘    │  │  └──────┬──────┘    │       │ │
│  │  │         │           │  │         │           │       │ │
│  │  │      ENI (10.0.1.x) │  │      ENI (10.0.2.x) │       │ │
│  │  └─────────┼────────────┘  └─────────┼───────────┘       │ │
│  │            │                          │                   │ │
│  │            └──────────┬───────────────┘                   │ │
│  │                       │                                   │ │
│  │              ┌────────▼────────┐                          │ │
│  │              │ Route Table     │                          │ │
│  │              │ 10.0.0.0/16→local                          │ │
│  │              │ pl-xxx→vpce-xxx │                          │ │
│  │              └────────┬────────┘                          │ │
│  │                       │                                   │ │
│  │            ┌──────────▼──────────┐                        │ │
│  │            │ S3 Gateway Endpoint │                        │ │
│  │            │ (vpce-xxx)          │                        │ │
│  │            └─────────────────────┘                        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                          │                                      │
│              ┌───────────▼────────────┐                         │
│              │  S3 Bucket             │                         │
│              │  - SSE-AES256          │                         │
│              │  - Versioning          │                         │
│              │  - Lifecycle           │                         │
│              │  - Bucket Key          │                         │
│              └────────────────────────┘                         │
│                                                                  │
│  ┌────────────────────┐  ┌──────────────────┐                  │
│  │  Secrets Manager   │  │  CloudWatch      │                  │
│  │  - SFTP Creds      │  │  - Logs          │                  │
│  │  - KMS Encrypted   │  │  - Metrics       │                  │
│  └────────────────────┘  └──────────────────┘                  │
│                                                                  │
│  ┌──────────────────────────────────────────┐                  │
│  │  IAM                                      │                  │
│  │  - Lambda Execution Role                 │                  │
│  │  - S3 Access Policy (Least Privilege)    │                  │
│  │  - Secrets Manager Access Policy         │                  │
│  │  - CloudWatch Logs Policy                │                  │
│  │  - VPC ENI Management Policy             │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                  │
│  ┌──────────────────────────────────────────┐                  │
│  │  EventBridge                              │                  │
│  │  - Schedule: cron(0 2 * * ? *)           │                  │
│  │  - Target: Lambda Function                │                  │
│  └──────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
```

### Deployment Steps (AWS)

1. **Prepare Infrastructure Code**
   ```bash
   cd terraform/environments/dev
   terraform init
   ```

2. **Configure Variables**
   ```hcl
   # terraform.tfvars
   aws_region = "us-east-1"
   environment = "dev"
   vpc_cidr = "10.0.0.0/16"
   private_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
   availability_zones = ["us-east-1a", "us-east-1b"]
   ```

3. **Package Lambda Function**
   ```bash
   cd ../../../
   ./scripts/deployment/package-lambda.sh
   ```

4. **Deploy Infrastructure**
   ```bash
   cd terraform/environments/dev
   terraform plan
   terraform apply
   ```

5. **Update Secrets**
   ```bash
   SECRET_ARN=$(terraform output -raw sftp_secret_arn)
   aws secretsmanager put-secret-value \
     --secret-id $SECRET_ARN \
     --secret-string file://credentials.json
   ```

6. **Test Function**
   ```bash
   FUNCTION_NAME=$(terraform output -raw lambda_function_name)
   aws lambda invoke --function-name $FUNCTION_NAME response.json
   ```

### AWS Resource Checklist

- ✅ VPC with private subnets (multi-AZ)
- ✅ Security groups (egress only)
- ✅ S3 bucket with encryption and lifecycle
- ✅ VPC Gateway Endpoint for S3
- ✅ Lambda function in VPC
- ✅ IAM role with least privilege policies
- ✅ Secrets Manager secret for SFTP credentials
- ✅ CloudWatch Log Group
- ✅ EventBridge rule (optional scheduler)

---

## GCP Deployment Pattern

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      GCP Project                                 │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  VPC Network (Custom Mode)                                 │ │
│  │                                                             │ │
│  │  ┌──────────────────────┐  ┌──────────────────────┐       │ │
│  │  │  us-east1-b          │  │  us-east1-c          │       │ │
│  │  │  Private Subnet      │  │  Private Subnet      │       │ │
│  │  │  10.0.1.0/24         │  │  10.0.2.0/24         │       │ │
│  │  │                      │  │                      │       │ │
│  │  │  Private Google      │  │  Private Google      │       │ │
│  │  │  Access: Enabled     │  │  Access: Enabled     │       │ │
│  │  └──────────────────────┘  └──────────────────────┘       │ │
│  │            │                          │                   │ │
│  │  ┌─────────▼──────────────────────────▼────────┐         │ │
│  │  │  Serverless VPC Access Connector            │         │ │
│  │  │  IP Range: 10.8.0.0/28                      │         │ │
│  │  │  Throughput: 200-300 Mbps                   │         │ │
│  │  └─────────────────┬─────────────────────────────┘       │ │
│  └────────────────────┼──────────────────────────────────────┘ │
│                       │                                         │
│         ┌─────────────▼──────────────┐                          │
│         │  Cloud Functions (Gen 2)   │                          │
│         │  - Python 3.11              │                          │
│         │  - Memory: 512 MB           │                          │
│         │  - Timeout: 540s            │                          │
│         │  - VPC Connector attached   │                          │
│         └─────────────┬────────────────┘                         │
│                       │                                          │
│         ┌─────────────▼──────────────┐                          │
│         │  Cloud Storage Bucket      │                          │
│         │  - CMEK Encryption         │                          │
│         │  - Versioning              │                          │
│         │  - Lifecycle Management    │                          │
│         │  - Uniform Bucket Access   │                          │
│         └────────────────────────────┘                          │
│                                                                  │
│  ┌────────────────────┐  ┌──────────────────┐                  │
│  │  Secret Manager    │  │  Cloud Logging   │                  │
│  │  - SFTP Creds      │  │  - Function Logs │                  │
│  │  - Auto Encrypted  │  │  - Audit Logs    │                  │
│  └────────────────────┘  └──────────────────┘                  │
│                                                                  │
│  ┌──────────────────────────────────────────┐                  │
│  │  Cloud IAM                                │                  │
│  │  - Service Account                        │                  │
│  │  - Storage Object Creator Role            │                  │
│  │  - Secret Manager Accessor Role          │                  │
│  │  - Logging Writer Role                    │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                  │
│  ┌──────────────────────────────────────────┐                  │
│  │  Cloud Scheduler                          │                  │
│  │  - Schedule: 0 2 * * *                   │                  │
│  │  - Target: HTTP (Function URL)            │                  │
│  └──────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
```

### Deployment Steps (GCP)

1. **Enable Required APIs**
   ```bash
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable vpcaccess.googleapis.com
   gcloud services enable secretmanager.googleapis.com
   gcloud services enable storage.googleapis.com
   gcloud services enable cloudscheduler.googleapis.com
   ```

2. **Create VPC and Subnets**
   ```bash
   gcloud compute networks create file-transfer-vpc \
     --subnet-mode=custom \
     --bgp-routing-mode=regional

   gcloud compute networks subnets create private-subnet-1 \
     --network=file-transfer-vpc \
     --region=us-east1 \
     --range=10.0.1.0/24 \
     --enable-private-ip-google-access
   ```

3. **Create VPC Connector**
   ```bash
   gcloud compute networks vpc-access connectors create file-transfer-connector \
     --region=us-east1 \
     --network=file-transfer-vpc \
     --range=10.8.0.0/28 \
     --min-instances=2 \
     --max-instances=10
   ```

4. **Create Service Account**
   ```bash
   gcloud iam service-accounts create file-transfer-sa \
     --display-name="File Transfer Service Account"
   
   # Grant permissions
   gcloud projects add-iam-policy-binding PROJECT_ID \
     --member="serviceAccount:file-transfer-sa@PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/storage.objectCreator"
   ```

5. **Create Secret**
   ```bash
   echo -n '{"username":"user","password":"pass"}' | \
     gcloud secrets create sftp-credentials --data-file=-
   
   # Grant access to service account
   gcloud secrets add-iam-policy-binding sftp-credentials \
     --member="serviceAccount:file-transfer-sa@PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor"
   ```

6. **Deploy Cloud Function**
   ```bash
   gcloud functions deploy file-transfer-function \
     --gen2 \
     --runtime=python311 \
     --region=us-east1 \
     --source=./function \
     --entry-point=transfer_files \
     --memory=512MB \
     --timeout=540s \
     --service-account=file-transfer-sa@PROJECT_ID.iam.gserviceaccount.com \
     --vpc-connector=file-transfer-connector \
     --egress-settings=private-ranges-only \
     --set-env-vars=BUCKET_NAME=file-transfer-bucket,SECRET_ID=sftp-credentials
   ```

7. **Create Cloud Storage Bucket**
   ```bash
   gsutil mb -l us-east1 -c STANDARD gs://file-transfer-bucket
   gsutil versioning set on gs://file-transfer-bucket
   gsutil lifecycle set lifecycle.json gs://file-transfer-bucket
   ```

8. **Setup Scheduler**
   ```bash
   gcloud scheduler jobs create http file-transfer-schedule \
     --location=us-east1 \
     --schedule="0 2 * * *" \
     --uri="https://REGION-PROJECT_ID.cloudfunctions.net/file-transfer-function" \
     --oidc-service-account-email=file-transfer-sa@PROJECT_ID.iam.gserviceaccount.com
   ```

### GCP Resource Checklist

- ✅ VPC Network with custom subnets
- ✅ Private Google Access enabled
- ✅ VPC Access Connector
- ✅ Cloud Storage bucket with lifecycle
- ✅ Cloud Function (Gen 2) with VPC connector
- ✅ Service Account with minimal permissions
- ✅ Secret Manager secret
- ✅ Cloud Logging configured
- ✅ Cloud Scheduler job (optional)

---

## Azure Deployment Pattern

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  Azure Subscription                              │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Resource Group: rg-file-transfer-dev                      │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  Virtual Network (10.0.0.0/16)                       │  │ │
│  │  │                                                       │  │ │
│  │  │  ┌────────────────┐  ┌────────────────┐             │  │ │
│  │  │  │  Zone 1        │  │  Zone 2        │             │  │ │
│  │  │  │  Subnet        │  │  Subnet        │             │  │ │
│  │  │  │  10.0.1.0/24   │  │  10.0.2.0/24   │             │  │ │
│  │  │  │                │  │                │             │  │ │
│  │  │  │  Service       │  │  Service       │             │  │ │
│  │  │  │  Delegation:   │  │  Delegation:   │             │  │ │
│  │  │  │  Functions     │  │  Functions     │             │  │ │
│  │  │  └────────────────┘  └────────────────┘             │  │ │
│  │  │            │                  │                     │  │ │
│  │  │  ┌─────────▼──────────────────▼───────┐            │  │ │
│  │  │  │  Private Endpoint (Storage)        │            │  │ │
│  │  │  │  IP: 10.0.1.4                      │            │  │ │
│  │  │  └────────────────────────────────────┘            │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                       │                                    │ │
│  │         ┌─────────────▼──────────────┐                     │ │
│  │         │  Azure Functions            │                     │ │
│  │         │  - Premium Plan (EP1)       │                     │ │
│  │         │  - Python 3.11              │                     │ │
│  │         │  - VNet Integration         │                     │ │
│  │         │  - Managed Identity         │                     │ │
│  │         └─────────────┬────────────────┘                    │ │
│  │                       │                                     │ │
│  │         ┌─────────────▼──────────────┐                     │ │
│  │         │  Storage Account            │                     │ │
│  │         │  - Blob Container           │                     │ │
│  │         │  - Encryption (SSE)         │                     │ │
│  │         │  - Versioning               │                     │ │
│  │         │  - Lifecycle Management     │                     │ │
│  │         │  - Private Endpoint         │                     │ │
│  │         └────────────────────────────┘                      │ │
│  │                                                             │ │
│  │  ┌────────────────────┐  ┌──────────────────┐             │ │
│  │  │  Key Vault         │  │  Log Analytics   │             │ │
│  │  │  - SFTP Secret     │  │  - Function Logs │             │ │
│  │  │  - Access Policy   │  │  - Metrics       │             │ │
│  │  └────────────────────┘  └──────────────────┘             │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────┐             │ │
│  │  │  Managed Identity                         │             │ │
│  │  │  - Storage Blob Data Contributor          │             │ │
│  │  │  - Key Vault Secrets User                │             │ │
│  │  └──────────────────────────────────────────┘             │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────┐             │ │
│  │  │  Logic App (Optional Scheduler)           │             │ │
│  │  │  - Recurrence Trigger                     │             │ │
│  │  │  - HTTP Action to Function                │             │ │
│  │  └──────────────────────────────────────────┘             │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Deployment Steps (Azure)

1. **Login and Setup**
   ```bash
   az login
   az account set --subscription "SUBSCRIPTION_ID"
   ```

2. **Create Resource Group**
   ```bash
   az group create \
     --name rg-file-transfer-dev \
     --location eastus
   ```

3. **Create Virtual Network**
   ```bash
   az network vnet create \
     --resource-group rg-file-transfer-dev \
     --name vnet-file-transfer \
     --address-prefix 10.0.0.0/16 \
     --subnet-name subnet-functions \
     --subnet-prefix 10.0.1.0/24
   ```

4. **Create Storage Account**
   ```bash
   az storage account create \
     --name stfiletransferdev \
     --resource-group rg-file-transfer-dev \
     --location eastus \
     --sku Standard_LRS \
     --kind StorageV2 \
     --allow-blob-public-access false \
     --enable-hierarchical-namespace false
   
   # Enable versioning
   az storage account blob-service-properties update \
     --account-name stfiletransferdev \
     --enable-versioning true
   
   # Create container
   az storage container create \
     --account-name stfiletransferdev \
     --name files \
     --auth-mode login
   ```

5. **Create Key Vault and Secret**
   ```bash
   az keyvault create \
     --name kv-file-transfer-dev \
     --resource-group rg-file-transfer-dev \
     --location eastus
   
   az keyvault secret set \
     --vault-name kv-file-transfer-dev \
     --name sftp-credentials \
     --value '{"username":"user","password":"pass"}'
   ```

6. **Create Function App (Premium Plan)**
   ```bash
   # Create App Service Plan (Premium EP1)
   az functionapp plan create \
     --resource-group rg-file-transfer-dev \
     --name plan-file-transfer \
     --location eastus \
     --sku EP1 \
     --is-linux
   
   # Create Function App
   az functionapp create \
     --resource-group rg-file-transfer-dev \
     --name func-file-transfer-dev \
     --plan plan-file-transfer \
     --runtime python \
     --runtime-version 3.11 \
     --functions-version 4 \
     --storage-account stfiletransferdev
   
   # Enable system-assigned managed identity
   az functionapp identity assign \
     --name func-file-transfer-dev \
     --resource-group rg-file-transfer-dev
   ```

7. **Configure VNet Integration**
   ```bash
   # Delegate subnet to Functions
   az network vnet subnet update \
     --resource-group rg-file-transfer-dev \
     --vnet-name vnet-file-transfer \
     --name subnet-functions \
     --delegations Microsoft.Web/serverFarms
   
   # Integrate Function with VNet
   az functionapp vnet-integration add \
     --name func-file-transfer-dev \
     --resource-group rg-file-transfer-dev \
     --vnet vnet-file-transfer \
     --subnet subnet-functions
   ```

8. **Grant Permissions**
   ```bash
   # Get managed identity principal ID
   PRINCIPAL_ID=$(az functionapp identity show \
     --name func-file-transfer-dev \
     --resource-group rg-file-transfer-dev \
     --query principalId -o tsv)
   
   # Grant Storage Blob Data Contributor
   az role assignment create \
     --assignee $PRINCIPAL_ID \
     --role "Storage Blob Data Contributor" \
     --scope /subscriptions/SUBSCRIPTION_ID/resourceGroups/rg-file-transfer-dev/providers/Microsoft.Storage/storageAccounts/stfiletransferdev
   
   # Grant Key Vault Secrets User
   az keyvault set-policy \
     --name kv-file-transfer-dev \
     --object-id $PRINCIPAL_ID \
     --secret-permissions get list
   ```

9. **Deploy Function Code**
   ```bash
   cd function-app
   func azure functionapp publish func-file-transfer-dev
   ```

10. **Setup Scheduler (Timer Trigger in Function)**
    ```python
    # function_app.py
    import azure.functions as func
    
    app = func.FunctionApp()
    
    @app.schedule(schedule="0 0 2 * * *", 
                  arg_name="timer", 
                  run_on_startup=False)
    def file_transfer_timer(timer: func.TimerRequest) -> None:
        # Transfer logic here
        pass
    ```

### Azure Resource Checklist

- ✅ Resource Group
- ✅ Virtual Network with delegated subnet
- ✅ Storage Account with blob container
- ✅ Private Endpoint (or Service Endpoint)
- ✅ Azure Functions (Premium Plan for VNet)
- ✅ Managed Identity
- ✅ Key Vault with secrets
- ✅ RBAC assignments
- ✅ Log Analytics workspace
- ✅ Timer trigger (or Logic App)

---

## Multi-Cloud Comparison

### Feature Matrix

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **VNet Integration Cost** | FREE (ENI) | $27/month (Connector min) | $167/month (Premium Plan) |
| **Private Endpoint Cost** | FREE (Gateway) | FREE (Private Google Access) | FREE (Service Endpoint) |
| **Function Free Tier** | 1M requests | 2M requests | 1M requests |
| **Max Function Timeout** | 15 min | 60 min (Gen 2) | Unlimited (Premium) |
| **Cold Start** | ~1-3s (VPC) | ~2-4s (VPC) | ~1-2s (Premium) |
| **Storage Cost (Hot)** | $0.023/GB | $0.020/GB | $0.0184/GB |
| **Secrets Cost** | $0.40/secret/month | $0.06/secret/month | $0.03/secret/month |
| **Logging Cost** | $0.50/GB | $0.50/GB (>50GB) | $2.76/GB |

### Best Choice by Criteria

**Lowest Cost**: GCP (if within free tiers) or AWS (for production with Gateway Endpoint)

**Simplest Deployment**: AWS (native VPC integration, no connector needed)

**Longest Function Execution**: GCP Cloud Functions Gen 2 (60 minutes)

**Best for Large Scale**: AWS (mature tooling, extensive documentation)

**Best for Microsoft Ecosystem**: Azure (AD integration, existing infrastructure)

---

## Environment Strategies

### Development Environment

**Characteristics**:
- Lower costs
- Relaxed security (but still encrypted)
- Single AZ deployment acceptable
- Shorter log retention
- Manual deployments

**Configuration**:
```yaml
Environment: dev
VPC CIDR: 10.0.0.0/16
Subnets: 1 private subnet
Function Memory: 256 MB
Timeout: 120s
Log Retention: 7 days
Storage Lifecycle: None or simple
Monitoring: Basic metrics
```

### Staging Environment

**Characteristics**:
- Production-like configuration
- Multi-AZ for testing
- Standard security practices
- Automated deployments via CI/CD

**Configuration**:
```yaml
Environment: staging
VPC CIDR: 10.1.0.0/16
Subnets: 2 private subnets (multi-AZ)
Function Memory: 512 MB
Timeout: 300s
Log Retention: 30 days
Storage Lifecycle: Simplified (30/90 days)
Monitoring: Full metrics + alarms
```

### Production Environment

**Characteristics**:
- Maximum reliability and security
- Multi-AZ deployment
- Aggressive cost optimization
- Automated deployments with approval gates
- Comprehensive monitoring and alerting

**Configuration**:
```yaml
Environment: prod
VPC CIDR: 10.2.0.0/16
Subnets: 3 private subnets (multi-AZ)
Function Memory: 512 MB (optimized)
Timeout: 300s
Reserved Concurrency: 10
Log Retention: 90 days
Storage Lifecycle: Full (30/90/180 days)
Cross-Region Replication: Enabled
Monitoring: Full stack observability
Alarms: Critical alerts to PagerDuty
Disaster Recovery: Tested quarterly
```

### Multi-Region Production (DR)

**Characteristics**:
- Primary + DR region
- Active-passive or active-active
- Cross-region replication
- Automated failover

**Configuration**:
```yaml
Primary Region: us-east-1
DR Region: us-west-2

Replication: S3 Cross-Region Replication
DNS: Route 53 with health checks
Failover: Automated (health check based)
RTO: < 15 minutes
RPO: < 5 minutes
```

---

## CI/CD Pipeline Example

### GitHub Actions (Multi-Cloud)

```yaml
name: Deploy File Transfer Function

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      cloud:
        description: 'Cloud Provider'
        required: true
        type: choice
        options:
          - aws
          - gcp
          - azure
      environment:
        description: 'Environment'
        required: true
        type: choice
        options:
          - dev
          - staging
          - prod

jobs:
  deploy-aws:
    if: github.event.inputs.cloud == 'aws' || github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
      
      - name: Terraform Init
        run: |
          cd terraform/environments/${{ github.event.inputs.environment || 'dev' }}
          terraform init
      
      - name: Terraform Plan
        run: |
          cd terraform/environments/${{ github.event.inputs.environment || 'dev' }}
          terraform plan
      
      - name: Terraform Apply
        if: github.event.inputs.environment == 'prod'
        run: |
          cd terraform/environments/prod
          terraform apply -auto-approve
  
  deploy-gcp:
    if: github.event.inputs.cloud == 'gcp'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      
      - name: Deploy Cloud Function
        run: |
          gcloud functions deploy file-transfer-function \
            --gen2 \
            --runtime=python311 \
            --region=us-east1 \
            --source=./function \
            --entry-point=transfer_files
  
  deploy-azure:
    if: github.event.inputs.cloud == 'azure'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy to Azure Functions
        uses: Azure/functions-action@v1
        with:
          app-name: func-file-transfer-${{ github.event.inputs.environment }}
          package: ./function-app
```

---

This comprehensive deployment pattern guide enables teams to choose the optimal cloud provider and deployment strategy based on their specific requirements, constraints, and existing infrastructure.
