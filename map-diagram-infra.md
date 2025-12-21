# Universal Infrastructure Composer - Multi-Cloud Architecture Map

## Overview

This document provides a **comprehensive, cloud-agnostic infrastructure composition** for the secure file transfer solution. It maps all components and resources to be **universal across AWS, GCP, and Azure**, enabling deployment on any major cloud provider.

## Table of Contents

1. [Universal Architecture Components](#universal-architecture-components)
2. [Cloud Service Mappings](#cloud-service-mappings)
3. [Architecture Diagrams](#architecture-diagrams)
4. [Component Details](#component-details)
5. [Deployment Patterns](#deployment-patterns)
6. [Configuration Examples](#configuration-examples)
7. [Security Mappings](#security-mappings)
8. [Monitoring & Logging](#monitoring--logging)
9. [Cost Comparison](#cost-comparison)

---

## Universal Architecture Components

### Core Components (Cloud-Agnostic)

| Component | Purpose | Function |
|-----------|---------|----------|
| **Serverless Function** | File transfer logic | Executes SFTP to object storage transfer |
| **Virtual Network** | Network isolation | Provides private network space for resources |
| **Private Subnets** | Secure compute environment | Isolates serverless functions from internet |
| **Object Storage** | File destination | Stores transferred files with encryption |
| **Private Endpoint** | Internal connectivity | Enables private access to object storage |
| **Identity & Access Management** | Security & permissions | Controls access to resources |
| **Secret Management** | Credential storage | Securely stores SFTP credentials |
| **Logging Service** | Observability | Captures execution logs and metrics |
| **Event Scheduler** | Automation | Triggers functions on schedule |
| **Security Groups/Firewalls** | Network security | Controls inbound/outbound traffic |

---

## Cloud Service Mappings

### Complete Service Mapping Table

| Universal Component | AWS | GCP | Azure | Notes |
|---------------------|-----|-----|-------|-------|
| **Serverless Function** | Lambda | Cloud Functions | Azure Functions | Stateless compute |
| **Virtual Network** | VPC | VPC | Virtual Network (VNet) | Private network space |
| **Private Subnets** | VPC Subnets | VPC Subnets | VNet Subnets | Network segmentation |
| **Object Storage** | S3 | Cloud Storage | Blob Storage | Durable object storage |
| **Private Endpoint** | VPC Gateway Endpoint (S3) | Private Google Access | Private Endpoint | Private connectivity |
| **IAM Roles** | IAM Roles | Service Accounts | Managed Identities | Identity management |
| **IAM Policies** | IAM Policies | IAM Roles/Bindings | RBAC Roles | Permission definitions |
| **Secret Management** | Secrets Manager | Secret Manager | Key Vault | Credential storage |
| **Logging** | CloudWatch Logs | Cloud Logging | Log Analytics | Centralized logging |
| **Metrics** | CloudWatch Metrics | Cloud Monitoring | Azure Monitor | Performance metrics |
| **Event Scheduler** | EventBridge | Cloud Scheduler | Logic Apps / Event Grid | Scheduled triggers |
| **Security Groups** | Security Groups | Firewall Rules | Network Security Groups | Network ACLs |
| **Route Tables** | Route Tables | Routes | Route Tables | Network routing |
| **Encryption (Object)** | SSE-S3/KMS | CMEK/Google-managed | SSE/Customer-managed | Data encryption |
| **Encryption (Transit)** | TLS/HTTPS | TLS/HTTPS | TLS/HTTPS | In-transit encryption |
| **Versioning** | S3 Versioning | Object Versioning | Blob Versioning | Object versioning |
| **Lifecycle Policies** | S3 Lifecycle | Object Lifecycle | Lifecycle Management | Cost optimization |
| **Tags/Labels** | Tags | Labels | Tags | Resource organization |
| **DNS** | Route 53 | Cloud DNS | Azure DNS | Domain management |
| **KMS** | AWS KMS | Cloud KMS | Azure Key Vault | Key management |

---

## Architecture Diagrams

### Universal Architecture Pattern

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLOUD PROVIDER                                │
│                     (AWS / GCP / Azure)                              │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │              VIRTUAL NETWORK (VPC/VNet)                     │    │
│  │                  (10.0.0.0/16)                              │    │
│  │                                                              │    │
│  │  ┌────────────────────────────────────────────────────┐    │    │
│  │  │         PRIVATE SUBNET 1 (Multi-AZ/Zone)           │    │    │
│  │  │              (10.0.1.0/24)                          │    │    │
│  │  │                                                      │    │    │
│  │  │  ┌──────────────────────────────────────┐          │    │    │
│  │  │  │   SERVERLESS FUNCTION                │          │    │    │
│  │  │  │   - Runtime: Python 3.11              │          │    │    │
│  │  │  │   - Memory: 512 MB                    │          │    │    │
│  │  │  │   - Timeout: 300s                     │          │    │    │
│  │  │  │   - VPC-attached                      │          │    │    │
│  │  │  │                                        │          │    │    │
│  │  │  │   Responsibilities:                   │          │    │    │
│  │  │  │   1. Retrieve SFTP credentials        │          │    │    │
│  │  │  │   2. Connect to SFTP server           │          │    │    │
│  │  │  │   3. Download files                   │          │    │    │
│  │  │  │   4. Upload to object storage         │          │    │    │
│  │  │  │   5. Log operations                   │          │    │    │
│  │  │  └──────────┬──────────────┬────────────┘          │    │    │
│  │  │             │              │                        │    │    │
│  │  └─────────────┼──────────────┼────────────────────────┘    │    │
│  │                │              │                              │    │
│  │                │ HTTPS        │ SSH/SFTP (Port 22)           │    │
│  │                │              │                              │    │
│  │  ┌─────────────▼────────────┐ │                              │    │
│  │  │  PRIVATE ENDPOINT        │ └──────────────────────────┐   │    │
│  │  │  (Gateway/Service)       │                            │   │    │
│  │  │  - FREE in AWS/GCP       │                            │   │    │
│  │  │  - No data charges       │                            │   │    │
│  │  │  - Private connectivity  │                            │   │    │
│  │  └─────────────┬────────────┘                            │   │    │
│  │                │                                          │   │    │
│  └────────────────┼──────────────────────────────────────────┼───┘    │
│                   │                                          │        │
│                   │ Private                                  │        │
│                   │ Connection                               │        │
│         ┌─────────▼────────────┐                   ┌─────────▼──────┐ │
│         │  OBJECT STORAGE      │                   │  EXTERNAL       │ │
│         │  - Encrypted at rest │                   │  SFTP SERVER    │ │
│         │  - Versioning enabled│                   │  (Legacy System)│ │
│         │  - Lifecycle policies│                   │                 │ │
│         │  - Private access    │                   └─────────────────┘ │
│         └──────────────────────┘                            ▲          │
│                                                              │          │
│         ┌──────────────────────┐                            │          │
│         │  SECRET MANAGER      │                            │          │
│         │  - SFTP credentials  │                            │          │
│         │  - Encrypted storage │                            │          │
│         └──────────────────────┘                            │          │
│                                                              │          │
│         ┌──────────────────────┐                    Internet/VPN      │
│         │  LOGGING SERVICE     │                                       │
│         │  - Function logs     │                                       │
│         │  - Metrics & traces  │                                       │
│         └──────────────────────┘                                       │
│                                                                         │
│         ┌──────────────────────┐                                       │
│         │  EVENT SCHEDULER     │                                       │
│         │  - Cron schedule     │                                       │
│         │  - Triggers function │                                       │
│         └──────────────────────┘                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

### AWS-Specific Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           AWS CLOUD                                  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                   VPC (10.0.0.0/16)                         │    │
│  │                                                              │    │
│  │  ┌──────────────────┐        ┌──────────────────┐          │    │
│  │  │ Private Subnet   │        │ Private Subnet   │          │    │
│  │  │ AZ-1 (10.0.1.0/24)│       │ AZ-2 (10.0.2.0/24)│         │    │
│  │  │                  │        │                  │          │    │
│  │  │  ┌─────────────┐ │        │  ┌─────────────┐ │          │    │
│  │  │  │   Lambda    │ │        │  │   Lambda    │ │          │    │
│  │  │  │  Function   │ │        │  │   (HA)      │ │          │    │
│  │  │  │  Python 3.11│ │        │  │             │ │          │    │
│  │  │  └──────┬──────┘ │        │  └──────┬──────┘ │          │    │
│  │  │         │        │        │         │        │          │    │
│  │  └─────────┼────────┘        └─────────┼────────┘          │    │
│  │            │                           │                   │    │
│  │  ┌─────────▼───────────────────────────▼────────┐          │    │
│  │  │     S3 VPC Gateway Endpoint (FREE)           │          │    │
│  │  │     - Attached to Route Tables                │          │    │
│  │  │     - Endpoint Policy (Least Privilege)      │          │    │
│  │  └──────────────────┬───────────────────────────┘          │    │
│  │                     │                                       │    │
│  └─────────────────────┼───────────────────────────────────────┘    │
│                        │                                            │
│         ┌──────────────▼─────────────┐                              │
│         │    S3 Bucket               │                              │
│         │    - SSE-S3/KMS           │                              │
│         │    - Bucket Key Enabled   │                              │
│         │    - Versioning           │                              │
│         │    - Lifecycle Policies   │                              │
│         │    - Public Access Blocked│                              │
│         └───────────────────────────┘                              │
│                                                                      │
│         ┌───────────────────────────┐                              │
│         │  Secrets Manager          │                              │
│         │  - SFTP Credentials       │                              │
│         │  - KMS Encrypted          │                              │
│         └───────────────────────────┘                              │
│                                                                      │
│         ┌───────────────────────────┐                              │
│         │  CloudWatch Logs          │                              │
│         │  - Log Group              │                              │
│         │  - 7-day Retention        │                              │
│         └───────────────────────────┘                              │
│                                                                      │
│         ┌───────────────────────────┐                              │
│         │  EventBridge              │                              │
│         │  - Scheduled Rule         │                              │
│         │  - Cron Expression        │                              │
│         └───────────────────────────┘                              │
│                                                                      │
│         ┌───────────────────────────┐                              │
│         │  IAM                      │                              │
│         │  - Lambda Execution Role  │                              │
│         │  - S3 Access Policy       │                              │
│         │  - VPC Execution Policy   │                              │
│         │  - Secrets Access Policy  │                              │
│         └───────────────────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘
```

### GCP-Specific Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      GOOGLE CLOUD PLATFORM                           │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                   VPC (10.0.0.0/16)                         │    │
│  │                                                              │    │
│  │  ┌──────────────────┐        ┌──────────────────┐          │    │
│  │  │ Private Subnet   │        │ Private Subnet   │          │    │
│  │  │ Zone A (10.0.1.0/24)│     │ Zone B (10.0.2.0/24)│       │    │
│  │  │                  │        │                  │          │    │
│  │  │  ┌─────────────┐ │        │  ┌─────────────┐ │          │    │
│  │  │  │ Cloud       │ │        │  │ Cloud       │ │          │    │
│  │  │  │ Function    │ │        │  │ Function    │ │          │    │
│  │  │  │ Gen 2       │ │        │  │ (HA)        │ │          │    │
│  │  │  │ Python 3.11 │ │        │  │             │ │          │    │
│  │  │  └──────┬──────┘ │        │  └──────┬──────┘ │          │    │
│  │  │         │        │        │         │        │          │    │
│  │  └─────────┼────────┘        └─────────┼────────┘          │    │
│  │            │                           │                   │    │
│  │  ┌─────────▼───────────────────────────▼────────┐          │    │
│  │  │     Private Google Access (FREE)             │          │    │
│  │  │     - Enables private GCS access             │          │    │
│  │  │     - No external IP needed                  │          │    │
│  │  └──────────────────┬───────────────────────────┘          │    │
│  │                     │                                       │    │
│  └─────────────────────┼───────────────────────────────────────┘    │
│                        │                                            │
│         ┌──────────────▼─────────────┐                              │
│         │  Cloud Storage Bucket      │                              │
│         │  - Google-managed encryption│                             │
│         │  - CMEK (optional)         │                              │
│         │  - Object Versioning       │                              │
│         │  - Lifecycle Policies      │                              │
│         │  - Uniform bucket-level access│                           │
│         └───────────────────────────┘                              │
│                                                                      │
│         ┌───────────────────────────┐                              │
│         │  Secret Manager           │                              │
│         │  - SFTP Credentials       │                              │
│         │  - Encrypted with KMS     │                              │
│         └───────────────────────────┘                              │
│                                                                      │
│         ┌───────────────────────────┐                              │
│         │  Cloud Logging            │                              │
│         │  - Function Logs          │                              │
│         │  - Log Retention          │                              │
│         └───────────────────────────┘                              │
│                                                                      │
│         ┌───────────────────────────┐                              │
│         │  Cloud Scheduler          │                              │
│         │  - Cron Job               │                              │
│         │  - HTTP/Pub/Sub trigger   │                              │
│         └───────────────────────────┘                              │
│                                                                      │
│         ┌───────────────────────────┐                              │
│         │  IAM                      │                              │
│         │  - Service Account        │                              │
│         │  - Cloud Storage roles    │                              │
│         │  - Secret Manager roles   │                              │
│         │  - VPC Access roles       │                              │
│         └───────────────────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘
```

### Azure-Specific Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MICROSOFT AZURE                               │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │              Virtual Network (10.0.0.0/16)                  │    │
│  │                                                              │    │
│  │  ┌──────────────────┐        ┌──────────────────┐          │    │
│  │  │ Private Subnet   │        │ Private Subnet   │          │    │
│  │  │ Zone 1 (10.0.1.0/24)│     │ Zone 2 (10.0.2.0/24)│       │    │
│  │  │                  │        │                  │          │    │
│  │  │  ┌─────────────┐ │        │  ┌─────────────┐ │          │    │
│  │  │  │ Azure       │ │        │  │ Azure       │ │          │    │
│  │  │  │ Function    │ │        │  │ Function    │ │          │    │
│  │  │  │ Premium/    │ │        │  │ (HA)        │ │          │    │
│  │  │  │ Dedicated   │ │        │  │             │ │          │    │
│  │  │  │ Python 3.11 │ │        │  │             │ │          │    │
│  │  │  └──────┬──────┘ │        │  └──────┬──────┘ │          │    │
│  │  │         │        │        │         │        │          │    │
│  │  └─────────┼────────┘        └─────────┼────────┘          │    │
│  │            │                           │                   │    │
│  │  ┌─────────▼───────────────────────────▼────────┐          │    │
│  │  │     Private Endpoint                         │          │    │
│  │  │     - Azure Storage Private Endpoint         │          │    │
│  │  │     - Private DNS Zone                       │          │    │
│  │  └──────────────────┬───────────────────────────┘          │    │
│  │                     │                                       │    │
│  └─────────────────────┼───────────────────────────────────────┘    │
│                        │                                            │
│         ┌──────────────▼─────────────┐                              │
│         │  Blob Storage Account      │                              │
│         │  - SSE (AES-256)           │                              │
│         │  - Customer-managed keys   │                              │
│         │  - Blob Versioning         │                              │
│         │  - Lifecycle Management    │                              │
│         │  - Private Endpoint only   │                              │
│         └───────────────────────────┘                              │
│                                                                      │
│         ┌───────────────────────────┐                              │
│         │  Key Vault                │                              │
│         │  - SFTP Credentials       │                              │
│         │  - Encryption keys        │                              │
│         └───────────────────────────┘                              │
│                                                                      │
│         ┌───────────────────────────┐                              │
│         │  Log Analytics            │                              │
│         │  - Application Insights   │                              │
│         │  - Function Logs          │                              │
│         └───────────────────────────┘                              │
│                                                                      │
│         ┌───────────────────────────┐                              │
│         │  Logic Apps / Event Grid  │                              │
│         │  - Scheduled Trigger      │                              │
│         │  - Timer Trigger          │                              │
│         └───────────────────────────┘                              │
│                                                                      │
│         ┌───────────────────────────┐                              │
│         │  RBAC                     │                              │
│         │  - Managed Identity       │                              │
│         │  - Storage Blob roles     │                              │
│         │  - Key Vault roles        │                              │
│         │  - Network Contributor    │                              │
│         └───────────────────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Serverless Function

**Purpose**: Execute file transfer logic between SFTP and object storage

#### AWS Implementation
```hcl
resource "aws_lambda_function" "file_transfer" {
  function_name = "secure-file-transfer"
  runtime       = "python3.11"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 512
  timeout       = 300
  
  vpc_config {
    subnet_ids         = [aws_subnet.private.*.id]
    security_group_ids = [aws_security_group.lambda.id]
  }
  
  environment {
    variables = {
      S3_BUCKET_NAME  = aws_s3_bucket.files.id
      SECRET_ARN      = aws_secretsmanager_secret.sftp.arn
    }
  }
}
```

#### GCP Implementation
```hcl
resource "google_cloudfunctions2_function" "file_transfer" {
  name        = "secure-file-transfer"
  location    = var.region
  
  build_config {
    runtime     = "python311"
    entry_point = "main"
  }
  
  service_config {
    max_instance_count = 10
    available_memory   = "512M"
    timeout_seconds    = 300
    
    vpc_connector = google_vpc_access_connector.connector.id
    
    environment_variables = {
      GCS_BUCKET_NAME = google_storage_bucket.files.name
      SECRET_ID       = google_secret_manager_secret.sftp.secret_id
    }
  }
}
```

#### Azure Implementation
```hcl
resource "azurerm_linux_function_app" "file_transfer" {
  name                = "secure-file-transfer"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  
  storage_account_name       = azurerm_storage_account.function.name
  storage_account_access_key = azurerm_storage_account.function.primary_access_key
  service_plan_id           = azurerm_service_plan.main.id
  
  site_config {
    application_stack {
      python_version = "3.11"
    }
    
    vnet_route_all_enabled = true
  }
  
  app_settings = {
    STORAGE_ACCOUNT_NAME = azurerm_storage_account.files.name
    KEY_VAULT_URI        = azurerm_key_vault.main.vault_uri
  }
  
  virtual_network_subnet_id = azurerm_subnet.private.id
}
```

### 2. Virtual Network

**Purpose**: Provide network isolation and security

#### Configuration Comparison

| Aspect | AWS VPC | GCP VPC | Azure VNet |
|--------|---------|---------|------------|
| CIDR Block | 10.0.0.0/16 | 10.0.0.0/16 | 10.0.0.0/16 |
| Subnet Size | /24 per AZ | /24 per Zone | /24 per Zone |
| DNS Support | Route 53 | Cloud DNS | Azure DNS |
| Private DNS | Enabled | Enabled | Private DNS Zones |
| Multi-AZ/Zone | Yes | Yes | Yes |

### 3. Object Storage

**Purpose**: Store transferred files securely

#### Feature Comparison

| Feature | AWS S3 | GCP Cloud Storage | Azure Blob Storage |
|---------|--------|-------------------|-------------------|
| Encryption at Rest | SSE-S3, SSE-KMS | Google-managed, CMEK | SSE, Customer-managed |
| Versioning | Yes | Yes | Yes |
| Lifecycle Policies | Yes | Yes | Yes |
| Storage Classes | Standard, IA, Glacier, Deep Archive | Standard, Nearline, Coldline, Archive | Hot, Cool, Archive |
| Access Control | Bucket policies, ACLs | IAM, ACLs | RBAC, SAS tokens |
| Private Access | VPC Gateway Endpoint | Private Google Access | Private Endpoint |

### 4. Private Endpoint

**Purpose**: Enable private connectivity to object storage

#### Implementation Comparison

| Cloud | Service | Cost | Configuration |
|-------|---------|------|---------------|
| **AWS** | VPC Gateway Endpoint | FREE | Attached to route tables |
| **GCP** | Private Google Access | FREE | Enabled on subnet |
| **Azure** | Private Endpoint | ~$7.30/month | Dedicated network interface |

**Note**: AWS and GCP offer FREE private access to their object storage services, while Azure charges for Private Endpoints.

### 5. Identity & Access Management

**Purpose**: Control access to resources

#### Role/Policy Examples

**AWS IAM Policy**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::bucket-name/*"
    }
  ]
}
```

**GCP IAM Binding**
```hcl
resource "google_storage_bucket_iam_member" "function" {
  bucket = google_storage_bucket.files.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.function.email}"
}
```

**Azure RBAC**
```hcl
resource "azurerm_role_assignment" "function" {
  scope                = azurerm_storage_account.files.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_linux_function_app.file_transfer.identity[0].principal_id
}
```

### 6. Secret Management

**Purpose**: Securely store SFTP credentials

#### Service Comparison

| Feature | AWS Secrets Manager | GCP Secret Manager | Azure Key Vault |
|---------|--------------------|--------------------|-----------------|
| Encryption | KMS | Cloud KMS | Key Vault managed |
| Versioning | Yes | Yes | Yes |
| Rotation | Automatic | Manual | Automatic |
| Cost | $0.40/secret/month + $0.05/10k API calls | $0.06/secret/month + $0.03/10k access | $0.03/secret/month + $0.03/10k operations |
| Access Control | IAM policies | IAM roles | RBAC |

---

## Deployment Patterns

### Pattern 1: Single-Cloud Deployment

Deploy on one cloud provider based on requirements:

```
Choose Cloud → Configure Network → Deploy Functions → Configure Storage → Test
```

**When to use**:
- Organization is committed to one cloud
- No multi-cloud requirements
- Optimizing for single cloud features

### Pattern 2: Multi-Cloud Active-Passive

Deploy on primary cloud, maintain standby in secondary:

```
Primary Cloud (Active) ↔ Replication ↔ Secondary Cloud (Passive)
```

**When to use**:
- Disaster recovery requirements
- Geographic redundancy
- Compliance with data residency

### Pattern 3: Multi-Cloud Active-Active

Deploy on multiple clouds simultaneously:

```
Cloud A ← Load Balancer/Router → Cloud B
```

**When to use**:
- High availability requirements
- Avoid vendor lock-in
- Geographic distribution

### Pattern 4: Cloud-Agnostic with Abstraction Layer

Use infrastructure abstraction tools (Terraform, Pulumi):

```
Universal Configuration → Cloud-Specific Deployment
```

**When to use**:
- Need flexibility to switch clouds
- Managing multiple cloud deployments
- Standardizing infrastructure

---

## Configuration Examples

### Environment Variables (All Clouds)

```bash
# Common variables
FUNCTION_NAME=secure-file-transfer
RUNTIME=python3.11
MEMORY_SIZE=512
TIMEOUT=300
NETWORK_CIDR=10.0.0.0/16

# Object storage
BUCKET_NAME=secure-transfer-files
STORAGE_CLASS=STANDARD

# SFTP configuration
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USERNAME=transfer_user
SFTP_REMOTE_PATH=/data/incoming

# Logging
LOG_LEVEL=INFO
LOG_RETENTION_DAYS=7
```

### Terraform Variables (Universal)

```hcl
variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "secure-transfer"
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
  default     = "dev"
}

variable "network_cidr" {
  description = "CIDR block for virtual network"
  type        = string
  default     = "10.0.0.0/16"
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "function_memory_mb" {
  description = "Memory allocation for serverless function"
  type        = number
  default     = 512
}

variable "function_timeout_seconds" {
  description = "Timeout for serverless function"
  type        = number
  default     = 300
}

variable "storage_lifecycle_days" {
  description = "Days before transitioning to cheaper storage"
  type        = map(number)
  default     = {
    standard_to_ia      = 30
    ia_to_glacier       = 90
    glacier_to_archive  = 180
  }
}
```

---

## Security Mappings

### Network Security

| Security Layer | AWS | GCP | Azure |
|----------------|-----|-----|-------|
| **Virtual Network** | VPC | VPC | Virtual Network |
| **Firewall Rules** | Security Groups | VPC Firewall Rules | Network Security Groups |
| **Network ACLs** | NACLs | VPC Firewall | NSG Rules |
| **Private DNS** | Route 53 Private | Cloud DNS Private | Private DNS Zones |
| **DDoS Protection** | AWS Shield | Cloud Armor | DDoS Protection |
| **Web Firewall** | AWS WAF | Cloud Armor | Azure Firewall |

### Data Security

| Security Feature | AWS | GCP | Azure |
|-----------------|-----|-----|-------|
| **Encryption at Rest** | SSE-S3/KMS | Google-managed/CMEK | SSE/Customer-managed |
| **Encryption in Transit** | TLS 1.2+ | TLS 1.2+ | TLS 1.2+ |
| **Key Management** | KMS | Cloud KMS | Key Vault |
| **Secret Storage** | Secrets Manager | Secret Manager | Key Vault |
| **Certificate Management** | ACM | Certificate Manager | Key Vault |

### Identity Security

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Service Identity** | IAM Roles | Service Accounts | Managed Identities |
| **Access Policies** | IAM Policies | IAM Bindings | RBAC |
| **MFA** | Yes | Yes | Yes |
| **Audit Logs** | CloudTrail | Cloud Audit Logs | Activity Logs |

---

## Monitoring & Logging

### Logging Services

| Feature | AWS CloudWatch | GCP Cloud Logging | Azure Monitor |
|---------|---------------|-------------------|---------------|
| **Log Collection** | Automatic for Lambda | Automatic for Cloud Functions | Automatic for Functions |
| **Log Retention** | Configurable (default 7 days) | 30 days default | 90 days default |
| **Log Query** | CloudWatch Insights | Log Explorer | Kusto Query Language |
| **Real-time Monitoring** | Yes | Yes | Yes |
| **Alerting** | CloudWatch Alarms | Alert Policies | Alert Rules |

### Metrics & Monitoring

| Metric Type | AWS | GCP | Azure |
|-------------|-----|-----|-------|
| **Function Invocations** | CloudWatch Metrics | Cloud Monitoring | Application Insights |
| **Function Duration** | CloudWatch Metrics | Cloud Monitoring | Application Insights |
| **Function Errors** | CloudWatch Metrics | Cloud Monitoring | Application Insights |
| **Storage Metrics** | S3 Metrics | GCS Metrics | Storage Metrics |
| **Network Metrics** | VPC Flow Logs | VPC Flow Logs | Network Watcher |

### Distributed Tracing

| Service | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Tracing Service** | X-Ray | Cloud Trace | Application Insights |
| **APM** | X-Ray | Cloud Profiler | Application Insights |

---

## Cost Comparison

### Monthly Cost Estimate (1,000 transfers, 100 MB avg file size)

#### AWS Cost Breakdown
| Service | Cost |
|---------|------|
| Lambda (1,000 invocations × 30s) | $0.25 |
| S3 Storage (100 GB) | $2.30 |
| S3 Requests (1,000 PUTs) | $0.01 |
| Secrets Manager | $0.40 |
| CloudWatch Logs | $0.05 |
| VPC Gateway Endpoint | $0.00 |
| **Total** | **~$3.00/month** |

#### GCP Cost Breakdown
| Service | Cost |
|---------|------|
| Cloud Functions (1,000 invocations × 30s) | $0.20 |
| Cloud Storage (100 GB) | $2.00 |
| Cloud Storage Operations (1,000) | $0.01 |
| Secret Manager | $0.06 |
| Cloud Logging | $0.50 |
| Private Google Access | $0.00 |
| **Total** | **~$2.77/month** |

#### Azure Cost Breakdown
| Service | Cost |
|---------|------|
| Azure Functions Premium (required for VNet) | $15.00 |
| Blob Storage (100 GB) | $1.84 |
| Storage Transactions (1,000) | $0.01 |
| Key Vault | $0.03 |
| Log Analytics | $0.10 |
| Private Endpoint | $7.30 |
| **Total** | **~$24.28/month** |

**Cost Analysis**:
- **GCP**: Most cost-effective (~7% cheaper than AWS)
- **AWS**: Very competitive, excellent for AWS-native workloads
- **Azure**: More expensive due to Premium Functions plan and Private Endpoint costs

### Cost Optimization Strategies

#### All Clouds
1. **Implement lifecycle policies** to move old data to cheaper storage
2. **Right-size function memory** based on actual usage
3. **Use reserved capacity** for predictable workloads
4. **Monitor and optimize** execution time
5. **Implement retention policies** for logs

#### Cloud-Specific
- **AWS**: Use S3 Intelligent-Tiering for automatic cost optimization
- **GCP**: Use Coldline/Archive storage for long-term retention
- **Azure**: Consider Consumption plan if VNet integration not required

---

## Migration Strategy

### Cross-Cloud Migration Steps

1. **Prepare**
   - Document current architecture
   - Identify cloud-specific dependencies
   - Plan data migration strategy

2. **Adapt Code**
   - Abstract cloud-specific SDK calls
   - Use environment variables for configuration
   - Implement cloud-agnostic interfaces

3. **Infrastructure as Code**
   - Create Terraform/Pulumi modules for each cloud
   - Use variables for cloud-specific resources
   - Test deployment in non-production

4. **Data Migration**
   - Use cloud transfer services (AWS DataSync, GCP Transfer Service, Azure Data Box)
   - Implement incremental sync
   - Validate data integrity

5. **Cutover**
   - Update DNS/routing
   - Monitor closely
   - Maintain rollback plan

### Cloud Transfer Services

| Source → Destination | Service | Cost |
|---------------------|---------|------|
| AWS → GCP | GCP Transfer Service | $0.12/GB |
| AWS → Azure | Azure Data Box / AzCopy | Variable |
| GCP → AWS | AWS DataSync | $0.0125/GB |
| GCP → Azure | gsutil + AzCopy | Free (egress charges apply) |
| Azure → AWS | AWS DataSync | $0.0125/GB |
| Azure → GCP | GCP Transfer Service | $0.12/GB |

---

## Best Practices

### Universal Best Practices

1. **Use Infrastructure as Code**
   - Version control all infrastructure
   - Use modules for reusability
   - Implement CI/CD for infrastructure

2. **Implement Least Privilege**
   - Grant minimum required permissions
   - Use service identities
   - Rotate credentials regularly

3. **Enable Encryption**
   - Encrypt at rest and in transit
   - Use managed encryption keys
   - Implement key rotation

4. **Monitor Everything**
   - Collect logs from all components
   - Set up alerts for errors
   - Track performance metrics

5. **Plan for Disaster Recovery**
   - Regular backups
   - Multi-region deployment
   - Test recovery procedures

6. **Optimize Costs**
   - Right-size resources
   - Implement lifecycle policies
   - Use spot/preemptible instances where possible

### Cloud-Specific Recommendations

#### AWS
- Use VPC Gateway Endpoints for S3 (free)
- Implement S3 Intelligent-Tiering
- Use CloudFormation StackSets for multi-region

#### GCP
- Enable Private Google Access (free)
- Use preemptible Cloud Functions for non-critical workloads
- Implement Organization Policies

#### Azure
- Use Managed Identities instead of service principals
- Implement Azure Policy for governance
- Use Azure Blueprints for standardization

---

## Conclusion

This infrastructure composer provides a **complete, universal mapping** of the secure file transfer solution across AWS, GCP, and Azure. Key takeaways:

1. **Architecture is portable** - Core patterns translate across clouds
2. **Services are equivalent** - Each cloud offers similar capabilities
3. **Costs vary significantly** - GCP/AWS are most cost-effective for this pattern
4. **Implementation differs** - Cloud-specific knowledge required
5. **Abstraction is possible** - IaC tools enable cloud-agnostic deployments

### Recommendations by Use Case

| Use Case | Recommended Cloud | Reason |
|----------|------------------|---------|
| **Cost-sensitive** | GCP | Lowest monthly cost (~$2.77) |
| **AWS ecosystem** | AWS | Best integration, mature services |
| **Enterprise Microsoft** | Azure | Integration with Microsoft ecosystem |
| **Multi-cloud strategy** | AWS + GCP | Best balance of features and cost |
| **Highest availability** | Multi-cloud | Eliminate single-cloud dependency |

---

## Additional Resources

### Documentation Links

**AWS**
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/)
- [VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html)

**GCP**
- [Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Private Google Access](https://cloud.google.com/vpc/docs/configure-private-google-access)

**Azure**
- [Azure Functions Documentation](https://docs.microsoft.com/azure/azure-functions/)
- [Blob Storage Documentation](https://docs.microsoft.com/azure/storage/blobs/)
- [Private Endpoints](https://docs.microsoft.com/azure/private-link/private-endpoint-overview)

### Infrastructure as Code Examples

See repository directories:
- `/terraform/aws/` - AWS implementation
- `/terraform/gcp/` - GCP implementation (to be added)
- `/terraform/azure/` - Azure implementation (to be added)

---

**Version**: 1.0  
**Last Updated**: 2025-12-21  
**Maintainer**: Infrastructure Team  
**License**: MIT
