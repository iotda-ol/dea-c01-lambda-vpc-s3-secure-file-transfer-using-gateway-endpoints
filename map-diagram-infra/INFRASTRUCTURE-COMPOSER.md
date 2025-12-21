# Universal Infrastructure Composer
## Multi-Cloud Architecture for Secure File Transfer Solution

This document provides a comprehensive, cloud-agnostic infrastructure composition that maps the secure file transfer solution across AWS, Google Cloud Platform (GCP), and Microsoft Azure.

---

## Table of Contents

1. [Universal Architecture Overview](#universal-architecture-overview)
2. [Cloud Provider Component Mapping](#cloud-provider-component-mapping)
3. [Detailed Component Descriptions](#detailed-component-descriptions)
4. [Infrastructure as Code Equivalents](#infrastructure-as-code-equivalents)
5. [Network Architecture](#network-architecture)
6. [Security Architecture](#security-architecture)
7. [Data Flow Diagrams](#data-flow-diagrams)
8. [Cost Comparison](#cost-comparison)
9. [Migration Considerations](#migration-considerations)

---

## Universal Architecture Overview

### High-Level Multi-Cloud Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          LEGACY SFTP SERVER                                  │
│                        (On-Premises / External)                              │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                │ Port 22 (SSH/SFTP)
                                │
┌───────────────────────────────▼─────────────────────────────────────────────┐
│                         CLOUD PLATFORM (AWS/GCP/Azure)                       │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                    VIRTUAL PRIVATE NETWORK                          │    │
│  │              (VPC / VNet / Virtual Private Cloud)                   │    │
│  │                                                                      │    │
│  │  ┌──────────────────────────────────────────────────────────────┐  │    │
│  │  │               PRIVATE SUBNET / SUBNETWORK                     │  │    │
│  │  │                  (Isolated Network Zone)                      │  │    │
│  │  │                                                                │  │    │
│  │  │  ┌────────────────────────────────────────────────────────┐  │  │    │
│  │  │  │          SERVERLESS COMPUTE FUNCTION               │  │  │    │
│  │  │  │     (Lambda / Cloud Functions / Azure Functions)      │  │  │    │
│  │  │  │                                                        │  │  │    │
│  │  │  │  Components:                                          │  │  │    │
│  │  │  │  • SFTP Client Library                                │  │  │    │
│  │  │  │  • Object Storage Client                              │  │  │    │
│  │  │  │  • File Transfer Orchestrator                         │  │  │    │
│  │  │  │  • Error Handler & Logger                             │  │  │    │
│  │  │  │  • Credential Manager Integration                     │  │  │    │
│  │  │  └────────────────────┬───────────────────────────────────┘  │  │    │
│  │  │                       │                                       │  │    │
│  │  │                       │ HTTPS (443)                           │  │    │
│  │  │                       │                                       │  │    │
│  │  │  ┌────────────────────▼───────────────────────────────────┐  │  │    │
│  │  │  │       NETWORK SECURITY GROUP / FIREWALL              │  │  │    │
│  │  │  │   • Egress HTTPS (443) to Object Storage             │  │  │    │
│  │  │  │   • Egress SSH/SFTP (22) to Legacy Server            │  │  │    │
│  │  │  │   • No Ingress (Private Function)                    │  │  │    │
│  │  │  └──────────────────────────────────────────────────────────┘  │  │    │
│  │  │                                                                │  │    │
│  │  └────────────────────────┬───────────────────────────────────────┘  │    │
│  │                           │                                           │    │
│  │                           │ Private Connection (No Internet)          │    │
│  │                           │                                           │    │
│  │  ┌────────────────────────▼───────────────────────────────────────┐  │    │
│  │  │         PRIVATE SERVICE ENDPOINT / GATEWAY                     │  │    │
│  │  │  • AWS: VPC Gateway Endpoint (S3)                              │  │    │
│  │  │  • GCP: Private Google Access                                  │  │    │
│  │  │  • Azure: Service Endpoint / Private Endpoint                  │  │    │
│  │  │                                                                 │  │    │
│  │  │  Benefits:                                                      │  │    │
│  │  │  ✓ No NAT Gateway required (Cost savings)                      │  │    │
│  │  │  ✓ Traffic stays within cloud network                          │  │    │
│  │  │  ✓ No data transfer charges                                    │  │    │
│  │  │  ✓ Enhanced security (No internet exposure)                    │  │    │
│  │  └────────────────────────┬───────────────────────────────────────┘  │    │
│  └───────────────────────────┼──────────────────────────────────────────┘    │
│                              │                                               │
│                              │ Private Cloud Network Path                    │
│                              │                                               │
│  ┌───────────────────────────▼──────────────────────────────────────────┐   │
│  │                    OBJECT STORAGE SERVICE                             │   │
│  │         (S3 / Cloud Storage / Blob Storage)                           │   │
│  │                                                                        │   │
│  │  Features:                                                             │   │
│  │  • Server-side encryption (AES-256 / KMS)                             │   │
│  │  • Versioning enabled                                                 │   │
│  │  • Lifecycle policies (Auto-tiering)                                  │   │
│  │  • Public access blocked                                              │   │
│  │  • Access logging enabled                                             │   │
│  │  • Object-level permissions                                           │   │
│  └────────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                    SUPPORTING SERVICES                              │     │
│  │                                                                      │     │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │     │
│  │  │ Secrets Manager  │  │   Log Service    │  │  IAM / RBAC     │  │     │
│  │  │ (Credentials)    │  │  (Monitoring)    │  │  (Permissions)  │  │     │
│  │  │                  │  │                  │  │                 │  │     │
│  │  │ • AWS Secrets    │  │ • CloudWatch     │  │ • IAM Roles     │  │     │
│  │  │ • GCP Secret     │  │ • Cloud Logging  │  │ • Service Accts │  │     │
│  │  │ • Azure Key Vault│  │ • Monitor Logs   │  │ • Managed ID    │  │     │
│  │  └──────────────────┘  └──────────────────┘  └─────────────────┘  │     │
│  │                                                                      │     │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │     │
│  │  │  Event Scheduler │  │   Metrics/APM    │  │  Notification   │  │     │
│  │  │  (Triggers)      │  │  (Performance)   │  │  (Alerts)       │  │     │
│  │  │                  │  │                  │  │                 │  │     │
│  │  │ • EventBridge    │  │ • CloudWatch     │  │ • SNS           │  │     │
│  │  │ • Cloud Scheduler│  │ • Cloud Monitor  │  │ • Pub/Sub       │  │     │
│  │  │ • Logic Apps     │  │ • App Insights   │  │ • Event Grid    │  │     │
│  │  └──────────────────┘  └──────────────────┘  └─────────────────┘  │     │
│  └────────────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Cloud Provider Component Mapping

### Core Infrastructure Components

| **Component Type** | **AWS** | **GCP** | **Azure** | **Purpose** |
|-------------------|---------|---------|-----------|-------------|
| **Serverless Compute** | AWS Lambda | Cloud Functions (2nd Gen) | Azure Functions | Execute file transfer logic without managing servers |
| **Object Storage** | Amazon S3 | Cloud Storage | Azure Blob Storage | Store transferred files with encryption and lifecycle |
| **Virtual Network** | Amazon VPC | Virtual Private Cloud (VPC) | Virtual Network (VNet) | Isolated network environment for resources |
| **Private Subnet** | VPC Subnet (Private) | VPC Subnet | VNet Subnet | Network segment without direct internet access |
| **Security Group** | Security Group | Firewall Rules | Network Security Group (NSG) | Control inbound/outbound traffic |
| **Private Endpoint** | VPC Gateway Endpoint | Private Google Access | Service/Private Endpoint | Private connection to cloud services |
| **Identity & Access** | IAM Roles & Policies | IAM Service Accounts | Managed Identity + RBAC | Manage permissions and authentication |
| **Secrets Management** | AWS Secrets Manager | Secret Manager | Azure Key Vault | Securely store credentials |
| **Logging Service** | CloudWatch Logs | Cloud Logging | Azure Monitor Logs | Centralized logging and monitoring |
| **Metrics Service** | CloudWatch Metrics | Cloud Monitoring | Azure Monitor Metrics | Performance monitoring |
| **Event Scheduler** | EventBridge | Cloud Scheduler | Logic Apps / Timer Trigger | Schedule function executions |
| **Notification Service** | SNS / EventBridge | Pub/Sub | Event Grid | Event-driven notifications |
| **Encryption** | S3 SSE / KMS | CMEK / CSEK | Storage Service Encryption / Key Vault | Data encryption at rest |
| **Route Management** | Route Tables | Routes | Route Tables | Network traffic routing |
| **DNS** | Route 53 / VPC DNS | Cloud DNS | Azure DNS | Domain name resolution |

---

## Detailed Component Descriptions

### 1. Serverless Compute Function

#### AWS Lambda
```yaml
Service: AWS Lambda
Runtime: Python 3.11
Memory: 512 MB
Timeout: 300 seconds
VPC: Enabled (Private Subnets)
Concurrency: Reserved/Provisioned
Handler: lambda_function.lambda_handler
Execution Role: IAM Role with least privilege
Environment Variables:
  - S3_BUCKET_NAME
  - SFTP_SECRET_ARN
  - LOG_LEVEL
Layers: None (dependencies in deployment package)
```

#### GCP Cloud Functions (2nd Gen)
```yaml
Service: Cloud Functions (2nd Gen)
Runtime: Python 3.11
Memory: 512 MiB
Timeout: 300 seconds
VPC: Enabled (Serverless VPC Connector)
Concurrency: 1-1000
Entry Point: file_transfer_handler
Service Account: Custom SA with least privilege
Environment Variables:
  - GCS_BUCKET_NAME
  - SECRET_NAME
  - LOG_LEVEL
```

#### Azure Functions
```yaml
Service: Azure Functions
Runtime: Python 3.11
Plan: Consumption / Premium (with VNet integration)
Memory: 512 MB
Timeout: 300 seconds
VNet: Enabled (VNet Integration)
Concurrency: Instance-based
Function: FileTransferFunction
Identity: Managed Identity
Application Settings:
  - STORAGE_ACCOUNT_NAME
  - KEYVAULT_URI
  - LOG_LEVEL
```

---

### 2. Object Storage

#### Amazon S3
```yaml
Service: Amazon S3
Bucket Configuration:
  - Versioning: Enabled
  - Encryption: SSE-S3 (AES-256) or SSE-KMS
  - Public Access: Blocked (all settings)
  - Bucket Key: Enabled (99% cost reduction)
Lifecycle Policies:
  - Day 30: Transition to Standard-IA
  - Day 90: Transition to Glacier Instant Retrieval
  - Day 180: Transition to Glacier Deep Archive
Access Control:
  - Bucket Policy: Restrict to Lambda role
  - VPC Endpoint Policy: Additional restriction
Monitoring:
  - Access Logging: Enabled
  - CloudWatch Metrics: Enabled
```

#### Google Cloud Storage
```yaml
Service: Cloud Storage
Bucket Configuration:
  - Versioning: Enabled
  - Encryption: Google-managed / CMEK
  - Public Access: Prevented
  - Uniform bucket-level access: Enabled
Lifecycle Policies:
  - Day 30: Transition to Nearline
  - Day 90: Transition to Coldline
  - Day 180: Transition to Archive
Access Control:
  - IAM Policies: Restrict to service account
  - VPC Service Controls: Additional boundary
Monitoring:
  - Access Logs: Enabled
  - Cloud Monitoring: Enabled
```

#### Azure Blob Storage
```yaml
Service: Azure Blob Storage
Storage Account Configuration:
  - Account Kind: StorageV2 (General Purpose v2)
  - Versioning: Enabled
  - Encryption: Microsoft-managed / Customer-managed
  - Public Access: Disabled
  - Hierarchical Namespace: Optional (Data Lake)
Lifecycle Management:
  - Day 30: Move to Cool tier
  - Day 90: Move to Archive tier
Access Control:
  - RBAC: Restrict to Managed Identity
  - Private Endpoint: Enabled
Monitoring:
  - Diagnostic Logs: Enabled
  - Azure Monitor: Enabled
```

---

### 3. Virtual Private Network

#### AWS VPC
```yaml
Service: Amazon VPC
CIDR Block: 10.0.0.0/16
DNS: 
  - DNS Hostnames: Enabled
  - DNS Resolution: Enabled
Subnets:
  - Private Subnet 1: 10.0.1.0/24 (AZ-a)
  - Private Subnet 2: 10.0.2.0/24 (AZ-b)
Route Tables:
  - Private Route Table: No IGW route
  - S3 Gateway Endpoint: Automatic routes
NAT Gateway: Not required (cost savings)
Internet Gateway: Not required for S3 access
```

#### GCP VPC
```yaml
Service: Virtual Private Cloud
Subnet Mode: Custom
Subnets:
  - Private Subnet 1: 10.0.1.0/24 (Region-zone-a)
  - Private Subnet 2: 10.0.2.0/24 (Region-zone-b)
Private Google Access: Enabled
Cloud NAT: Not required for GCS access
Routes:
  - Default route to Private Google Access
Firewall Rules:
  - Egress: Allow HTTPS to googleapis.com
  - Egress: Allow SSH/SFTP to SFTP server
```

#### Azure Virtual Network
```yaml
Service: Virtual Network (VNet)
Address Space: 10.0.0.0/16
DNS Servers: Azure-provided
Subnets:
  - Private Subnet 1: 10.0.1.0/24
  - Private Subnet 2: 10.0.2.0/24
Service Endpoints: Microsoft.Storage
NAT Gateway: Not required
Virtual Network Gateway: Not required
```

---

### 4. Private Service Endpoint

#### AWS VPC Gateway Endpoint (S3)
```yaml
Service: VPC Gateway Endpoint
Type: Gateway (not Interface)
Target Service: com.amazonaws.{region}.s3
Cost: FREE (no hourly or data transfer charges)
Route Table Integration: Automatic
Endpoint Policy:
  - Allow: s3:PutObject, s3:GetObject, s3:ListBucket
  - Resource: Specific bucket ARN only
  - Principal: Lambda execution role
DNS: Automatic (uses public S3 DNS)
```

#### GCP Private Google Access
```yaml
Service: Private Google Access
Type: VPC-level configuration
Target Services: Cloud Storage (GCS)
Cost: FREE
Configuration: Enable on subnet
Access Method: Internal IP addresses
Firewall Rules: Allow egress to googleapis.com
DNS: Google-managed (restricted.googleapis.com)
VPC Service Controls: Optional perimeter
```

#### Azure Service Endpoint / Private Endpoint
```yaml
Service: Service Endpoint (or Private Endpoint)
Type: Service Endpoint for simplicity

Service Endpoint:
  - Service: Microsoft.Storage
  - Cost: FREE
  - Subnet Integration: Enabled on subnet
  - NSG Rules: Allow outbound to Storage

Private Endpoint (Alternative):
  - Private IP in VNet
  - Cost: $7.30/month + data processing
  - Private DNS Zone: Enabled
  - Higher security isolation
```

---

### 5. Identity and Access Management

#### AWS IAM
```yaml
Execution Role: Lambda Execution Role
Type: IAM Role
Trust Policy:
  - Service: lambda.amazonaws.com
Managed Policies: None (custom only)
Custom Policies:
  1. S3 Access Policy:
     - Actions: s3:PutObject, s3:PutObjectAcl, s3:ListBucket
     - Resource: Specific bucket ARN
  2. CloudWatch Logs Policy:
     - Actions: logs:CreateLogStream, logs:PutLogEvents
     - Resource: Specific log group ARN
  3. VPC Execution Policy:
     - Actions: ec2:CreateNetworkInterface, ec2:DescribeNetworkInterfaces, ec2:DeleteNetworkInterface
     - Resource: *
  4. Secrets Manager Policy:
     - Actions: secretsmanager:GetSecretValue
     - Resource: Specific secret ARN
```

#### GCP IAM
```yaml
Service Account: file-transfer-sa
Type: Service Account
Roles:
  1. Cloud Storage Object Creator:
     - Permission: storage.objects.create
     - Resource: Specific bucket
  2. Logging Writer:
     - Permission: logging.logEntries.create
  3. Secret Manager Accessor:
     - Permission: secretmanager.versions.access
     - Resource: Specific secret
  4. Serverless VPC Connector User:
     - Permission: vpcaccess.connectors.use
Impersonation: Disabled
Key Rotation: Automatic (no static keys)
```

#### Azure RBAC
```yaml
Managed Identity: file-transfer-identity
Type: System-assigned Managed Identity
Role Assignments:
  1. Storage Blob Data Contributor:
     - Scope: Specific storage account
     - Permissions: Write, Read, Delete blobs
  2. Key Vault Secrets User:
     - Scope: Specific Key Vault
     - Permissions: Get secrets
  3. Monitoring Metrics Publisher:
     - Scope: Resource group
     - Permissions: Publish metrics
Network Rules: Service endpoint enabled
```

---

### 6. Secrets Management

#### AWS Secrets Manager
```yaml
Service: AWS Secrets Manager
Secret Type: Other type of secret (JSON)
Secret Content:
  username: sftp_username
  password: sftp_password  # OR
  private_key: ssh_private_key
  host: sftp.example.com
  port: 22
Encryption: AWS KMS (default or custom key)
Rotation: Optional (Lambda rotation function)
Cost: $0.40/month per secret + $0.05 per 10K API calls
Access Policy: Restricted to Lambda role
Recovery Window: 7 days
```

#### GCP Secret Manager
```yaml
Service: Secret Manager
Secret Data:
  username: sftp_username
  password: sftp_password  # OR
  private_key: ssh_private_key
  host: sftp.example.com
  port: 22
Encryption: Google-managed / CMEK
Versioning: Enabled (automatic)
Rotation: Manual or Cloud Scheduler triggered
Cost: $0.06 per 10K access operations (6 free versions)
Access Control: IAM policy on secret
Replication: Automatic or user-managed
```

#### Azure Key Vault
```yaml
Service: Azure Key Vault
Vault Type: Standard or Premium
Secrets:
  - sftp-username
  - sftp-password  # OR
  - sftp-private-key
  - sftp-host
  - sftp-port
Encryption: Microsoft-managed keys
Soft Delete: Enabled (90 days retention)
Purge Protection: Enabled
Cost: $0.03 per 10K operations
Access Policy: Managed Identity only
Network: Private Endpoint (optional)
```

---

### 7. Logging and Monitoring

#### AWS CloudWatch
```yaml
Logs:
  - Log Group: /aws/lambda/file-transfer-function
  - Retention: 7 days
  - Encryption: KMS (optional)
  - Log Insights: Available
Metrics:
  - Namespace: AWS/Lambda
  - Metrics: Invocations, Duration, Errors, Throttles
  - Custom Metrics: File transfer count, sizes
Alarms:
  - Error Rate: > 5%
  - Duration: > 200 seconds
  - Throttles: > 0
Dashboards:
  - Lambda performance
  - S3 operations
  - Network metrics
```

#### GCP Cloud Logging & Monitoring
```yaml
Logging:
  - Log Name: projects/{project}/logs/file-transfer
  - Retention: 30 days (default)
  - Log Explorer: Available
  - Log Sinks: Optional (export to BigQuery)
Monitoring:
  - Metrics: cloud.googleapis.com/function/*
  - Custom Metrics: File counts, transfer sizes
  - Uptime Checks: N/A (event-driven)
Alerting:
  - Policies: Error rate, execution time
  - Notification Channels: Email, Pub/Sub, webhook
Dashboards:
  - Cloud Functions metrics
  - Storage operations
```

#### Azure Monitor
```yaml
Logs:
  - Log Analytics Workspace: file-transfer-logs
  - Retention: 30 days
  - Query Language: KQL (Kusto)
  - Application Insights: Integrated
Metrics:
  - Platform Metrics: Function executions, duration
  - Custom Metrics: File metrics
  - Metric Alerts: Available
Alerts:
  - Action Groups: Email, SMS, webhook
  - Alert Rules: Error rate, performance
Application Insights:
  - Dependency Tracking: Enabled
  - Performance Profiling: Available
Dashboards:
  - Azure Portal dashboards
  - Workbooks: Custom visualizations
```

---

## Infrastructure as Code Equivalents

### Terraform Providers

```hcl
# AWS
provider "aws" {
  region = "us-east-1"
}

# GCP
provider "google" {
  project = "my-project-id"
  region  = "us-central1"
}

# Azure
provider "azurerm" {
  features {}
}
```

### Resource Mapping Examples

#### Serverless Function

**AWS - Lambda**
```hcl
resource "aws_lambda_function" "file_transfer" {
  filename         = "lambda_function.zip"
  function_name    = "file-transfer"
  role             = aws_iam_role.lambda.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.11"
  timeout          = 300
  memory_size      = 512
  
  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.lambda.id]
  }
  
  environment {
    variables = {
      S3_BUCKET_NAME  = aws_s3_bucket.files.id
      SFTP_SECRET_ARN = aws_secretsmanager_secret.sftp.arn
    }
  }
}
```

**GCP - Cloud Functions**
```hcl
resource "google_cloudfunctions2_function" "file_transfer" {
  name        = "file-transfer"
  location    = "us-central1"
  description = "SFTP to GCS file transfer"
  
  build_config {
    runtime     = "python311"
    entry_point = "file_transfer_handler"
    source {
      storage_source {
        bucket = google_storage_bucket.source.name
        object = google_storage_bucket_object.code.name
      }
    }
  }
  
  service_config {
    max_instance_count    = 10
    available_memory      = "512Mi"
    timeout_seconds       = 300
    service_account_email = google_service_account.function.email
    
    vpc_connector = google_vpc_access_connector.connector.id
    
    environment_variables = {
      GCS_BUCKET_NAME = google_storage_bucket.files.name
      SECRET_NAME     = google_secret_manager_secret.sftp.secret_id
    }
  }
}
```

**Azure - Functions**
```hcl
resource "azurerm_linux_function_app" "file_transfer" {
  name                       = "file-transfer-func"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  service_plan_id            = azurerm_service_plan.main.id
  storage_account_name       = azurerm_storage_account.function.name
  storage_account_access_key = azurerm_storage_account.function.primary_access_key
  
  site_config {
    application_stack {
      python_version = "3.11"
    }
  }
  
  identity {
    type = "SystemAssigned"
  }
  
  app_settings = {
    STORAGE_ACCOUNT_NAME = azurerm_storage_account.files.name
    KEYVAULT_URI         = azurerm_key_vault.main.vault_uri
    FUNCTIONS_WORKER_RUNTIME = "python"
  }
  
  virtual_network_subnet_id = azurerm_subnet.function.id
}
```

#### Object Storage

**AWS - S3**
```hcl
resource "aws_s3_bucket" "file_transfer" {
  bucket_prefix = "file-transfer-"
}

resource "aws_s3_bucket_versioning" "file_transfer" {
  bucket = aws_s3_bucket.file_transfer.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "file_transfer" {
  bucket = aws_s3_bucket.file_transfer.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}
```

**GCP - Cloud Storage**
```hcl
resource "google_storage_bucket" "file_transfer" {
  name          = "file-transfer-${random_id.bucket_suffix.hex}"
  location      = "US"
  force_destroy = false
  
  versioning {
    enabled = true
  }
  
  encryption {
    default_kms_key_name = google_kms_crypto_key.bucket.id
  }
  
  uniform_bucket_level_access = true
  
  public_access_prevention = "enforced"
}
```

**Azure - Blob Storage**
```hcl
resource "azurerm_storage_account" "file_transfer" {
  name                     = "filetransfer${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  
  blob_properties {
    versioning_enabled = true
  }
  
  network_rules {
    default_action             = "Deny"
    virtual_network_subnet_ids = [azurerm_subnet.function.id]
  }
}
```

---

## Network Architecture

### Private Connectivity Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                    AWS ARCHITECTURE                              │
│                                                                  │
│  Lambda (VPC) → VPC Gateway Endpoint (FREE) → S3                │
│  • No NAT Gateway needed                                        │
│  • No data charges                                              │
│  • Route table integration                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    GCP ARCHITECTURE                              │
│                                                                  │
│  Cloud Functions → Serverless VPC Connector → Private Google    │
│  Access → Cloud Storage                                          │
│  • No Cloud NAT needed for GCS                                  │
│  • VPC connector: $0.07/hour                                    │
│  • Uses internal IPs (restricted.googleapis.com)                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    AZURE ARCHITECTURE                            │
│                                                                  │
│  Azure Functions → VNet Integration → Service Endpoint →        │
│  Blob Storage                                                    │
│  • No NAT Gateway needed                                        │
│  • Service Endpoint: FREE                                       │
│  • Private Endpoint: $7.30/month (more isolated)                │
└─────────────────────────────────────────────────────────────────┘
```

### Network Flow Comparison

| **Flow Step** | **AWS** | **GCP** | **Azure** |
|--------------|---------|---------|-----------|
| 1. Function Execution | Lambda in VPC private subnet | Cloud Functions with VPC connector | Functions with VNet integration |
| 2. DNS Resolution | VPC DNS resolves S3 public DNS | DNS resolves to restricted.googleapis.com | DNS resolves to privatelink endpoint |
| 3. Routing Decision | Route table directs to VPC endpoint | VPC routes to Private Google Access | Route table directs to service endpoint |
| 4. Network Path | Traffic to VPC Gateway Endpoint | Traffic via internal IP to GCS API | Traffic via service endpoint to storage |
| 5. Storage Access | S3 API called with IAM auth | GCS API called with SA auth | Blob API called with managed identity |
| 6. Return Path | Response via same VPC endpoint | Response via same internal path | Response via same service endpoint |

---

## Security Architecture

### Defense in Depth - All Cloud Providers

```
┌──────────────────────────────────────────────────────────────────────┐
│  LAYER 1: Network Security                                           │
│  • Private subnets/networks only (no public IPs)                    │
│  • Security groups/firewall rules (restrictive egress)              │
│  • No ingress rules (event/timer triggered only)                    │
│  • VPC/VNet isolation from internet                                 │
└──────────────────────────────────────────────────────────────────────┘
           ↓
┌──────────────────────────────────────────────────────────────────────┐
│  LAYER 2: Identity & Access Control                                  │
│  • Least privilege IAM/RBAC policies                                │
│  • Service-specific roles/identities                                │
│  • No long-lived credentials (temporary tokens only)                │
│  • Resource-level permissions (specific buckets/accounts)           │
└──────────────────────────────────────────────────────────────────────┘
           ↓
┌──────────────────────────────────────────────────────────────────────┐
│  LAYER 3: Data Protection                                            │
│  • Encryption in transit (TLS 1.2+)                                 │
│  • Encryption at rest (AES-256)                                     │
│  • Key management (KMS/CMEK/Key Vault)                              │
│  • Data classification and labeling                                 │
└──────────────────────────────────────────────────────────────────────┘
           ↓
┌──────────────────────────────────────────────────────────────────────┐
│  LAYER 4: Secrets Management                                         │
│  • Centralized secrets storage                                      │
│  • Automatic rotation (optional)                                    │
│  • Audit logging of secret access                                   │
│  • Encryption of secrets                                            │
└──────────────────────────────────────────────────────────────────────┘
           ↓
┌──────────────────────────────────────────────────────────────────────┐
│  LAYER 5: Monitoring & Audit                                         │
│  • Comprehensive logging (all API calls)                            │
│  • Anomaly detection                                                │
│  • Real-time alerting                                               │
│  • Compliance reporting                                             │
└──────────────────────────────────────────────────────────────────────┘
```

### Security Feature Comparison

| **Security Feature** | **AWS** | **GCP** | **Azure** |
|---------------------|---------|---------|-----------|
| **Encryption at Rest** | S3 SSE-S3/SSE-KMS | Google-managed/CMEK | Microsoft-managed/CMK |
| **Encryption in Transit** | TLS 1.2+ (enforced by S3) | TLS 1.2+ (enforced by GCS) | TLS 1.2+ (enforced) |
| **Key Management** | AWS KMS | Cloud KMS | Azure Key Vault |
| **Secret Rotation** | Lambda rotation function | Cloud Scheduler + Cloud Run | Key Vault rotation policy |
| **Network Isolation** | VPC + Security Groups | VPC + Firewall Rules | VNet + NSG |
| **Private Connectivity** | VPC Endpoint (Gateway) | Private Google Access | Service Endpoint |
| **Identity Federation** | IAM Roles | Workload Identity | Managed Identity |
| **Audit Logging** | CloudTrail + CloudWatch | Cloud Audit Logs | Activity Log + Monitor |
| **Compliance** | Multiple (HIPAA, PCI, etc.) | Multiple (HIPAA, PCI, etc.) | Multiple (HIPAA, PCI, etc.) |
| **DDoS Protection** | AWS Shield (Standard free) | Google Cloud Armor | Azure DDoS Protection |
| **Threat Detection** | GuardDuty | Security Command Center | Defender for Cloud |

---

## Data Flow Diagrams

### End-to-End Transfer Flow

```
┌────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: TRIGGERING                                                   │
│                                                                         │
│  Event Scheduler → Invokes Serverless Function                         │
│  • AWS: EventBridge Rule → Lambda                                      │
│  • GCP: Cloud Scheduler → Cloud Functions                              │
│  • Azure: Timer Trigger → Azure Functions                              │
└────────────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: CREDENTIAL RETRIEVAL                                         │
│                                                                         │
│  Function → Secrets Service → Returns SFTP Credentials                 │
│  • AWS: Lambda → Secrets Manager API                                   │
│  • GCP: Cloud Functions → Secret Manager API                           │
│  • Azure: Functions → Key Vault API                                    │
│                                                                         │
│  Authentication: IAM Role / Service Account / Managed Identity         │
└────────────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: SFTP CONNECTION                                              │
│                                                                         │
│  Function → Establishes SSH/SFTP connection → SFTP Server              │
│  • Network path: Private subnet → Internet (via IGW or egress)        │
│  • Protocol: SSH (Port 22)                                             │
│  • Authentication: Username/Password OR SSH Key                        │
│  • Library: Paramiko (Python) / SSH libraries                          │
└────────────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────────────┐
│  PHASE 4: FILE DOWNLOAD                                                │
│                                                                         │
│  Function downloads file(s) from SFTP → Temporarily stores in memory   │
│  • File listing (optional pattern matching)                            │
│  • Stream download to minimize memory usage                            │
│  • Checksum verification (optional)                                    │
│  • Error handling for large files                                      │
└────────────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────────────┐
│  PHASE 5: OBJECT STORAGE UPLOAD                                        │
│                                                                         │
│  Function → Private Endpoint → Object Storage                          │
│  • AWS: Lambda → VPC Gateway Endpoint → S3                             │
│  • GCP: Cloud Functions → Private Google Access → GCS                  │
│  • Azure: Functions → Service Endpoint → Blob Storage                  │
│                                                                         │
│  Transfer Method:                                                       │
│  • Streaming upload (multipart for large files)                        │
│  • Metadata tagging (source, timestamp, etc.)                          │
│  • Server-side encryption applied                                      │
└────────────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────────────┐
│  PHASE 6: LOGGING & NOTIFICATION                                       │
│                                                                         │
│  Function → Logs results → Logging Service                             │
│  • Success: File name, size, duration, destination                     │
│  • Failure: Error message, stack trace, retry info                     │
│                                                                         │
│  Optional: Send notification                                            │
│  • AWS: SNS topic                                                       │
│  • GCP: Pub/Sub message                                                │
│  • Azure: Event Grid event                                             │
└────────────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────────────┐
│  PHASE 7: CLEANUP & COMPLETION                                         │
│                                                                         │
│  • Close SFTP connection                                               │
│  • Release resources                                                   │
│  • Update metrics/counters                                             │
│  • Return success/failure status                                       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Cost Comparison

### Monthly Cost Breakdown (Assumptions: 1,000 transfers/month, 100 MB avg file size)

#### AWS Costs

| **Service** | **Usage** | **Cost** |
|------------|-----------|----------|
| Lambda | 1,000 invocations × 30s @ 512 MB | $0.25 |
| S3 Storage | 100 GB (with lifecycle) | $2.30 |
| S3 Requests | 1,000 PUTs | $0.01 |
| S3 Gateway Endpoint | Unlimited data | **$0.00** |
| Secrets Manager | 1 secret + 1,000 API calls | $0.40 |
| CloudWatch Logs | 1 GB | $0.50 |
| EventBridge | 1,000 rule evaluations | $0.00 (free tier) |
| VPC | No NAT Gateway | **$0.00** |
| **Total** | | **~$3.46/month** |

#### GCP Costs

| **Service** | **Usage** | **Cost** |
|------------|-----------|----------|
| Cloud Functions (2nd Gen) | 1,000 invocations × 30s @ 512 MB | $0.40 |
| Cloud Storage | 100 GB Standard (with lifecycle) | $2.00 |
| Storage Operations | 1,000 Class A operations | $0.05 |
| Serverless VPC Connector | 730 hours @ $0.07/hour | $51.10 |
| Secret Manager | 1 secret + 1,000 accesses | $0.06 |
| Cloud Logging | 1 GB | $0.50 |
| Cloud Scheduler | 1 job | $0.10 |
| Private Google Access | Unlimited data | **$0.00** |
| **Total** | | **~$54.21/month** |
| **Total (without VPC Connector)** | | **~$3.11/month** |

*Note: VPC Connector can be avoided if Cloud Functions can access SFTP server publicly.*

#### Azure Costs

| **Service** | **Usage** | **Cost** |
|------------|-----------|----------|
| Azure Functions (Consumption) | 1,000 executions × 30s @ 512 MB | $0.20 |
| Blob Storage | 100 GB Hot tier (with lifecycle) | $1.80 |
| Storage Transactions | 1,000 write operations | $0.01 |
| Service Endpoint | Unlimited data | **$0.00** |
| Key Vault | 1 vault + 1,000 operations | $0.03 |
| Monitor Logs | 1 GB | $2.76 |
| Logic Apps (Timer) | 1,000 actions | $0.00 (free tier) |
| VNet | No NAT Gateway | **$0.00** |
| **Total** | | **~$4.80/month** |

### Cost Comparison Summary

| **Cloud Provider** | **Monthly Cost** | **Key Differentiator** |
|-------------------|-----------------|----------------------|
| **AWS** | ~$3.46 | Free VPC Gateway Endpoint, mature services |
| **GCP** | ~$3.11 (or ~$54.21 with VPC Connector) | Slightly cheaper storage, expensive VPC connectivity |
| **Azure** | ~$4.80 | Higher logging costs, competitive pricing otherwise |

**Winner: GCP (without VPC Connector) or AWS**

---

## Migration Considerations

### Multi-Cloud Strategy Decision Matrix

#### When to Choose AWS
- ✅ Existing AWS infrastructure
- ✅ Need for extensive AWS service integrations
- ✅ Require mature ecosystem and extensive documentation
- ✅ VPC Gateway Endpoint for zero-cost private connectivity
- ✅ Comprehensive IAM and security features

#### When to Choose GCP
- ✅ Existing GCP infrastructure
- ✅ Need for BigQuery integration (analytics)
- ✅ Prefer uniform bucket-level access (simpler IAM)
- ✅ Cost-sensitive on storage (slightly cheaper)
- ✅ Can avoid VPC Connector requirement

#### When to Choose Azure
- ✅ Existing Azure/Microsoft ecosystem
- ✅ Integration with Microsoft services (Active Directory, Office 365)
- ✅ Enterprise compliance requirements aligned with Azure
- ✅ Prefer managed identities over service accounts
- ✅ Strong hybrid cloud requirements

### Portability Considerations

#### Highly Portable Components (Easy to migrate)
- ✅ Python code (serverless function logic)
- ✅ SFTP client library (Paramiko works everywhere)
- ✅ Logging logic (structured logging patterns)
- ✅ Error handling patterns
- ✅ Configuration management approach

#### Provider-Specific Components (Requires adaptation)
- ⚠️ Infrastructure as Code (Terraform helps, but resources differ)
- ⚠️ IAM/RBAC policies (different models)
- ⚠️ Secrets management API calls (different SDKs)
- ⚠️ Object storage API calls (S3 vs GCS vs Blob)
- ⚠️ Logging/monitoring integration (different services)
- ⚠️ Event scheduling syntax (different formats)

### Migration Checklist

```
□ Code Refactoring
  □ Abstract cloud-specific SDK calls (create adapter layer)
  □ Environment variable standardization
  □ Configuration externalization
  □ Dependency management (requirements.txt compatible)

□ Infrastructure Setup
  □ Virtual network configuration
  □ Security groups/firewall rules
  □ Private endpoint/service endpoint setup
  □ IAM/RBAC role creation

□ Secrets Migration
  □ Export secrets from source provider
  □ Import to target provider secrets service
  □ Update secret ARN/name references in code

□ Deployment Package
  □ Rebuild deployment package for target runtime
  □ Test locally if possible
  □ Deploy to staging environment first

□ Testing
  □ Unit tests (should pass without changes)
  □ Integration tests (adapt for target provider)
  □ End-to-end tests (full workflow)
  □ Performance tests (compare metrics)

□ Monitoring Setup
  □ Configure logging service
  □ Create dashboards
  □ Set up alerts
  □ Test notification channels

□ Cutover
  □ Update DNS/endpoints if applicable
  □ Update scheduling/triggering
  □ Monitor closely for first 24-48 hours
  □ Keep rollback plan ready
```

---

## Architecture Patterns

### Pattern 1: Event-Driven Scheduled Transfer
**Use Case:** Regular, scheduled file transfers (e.g., nightly batch)

**Trigger:** Scheduler (EventBridge / Cloud Scheduler / Timer Trigger)
**Execution:** Serverless function downloads from SFTP and uploads to object storage
**Best For:** Predictable schedules, non-time-critical transfers

### Pattern 2: On-Demand Transfer
**Use Case:** Ad-hoc file transfers triggered by external events

**Trigger:** API call, webhook, or manual invocation
**Execution:** Same as Pattern 1
**Best For:** User-initiated transfers, API-driven workflows

### Pattern 3: Multi-File Batch Transfer
**Use Case:** Transfer multiple files in one execution

**Trigger:** Scheduled or on-demand
**Execution:** Function iterates through file list, transfers all
**Optimization:** Use parallel processing (with concurrency limits)
**Best For:** Large numbers of small files

### Pattern 4: Large File Transfer with Streaming
**Use Case:** Transfer very large files (>100 MB)

**Execution:** 
- Stream download from SFTP (avoid loading entire file in memory)
- Multipart upload to object storage
- Progress tracking and resume capability
**Best For:** Large files, memory-constrained environments

### Pattern 5: Hybrid Multi-Cloud Sync
**Use Case:** Sync files across multiple cloud providers

**Execution:**
- Primary function in one cloud
- Cross-cloud API calls (S3 to GCS, etc.)
- Use cloud-native replication when possible
**Best For:** Disaster recovery, multi-cloud redundancy

---

## Conclusion

This infrastructure composer provides a universal framework for implementing secure file transfer solutions across AWS, GCP, and Azure. Key takeaways:

1. **Core Architecture Remains Consistent:** Serverless compute in private networks with private connectivity to object storage
2. **Cloud-Specific Optimizations:** Each provider has unique features (VPC Gateway Endpoint, Private Google Access, Service Endpoints)
3. **Cost Variations:** AWS and GCP (without VPC Connector) are most cost-effective
4. **Security Posture:** All three providers support defense-in-depth security when properly configured
5. **Portability:** Business logic is highly portable; infrastructure requires adaptation

### Recommended Approach

1. **Start with AWS** if no existing cloud preference (mature ecosystem, zero-cost VPC endpoint)
2. **Use Terraform** for all infrastructure to ease potential future migrations
3. **Abstract cloud-specific code** into separate modules/classes
4. **Implement comprehensive testing** that works across providers
5. **Document cloud-specific configurations** for team knowledge sharing

---

## Additional Resources

### AWS Resources
- [AWS Lambda VPC Networking](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html)
- [VPC Gateway Endpoints for S3](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)
- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/)

### GCP Resources
- [Cloud Functions VPC Connectivity](https://cloud.google.com/functions/docs/networking/network-settings)
- [Private Google Access](https://cloud.google.com/vpc/docs/private-google-access)
- [Secret Manager](https://cloud.google.com/secret-manager)

### Azure Resources
- [Azure Functions VNet Integration](https://docs.microsoft.com/en-us/azure/azure-functions/functions-networking-options)
- [Virtual Network Service Endpoints](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview)
- [Azure Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/)

### Multi-Cloud Terraform
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Terraform AzureRM Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-21  
**Maintained By:** Infrastructure Team
