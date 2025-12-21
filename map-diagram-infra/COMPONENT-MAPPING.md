# Universal Cloud Infrastructure Component Mapping

This document provides a comprehensive mapping of infrastructure components across AWS, GCP, and Azure platforms for the Secure File Transfer Solution.

## Architecture Overview

**Purpose**: Transfer files securely from legacy SFTP systems to cloud object storage using serverless functions in an isolated network environment with private connectivity.

---

## Component Mapping Table

| Universal Component | AWS | GCP | Azure | Purpose |
|---------------------|-----|-----|-------|---------|
| **Compute - Serverless Function** | Lambda | Cloud Functions | Azure Functions | Execute file transfer logic |
| **Storage - Object Storage** | S3 | Cloud Storage | Blob Storage | Store transferred files |
| **Network - Virtual Network** | VPC | VPC (Virtual Private Cloud) | Virtual Network (VNet) | Isolated network environment |
| **Network - Private Subnet** | Private Subnet | Subnet | Subnet | Network isolation for compute |
| **Network - Private Endpoint** | VPC Gateway Endpoint (S3) | Private Service Connect | Private Endpoint | Private connectivity to storage |
| **Network - Security Group** | Security Group | Firewall Rules | Network Security Group (NSG) | Control ingress/egress traffic |
| **Network - Route Table** | Route Table | Routes | Route Table | Control network routing |
| **Identity - Service Role** | IAM Role | Service Account | Managed Identity | Grant permissions to function |
| **Identity - Policy** | IAM Policy | IAM Policy / Roles | Role Assignment | Define permissions |
| **Secret Management** | Secrets Manager | Secret Manager | Key Vault | Store SFTP credentials |
| **Logging** | CloudWatch Logs | Cloud Logging | Azure Monitor Logs | Centralized logging |
| **Monitoring** | CloudWatch Metrics | Cloud Monitoring | Azure Monitor Metrics | Performance metrics |
| **Scheduler** | EventBridge | Cloud Scheduler | Logic Apps / Functions Timer | Scheduled execution |
| **Encryption - At Rest** | S3 SSE (AES-256) | CMEK / Google-managed | Storage Service Encryption | Encrypt stored data |
| **Encryption - In Transit** | TLS/HTTPS | TLS/HTTPS | TLS/HTTPS | Encrypt data in motion |
| **Resource Tagging** | Tags | Labels | Tags | Resource organization |

---

## Detailed Component Descriptions

### 1. Compute Layer - Serverless Function

**Universal Concept**: Event-driven, auto-scaling compute service that executes code without server management.

#### AWS: Lambda
```hcl
resource "aws_lambda_function" "file_transfer" {
  function_name = "file-transfer"
  runtime       = "python3.11"
  handler       = "lambda_function.lambda_handler"
  timeout       = 300
  memory_size   = 512
  vpc_config {
    subnet_ids         = [...]
    security_group_ids = [...]
  }
}
```

#### GCP: Cloud Functions (2nd Gen)
```hcl
resource "google_cloudfunctions2_function" "file_transfer" {
  name        = "file-transfer"
  runtime     = "python311"
  entry_point = "file_transfer_handler"
  
  service_config {
    timeout_seconds      = 300
    available_memory     = "512Mi"
    vpc_connector        = ...
  }
}
```

#### Azure: Azure Functions
```hcl
resource "azurerm_linux_function_app" "file_transfer" {
  name                       = "file-transfer"
  resource_group_name        = ...
  location                   = ...
  storage_account_name       = ...
  service_plan_id           = ...
  
  site_config {
    application_stack {
      python_version = "3.11"
    }
  }
  
  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME" = "python"
  }
}
```

**Key Differences**:
- **AWS**: Best VPC integration, most mature
- **GCP**: Simpler configuration, integrated with GCP services
- **Azure**: Strong integration with Azure ecosystem

---

### 2. Storage Layer - Object Storage

**Universal Concept**: Highly durable, scalable object storage for unstructured data.

#### AWS: S3
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
  }
}
```

#### GCP: Cloud Storage
```hcl
resource "google_storage_bucket" "file_transfer" {
  name     = "file-transfer-bucket"
  location = "US"
  
  versioning {
    enabled = true
  }
  
  encryption {
    default_kms_key_name = ...
  }
  
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }
}
```

#### Azure: Blob Storage
```hcl
resource "azurerm_storage_account" "file_transfer" {
  name                     = "filetransferstorage"
  resource_group_name      = ...
  location                 = ...
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  blob_properties {
    versioning_enabled = true
  }
}

resource "azurerm_storage_container" "files" {
  name                  = "transferred-files"
  storage_account_name  = azurerm_storage_account.file_transfer.name
  container_access_type = "private"
}
```

**Key Differences**:
- **AWS S3**: Most features, best lifecycle policies
- **GCP Cloud Storage**: Unified storage classes, simpler pricing
- **Azure Blob Storage**: Three blob types (Block, Page, Append)

---

### 3. Network Layer - Virtual Network

**Universal Concept**: Isolated virtual network for cloud resources.

#### AWS: VPC (Virtual Private Cloud)
```hcl
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_subnet" "private" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = false
}
```

#### GCP: VPC (Virtual Private Cloud)
```hcl
resource "google_compute_network" "main" {
  name                    = "file-transfer-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "private" {
  name          = "private-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = "us-central1"
  network       = google_compute_network.main.id
  
  private_ip_google_access = true
}
```

#### Azure: Virtual Network (VNet)
```hcl
resource "azurerm_virtual_network" "main" {
  name                = "file-transfer-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = ...
  resource_group_name = ...
}

resource "azurerm_subnet" "private" {
  name                 = "private-subnet"
  resource_group_name  = ...
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
  
  delegation {
    name = "functions-delegation"
    service_delegation {
      name = "Microsoft.Web/serverFarms"
    }
  }
}
```

**Key Differences**:
- **AWS VPC**: Most granular control, multi-AZ by default
- **GCP VPC**: Global resource, automatic multi-region
- **Azure VNet**: Regional resource, requires explicit peering

---

### 4. Network Layer - Private Endpoint/Service Connectivity

**Universal Concept**: Private connection from VPC to cloud services without internet exposure.

#### AWS: VPC Gateway Endpoint (for S3)
```hcl
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private.id]
}

resource "aws_vpc_endpoint_policy" "s3" {
  vpc_endpoint_id = aws_vpc_endpoint.s3.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { AWS = aws_iam_role.lambda.arn }
      Action = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"]
      Resource = [aws_s3_bucket.file_transfer.arn, "${aws_s3_bucket.file_transfer.arn}/*"]
    }]
  })
}
```

#### GCP: Private Service Connect
```hcl
resource "google_compute_global_address" "private_ip" {
  name          = "private-service-connect"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.main.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.main.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip.name]
}
```

#### Azure: Private Endpoint
```hcl
resource "azurerm_private_endpoint" "storage" {
  name                = "storage-private-endpoint"
  location            = ...
  resource_group_name = ...
  subnet_id           = azurerm_subnet.private.id

  private_service_connection {
    name                           = "storage-privateserviceconnection"
    private_connection_resource_id = azurerm_storage_account.file_transfer.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }
}
```

**Key Differences**:
- **AWS**: Gateway endpoints are FREE for S3/DynamoDB
- **GCP**: Uses VPC Service Controls and Private Service Connect
- **Azure**: Private Endpoints have hourly charges

**Cost Comparison**:
- **AWS VPC Gateway Endpoint (S3)**: $0.00/hour, $0.00/GB
- **GCP Private Service Connect**: ~$0.01/hour per endpoint
- **Azure Private Endpoint**: ~$0.01/hour per endpoint

---

### 5. Security Layer - Firewall Rules

**Universal Concept**: Stateful firewall controlling network traffic.

#### AWS: Security Group
```hcl
resource "aws_security_group" "lambda" {
  name        = "lambda-sg"
  description = "Security group for Lambda function"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS to S3 via Gateway Endpoint"
  }

  egress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SFTP access"
  }
}
```

#### GCP: Firewall Rules
```hcl
resource "google_compute_firewall" "egress_https" {
  name    = "allow-egress-https"
  network = google_compute_network.main.name
  direction = "EGRESS"

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }

  destination_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "egress_sftp" {
  name    = "allow-egress-sftp"
  network = google_compute_network.main.name
  direction = "EGRESS"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  destination_ranges = ["0.0.0.0/0"]
}
```

#### Azure: Network Security Group
```hcl
resource "azurerm_network_security_group" "lambda" {
  name                = "function-nsg"
  location            = ...
  resource_group_name = ...

  security_rule {
    name                       = "allow-https-outbound"
    priority                   = 100
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "allow-sftp-outbound"
    priority                   = 110
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}
```

**Key Differences**:
- **AWS**: Security Groups are stateful, attached to resources
- **GCP**: Firewall rules are network-wide, applied by tags/service accounts
- **Azure**: NSGs can be attached to subnets or NICs

---

### 6. Identity & Access Management

**Universal Concept**: Grant permissions to cloud resources using roles and policies.

#### AWS: IAM Role + Policies
```hcl
resource "aws_iam_role" "lambda" {
  name = "lambda-file-transfer-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_policy" "lambda_s3" {
  name = "lambda-s3-access"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["s3:PutObject", "s3:PutObjectAcl"]
      Resource = "${aws_s3_bucket.file_transfer.arn}/*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_s3" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_s3.arn
}
```

#### GCP: Service Account + IAM Bindings
```hcl
resource "google_service_account" "function" {
  account_id   = "file-transfer-function"
  display_name = "File Transfer Function Service Account"
}

resource "google_storage_bucket_iam_member" "function_storage_admin" {
  bucket = google_storage_bucket.file_transfer.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.function.email}"
}

resource "google_cloudfunctions2_function_iam_member" "invoker" {
  project        = google_cloudfunctions2_function.file_transfer.project
  location       = google_cloudfunctions2_function.file_transfer.location
  cloud_function = google_cloudfunctions2_function.file_transfer.name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${google_service_account.function.email}"
}
```

#### Azure: Managed Identity + Role Assignments
```hcl
resource "azurerm_user_assigned_identity" "function" {
  name                = "file-transfer-identity"
  resource_group_name = ...
  location            = ...
}

resource "azurerm_role_assignment" "storage_blob_contributor" {
  scope                = azurerm_storage_account.file_transfer.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.function.principal_id
}

resource "azurerm_linux_function_app" "file_transfer" {
  # ... other config ...
  
  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.function.id]
  }
}
```

**Key Differences**:
- **AWS**: Most granular IAM policies, supports resource-based policies
- **GCP**: Service accounts are email addresses, simpler model
- **Azure**: Managed Identities eliminate credential management

---

### 7. Secret Management

**Universal Concept**: Securely store and retrieve sensitive credentials.

#### AWS: Secrets Manager
```hcl
resource "aws_secretsmanager_secret" "sftp_credentials" {
  name_prefix             = "sftp-credentials-"
  description             = "SFTP credentials for legacy system"
  recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret_version" "sftp_credentials" {
  secret_id = aws_secretsmanager_secret.sftp_credentials.id
  secret_string = jsonencode({
    username = var.sftp_username
    password = var.sftp_password
    host     = var.sftp_host
    port     = var.sftp_port
  })
}
```

#### GCP: Secret Manager
```hcl
resource "google_secret_manager_secret" "sftp_credentials" {
  secret_id = "sftp-credentials"
  
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "sftp_credentials" {
  secret = google_secret_manager_secret.sftp_credentials.id
  
  secret_data = jsonencode({
    username = var.sftp_username
    password = var.sftp_password
    host     = var.sftp_host
    port     = var.sftp_port
  })
}

resource "google_secret_manager_secret_iam_member" "function_accessor" {
  secret_id = google_secret_manager_secret.sftp_credentials.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.function.email}"
}
```

#### Azure: Key Vault
```hcl
resource "azurerm_key_vault" "main" {
  name                = "file-transfer-kv"
  location            = ...
  resource_group_name = ...
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
}

resource "azurerm_key_vault_secret" "sftp_credentials" {
  name         = "sftp-credentials"
  value        = jsonencode({
    username = var.sftp_username
    password = var.sftp_password
    host     = var.sftp_host
    port     = var.sftp_port
  })
  key_vault_id = azurerm_key_vault.main.id
}

resource "azurerm_key_vault_access_policy" "function" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_user_assigned_identity.function.principal_id

  secret_permissions = ["Get", "List"]
}
```

**Key Differences**:
- **AWS Secrets Manager**: Automatic rotation, pay per secret
- **GCP Secret Manager**: Version-based, automatic replication
- **Azure Key Vault**: Supports keys, secrets, and certificates

---

### 8. Logging & Monitoring

**Universal Concept**: Centralized logging and metrics collection.

#### AWS: CloudWatch
```hcl
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/file-transfer"
  retention_in_days = 7
}

resource "aws_iam_policy" "lambda_logs" {
  name = "lambda-logs-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["logs:CreateLogStream", "logs:PutLogEvents"]
      Resource = "${aws_cloudwatch_log_group.lambda.arn}:*"
    }]
  })
}
```

#### GCP: Cloud Logging
```hcl
# Cloud Functions automatically logs to Cloud Logging
# No additional configuration needed for basic logging

resource "google_logging_project_sink" "function_logs" {
  name        = "function-logs-sink"
  destination = "storage.googleapis.com/${google_storage_bucket.logs.name}"
  
  filter = "resource.type=cloud_function AND resource.labels.function_name=file-transfer"
  
  unique_writer_identity = true
}
```

#### Azure: Application Insights
```hcl
resource "azurerm_application_insights" "function" {
  name                = "file-transfer-insights"
  location            = ...
  resource_group_name = ...
  application_type    = "web"
}

resource "azurerm_linux_function_app" "file_transfer" {
  # ... other config ...
  
  app_settings = {
    "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.function.instrumentation_key
  }
}
```

**Key Differences**:
- **AWS CloudWatch**: Unified metrics and logs, custom dashboards
- **GCP Cloud Logging**: Stackdriver-based, integrated with GCP services
- **Azure Application Insights**: APM focused, rich analytics

---

### 9. Scheduling

**Universal Concept**: Trigger serverless functions on a schedule.

#### AWS: EventBridge
```hcl
resource "aws_cloudwatch_event_rule" "schedule" {
  name                = "file-transfer-schedule"
  description         = "Trigger file transfer every hour"
  schedule_expression = "rate(1 hour)"
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.schedule.name
  target_id = "lambda"
  arn       = aws_lambda_function.file_transfer.arn
}

resource "aws_lambda_permission" "eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.file_transfer.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule.arn
}
```

#### GCP: Cloud Scheduler
```hcl
resource "google_cloud_scheduler_job" "function_trigger" {
  name        = "file-transfer-schedule"
  description = "Trigger file transfer every hour"
  schedule    = "0 * * * *"  # Cron format
  time_zone   = "America/New_York"

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.file_transfer.service_config[0].uri
    
    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}
```

#### Azure: Timer Trigger
```hcl
# Azure Functions uses code-based timer triggers
# In function.json or attributes:

# function.json
{
  "bindings": [
    {
      "name": "myTimer",
      "type": "timerTrigger",
      "direction": "in",
      "schedule": "0 0 * * * *"
    }
  ]
}

# Or use Logic Apps for external scheduling
resource "azurerm_logic_app_workflow" "schedule" {
  name                = "file-transfer-schedule"
  location            = ...
  resource_group_name = ...
}
```

**Key Differences**:
- **AWS EventBridge**: Most flexible, supports complex patterns
- **GCP Cloud Scheduler**: Simple cron-based scheduling
- **Azure**: Timer triggers in code or Logic Apps for orchestration

---

## Architecture Patterns Comparison

### Pattern: Serverless File Transfer with Private Storage Access

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Cold Start** | ~1-2s (Python) | ~1-2s (Python) | ~2-3s (Python) |
| **Max Timeout** | 15 min (Lambda) | 60 min (Cloud Functions 2nd gen) | 10 min (Consumption plan) |
| **VPC Integration** | Native, mature | VPC Connector required | VNet Integration required |
| **Private Storage** | FREE (Gateway Endpoint) | Included (Private Google Access) | ~$7.20/month (Private Endpoint) |
| **Secrets Management** | $0.40/secret/month | $0.06/secret/month | $0.03/secret/month |
| **Function Cost** | $0.20/1M requests | $0.40/1M requests | $0.20/1M requests |
| **Logging Cost** | $0.50/GB | Free (50GB/month) | $2.30/GB |

---

## Cost Comparison (Monthly)

**Scenario**: 1,000 file transfers per month, 100MB average file size, 30s execution time

| Component | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| Compute (1K invocations) | $0.25 | $0.40 | $0.20 |
| Storage (100GB) | $2.30 | $2.00 | $2.05 |
| Network (Private Endpoint) | **$0.00** | **$0.00** | $7.20 |
| Secrets | $0.40 | $0.06 | $0.03 |
| Logging | $0.50 | $0.00 | $2.30 |
| **TOTAL** | **$3.45** | **$2.46** | **$11.78** |

**Winner for Cost**: **GCP** (29% cheaper than AWS, 79% cheaper than Azure)

**Best for Features**: **AWS** (FREE S3 Gateway Endpoint, best VPC integration)

**Best for Simplicity**: **GCP** (Automatic logging, simpler networking)

---

## Migration Guide

### AWS → GCP
1. Replace Lambda with Cloud Functions (2nd gen)
2. Replace S3 with Cloud Storage
3. Replace VPC Gateway Endpoint with Private Google Access
4. Replace IAM Roles with Service Accounts
5. Replace Secrets Manager with Secret Manager
6. Replace EventBridge with Cloud Scheduler

### AWS → Azure
1. Replace Lambda with Azure Functions
2. Replace S3 with Blob Storage
3. Replace VPC with VNet
4. Replace VPC Gateway Endpoint with Private Endpoint
5. Replace IAM Roles with Managed Identities
6. Replace Secrets Manager with Key Vault
7. Replace EventBridge with Logic Apps

### GCP → Azure
1. Replace Cloud Functions with Azure Functions
2. Replace Cloud Storage with Blob Storage
3. Replace VPC with VNet
4. Replace Service Accounts with Managed Identities
5. Replace Secret Manager with Key Vault
6. Replace Cloud Scheduler with Logic Apps

---

## Best Practices (Universal)

1. **Network Isolation**
   - Always deploy serverless functions in private network
   - Use private endpoints for storage access
   - Minimize internet exposure

2. **Security**
   - Use managed identities/service accounts (never hardcode credentials)
   - Enable encryption at rest and in transit
   - Apply principle of least privilege
   - Use secret management services

3. **Cost Optimization**
   - Implement storage lifecycle policies
   - Right-size function memory and timeout
   - Use reserved capacity for predictable workloads
   - Monitor and optimize cold starts

4. **Observability**
   - Enable detailed logging
   - Set up monitoring and alerting
   - Track cost metrics
   - Implement distributed tracing

5. **Reliability**
   - Implement retry logic with exponential backoff
   - Use dead letter queues for failed executions
   - Design for idempotency
   - Test disaster recovery procedures

---

## Conclusion

This component mapping enables teams to:
- Understand equivalent services across cloud providers
- Estimate costs for multi-cloud deployments
- Plan migration strategies
- Choose the best cloud provider for specific requirements

**Recommendation**: 
- Choose **AWS** if you need FREE private storage access and best-in-class VPC integration
- Choose **GCP** if you prioritize simplicity and cost efficiency
- Choose **Azure** if you're already invested in Microsoft ecosystem
