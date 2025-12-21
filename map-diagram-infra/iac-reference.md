# Infrastructure-as-Code Reference

Complete Infrastructure-as-Code examples for deploying the secure file transfer solution on AWS, GCP, and Azure using Terraform.

## Table of Contents

1. [AWS Terraform](#aws-terraform)
2. [GCP Terraform](#gcp-terraform)
3. [Azure Terraform](#azure-terraform)
4. [Comparison Matrix](#comparison-matrix)

---

## AWS Terraform

### Directory Structure

```
terraform-aws/
├── main.tf
├── variables.tf
├── outputs.tf
├── vpc.tf
├── s3.tf
├── lambda.tf
├── iam.tf
├── secrets.tf
└── terraform.tfvars
```

### main.tf

```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "file-transfer/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
```

### variables.tf

```hcl
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "file-transfer"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "availability_zones" {
  description = "Availability zones for subnets"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "lambda_memory" {
  description = "Lambda function memory in MB"
  type        = number
  default     = 512
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 300
}

variable "sftp_port" {
  description = "SFTP server port"
  type        = number
  default     = 22
}

variable "sftp_host" {
  description = "SFTP server hostname"
  type        = string
  default     = "sftp.example.com"
}

variable "sftp_username" {
  description = "SFTP username (template only)"
  type        = string
  default     = "placeholder"
}

variable "sftp_remote_path" {
  description = "Remote path on SFTP server"
  type        = string
  default     = "/incoming"
}

variable "log_retention_days" {
  description = "CloudWatch Logs retention in days"
  type        = number
  default     = 7
}

variable "enable_scheduler" {
  description = "Enable EventBridge scheduler"
  type        = bool
  default     = false
}

variable "schedule_expression" {
  description = "EventBridge schedule expression"
  type        = string
  default     = "cron(0 2 * * ? *)"
}
```

### vpc.tf

```hcl
# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-${var.environment}-vpc"
  }
}

# Private Subnets
resource "aws_subnet" "private" {
  count                   = length(var.private_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.private_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = false

  tags = {
    Name = "${var.project_name}-${var.environment}-private-subnet-${count.index + 1}"
    Tier = "Private"
  }
}

# Route Table for Private Subnets
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-${var.environment}-private-rt"
  }
}

# Route Table Associations
resource "aws_route_table_association" "private" {
  count          = length(var.private_subnet_cidrs)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

# Security Group for Lambda
resource "aws_security_group" "lambda" {
  name        = "${var.project_name}-${var.environment}-lambda-sg"
  description = "Security group for Lambda function with VPC access"
  vpc_id      = aws_vpc.main.id

  # Egress to S3 via Gateway Endpoint
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS to S3 via Gateway Endpoint"
  }

  # Egress to SFTP server
  egress {
    from_port   = var.sftp_port
    to_port     = var.sftp_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SFTP access to legacy system"
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-lambda-sg"
  }
}
```

### s3.tf

```hcl
# S3 Bucket
resource "aws_s3_bucket" "files" {
  bucket_prefix = "${var.project_name}-${var.environment}-files-"

  tags = {
    Name = "${var.project_name}-${var.environment}-file-transfer-bucket"
  }
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "files" {
  bucket = aws_s3_bucket.files.id

  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "files" {
  bucket = aws_s3_bucket.files.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

# S3 Bucket Public Access Block
resource "aws_s3_bucket_public_access_block" "files" {
  bucket = aws_s3_bucket.files.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# S3 Lifecycle Configuration
resource "aws_s3_bucket_lifecycle_configuration" "files" {
  bucket = aws_s3_bucket.files.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER_IR"
    }

    transition {
      days          = 180
      storage_class = "DEEP_ARCHIVE"
    }
  }

  rule {
    id     = "expire-old-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

# S3 VPC Gateway Endpoint
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.${var.aws_region}.s3"
  vpc_endpoint_type = "Gateway"

  route_table_ids = [aws_route_table.private.id]

  tags = {
    Name = "${var.project_name}-${var.environment}-s3-gateway-endpoint"
  }
}

# VPC Endpoint Policy
resource "aws_vpc_endpoint_policy" "s3" {
  vpc_endpoint_id = aws_vpc_endpoint.s3.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.lambda.arn
        }
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl",
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.files.arn,
          "${aws_s3_bucket.files.arn}/*"
        ]
      }
    ]
  })
}
```

### lambda.tf

```hcl
# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.project_name}-${var.environment}-file-transfer"
  retention_in_days = var.log_retention_days

  tags = {
    Name = "${var.project_name}-${var.environment}-lambda-logs"
  }
}

# Lambda Function
resource "aws_lambda_function" "file_transfer" {
  filename         = "${path.module}/lambda_function.zip"
  function_name    = "${var.project_name}-${var.environment}-file-transfer"
  role             = aws_iam_role.lambda.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("${path.module}/lambda_function.zip")
  runtime          = "python3.11"
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory

  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      S3_BUCKET_NAME   = aws_s3_bucket.files.id
      SFTP_SECRET_ARN  = aws_secretsmanager_secret.sftp_credentials.arn
      SFTP_REMOTE_PATH = var.sftp_remote_path
      LOG_LEVEL        = "INFO"
      ENVIRONMENT      = var.environment
    }
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-file-transfer"
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda,
    aws_iam_role_policy_attachment.lambda_s3,
    aws_iam_role_policy_attachment.lambda_logs,
    aws_iam_role_policy_attachment.lambda_vpc,
    aws_iam_role_policy_attachment.lambda_secrets
  ]
}

# EventBridge Rule (Optional Scheduler)
resource "aws_cloudwatch_event_rule" "schedule" {
  count               = var.enable_scheduler ? 1 : 0
  name                = "${var.project_name}-${var.environment}-schedule"
  description         = "Trigger file transfer Lambda on schedule"
  schedule_expression = var.schedule_expression
  state               = "ENABLED"
}

# EventBridge Target
resource "aws_cloudwatch_event_target" "lambda" {
  count = var.enable_scheduler ? 1 : 0
  rule  = aws_cloudwatch_event_rule.schedule[0].name
  arn   = aws_lambda_function.file_transfer.arn
}

# Lambda Permission for EventBridge
resource "aws_lambda_permission" "eventbridge" {
  count         = var.enable_scheduler ? 1 : 0
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.file_transfer.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule[0].arn
}
```

### iam.tf

```hcl
# Lambda Execution Role
resource "aws_iam_role" "lambda" {
  name_prefix = "${var.project_name}-${var.environment}-lambda-"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-${var.environment}-lambda-role"
  }
}

# S3 Access Policy
resource "aws_iam_policy" "lambda_s3" {
  name_prefix = "${var.project_name}-${var.environment}-lambda-s3-"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl"
        ]
        Resource = "${aws_s3_bucket.files.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.files.arn
      }
    ]
  })
}

# CloudWatch Logs Policy
resource "aws_iam_policy" "lambda_logs" {
  name_prefix = "${var.project_name}-${var.environment}-lambda-logs-"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "${aws_cloudwatch_log_group.lambda.arn}:*"
      }
    ]
  })
}

# VPC Access Policy
resource "aws_iam_policy" "lambda_vpc" {
  name_prefix = "${var.project_name}-${var.environment}-lambda-vpc-"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface",
          "ec2:AssignPrivateIpAddresses",
          "ec2:UnassignPrivateIpAddresses"
        ]
        Resource = "*"
      }
    ]
  })
}

# Secrets Manager Access Policy
resource "aws_iam_policy" "lambda_secrets" {
  name_prefix = "${var.project_name}-${var.environment}-lambda-secrets-"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = aws_secretsmanager_secret.sftp_credentials.arn
      }
    ]
  })
}

# Attach Policies
resource "aws_iam_role_policy_attachment" "lambda_s3" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_s3.arn
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_logs.arn
}

resource "aws_iam_role_policy_attachment" "lambda_vpc" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_vpc.arn
}

resource "aws_iam_role_policy_attachment" "lambda_secrets" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_secrets.arn
}
```

### secrets.tf

```hcl
# Secrets Manager Secret
resource "aws_secretsmanager_secret" "sftp_credentials" {
  name_prefix             = "${var.project_name}-${var.environment}-sftp-"
  description             = "SFTP credentials for file transfer"
  recovery_window_in_days = 7

  tags = {
    Name = "${var.project_name}-${var.environment}-sftp-credentials"
  }
}

# Secret Version (Template - Update After Deploy)
resource "aws_secretsmanager_secret_version" "sftp_credentials" {
  secret_id = aws_secretsmanager_secret.sftp_credentials.id

  secret_string = jsonencode({
    username    = var.sftp_username
    password    = ""
    private_key = ""
    host        = var.sftp_host
    port        = var.sftp_port
  })

  lifecycle {
    ignore_changes = [secret_string]
  }
}
```

### outputs.tf

```hcl
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.files.id
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.file_transfer.function_name
}

output "lambda_function_arn" {
  description = "Lambda function ARN"
  value       = aws_lambda_function.file_transfer.arn
}

output "sftp_secret_arn" {
  description = "Secrets Manager secret ARN"
  value       = aws_secretsmanager_secret.sftp_credentials.arn
}

output "cloudwatch_log_group" {
  description = "CloudWatch Log Group name"
  value       = aws_cloudwatch_log_group.lambda.name
}

output "s3_gateway_endpoint_id" {
  description = "S3 Gateway Endpoint ID"
  value       = aws_vpc_endpoint.s3.id
}
```

---

## GCP Terraform

### Directory Structure

```
terraform-gcp/
├── main.tf
├── variables.tf
├── outputs.tf
├── network.tf
├── storage.tf
├── function.tf
├── iam.tf
├── secrets.tf
└── terraform.tfvars
```

### main.tf

```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  
  backend "gcs" {
    bucket = "terraform-state-bucket"
    prefix = "file-transfer"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_project" "current" {}
```

### variables.tf

```hcl
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-east1"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "network_cidr" {
  description = "Network CIDR range"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "Subnet CIDR range"
  type        = string
  default     = "10.0.1.0/24"
}

variable "function_memory" {
  description = "Function memory in MB"
  type        = number
  default     = 512
}

variable "function_timeout" {
  description = "Function timeout in seconds"
  type        = number
  default     = 540
}
```

### network.tf

```hcl
# VPC Network
resource "google_compute_network" "main" {
  name                    = "file-transfer-${var.environment}-vpc"
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
}

# Subnet
resource "google_compute_subnetwork" "private" {
  name          = "file-transfer-${var.environment}-subnet"
  ip_cidr_range = var.subnet_cidr
  region        = var.region
  network       = google_compute_network.main.id
  
  private_ip_google_access = true
}

# VPC Access Connector
resource "google_vpc_access_connector" "connector" {
  name          = "file-transfer-${var.environment}-connector"
  region        = var.region
  network       = google_compute_network.main.name
  ip_cidr_range = "10.8.0.0/28"
  
  min_instances = 2
  max_instances = 10
}

# Firewall Rules
resource "google_compute_firewall" "allow_egress" {
  name    = "file-transfer-${var.environment}-allow-egress"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["22", "443"]
  }

  direction          = "EGRESS"
  destination_ranges = ["0.0.0.0/0"]
}
```

### storage.tf

```hcl
# Cloud Storage Bucket
resource "google_storage_bucket" "files" {
  name          = "${var.project_id}-file-transfer-${var.environment}"
  location      = var.region
  storage_class = "STANDARD"
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
  
  encryption {
    default_kms_key_name = google_kms_crypto_key.storage.id
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
  
  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }
  
  lifecycle_rule {
    condition {
      age = 180
    }
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
  }
}

# KMS Key Ring
resource "google_kms_key_ring" "main" {
  name     = "file-transfer-${var.environment}"
  location = var.region
}

# KMS Crypto Key
resource "google_kms_crypto_key" "storage" {
  name     = "storage-key"
  key_ring = google_kms_key_ring.main.id
  
  lifecycle {
    prevent_destroy = true
  }
}
```

### function.tf

```hcl
# Cloud Function Gen 2
resource "google_cloudfunctions2_function" "file_transfer" {
  name     = "file-transfer-${var.environment}"
  location = var.region
  
  build_config {
    runtime     = "python311"
    entry_point = "transfer_files"
    
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.function_code.name
      }
    }
  }
  
  service_config {
    max_instance_count    = 10
    min_instance_count    = 0
    available_memory      = "${var.function_memory}M"
    timeout_seconds       = var.function_timeout
    service_account_email = google_service_account.function.email
    
    vpc_connector                 = google_vpc_access_connector.connector.id
    vpc_connector_egress_settings = "PRIVATE_RANGES_ONLY"
    
    environment_variables = {
      BUCKET_NAME      = google_storage_bucket.files.name
      SECRET_ID        = google_secret_manager_secret.sftp_credentials.secret_id
      ENVIRONMENT      = var.environment
      LOG_LEVEL        = "INFO"
    }
  }
}

# Function Source Bucket
resource "google_storage_bucket" "function_source" {
  name     = "${var.project_id}-function-source-${var.environment}"
  location = var.region
}

# Function Code Upload
resource "google_storage_bucket_object" "function_code" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.function_source.name
  source = "${path.module}/function-source.zip"
}

# Cloud Scheduler Job
resource "google_cloud_scheduler_job" "trigger" {
  name             = "file-transfer-${var.environment}-schedule"
  description      = "Trigger file transfer function"
  schedule         = "0 2 * * *"
  time_zone        = "America/New_York"
  attempt_deadline = "320s"
  
  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.file_transfer.service_config[0].uri
    
    oidc_token {
      service_account_email = google_service_account.function.email
    }
  }
}
```

### iam.tf

```hcl
# Service Account
resource "google_service_account" "function" {
  account_id   = "file-transfer-${var.environment}"
  display_name = "File Transfer Function SA"
}

# Storage Admin Role
resource "google_storage_bucket_iam_member" "function_storage" {
  bucket = google_storage_bucket.files.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.function.email}"
}

# Secret Accessor Role
resource "google_secret_manager_secret_iam_member" "function_secrets" {
  secret_id = google_secret_manager_secret.sftp_credentials.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.function.email}"
}

# Logs Writer Role
resource "google_project_iam_member" "function_logs" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.function.email}"
}
```

### secrets.tf

```hcl
# Secret Manager Secret
resource "google_secret_manager_secret" "sftp_credentials" {
  secret_id = "sftp-credentials-${var.environment}"
  
  replication {
    automatic = true
  }
}

# Secret Version
resource "google_secret_manager_secret_version" "sftp_credentials" {
  secret = google_secret_manager_secret.sftp_credentials.id
  
  secret_data = jsonencode({
    username = "placeholder"
    password = ""
    host     = "sftp.example.com"
    port     = 22
  })
  
  lifecycle {
    ignore_changes = [secret_data]
  }
}
```

### outputs.tf

```hcl
output "function_url" {
  value = google_cloudfunctions2_function.file_transfer.service_config[0].uri
}

output "bucket_name" {
  value = google_storage_bucket.files.name
}

output "secret_id" {
  value = google_secret_manager_secret.sftp_credentials.secret_id
}
```

---

## Azure Terraform

### Directory Structure

```
terraform-azure/
├── main.tf
├── variables.tf
├── outputs.tf
├── network.tf
├── storage.tf
├── function.tf
├── keyvault.tf
└── terraform.tfvars
```

### main.tf

```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstate"
    container_name       = "tfstate"
    key                  = "file-transfer.tfstate"
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = false
    }
  }
}

data "azurerm_client_config" "current" {}
```

### variables.tf

```hcl
variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "environment" {
  description = "Environment"
  type        = string
  default     = "dev"
}

variable "vnet_cidr" {
  description = "VNet CIDR"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "subnet_cidr" {
  description = "Subnet CIDR"
  type        = list(string)
  default     = ["10.0.1.0/24"]
}
```

### network.tf

```hcl
# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "rg-file-transfer-${var.environment}"
  location = var.location
}

# Virtual Network
resource "azurerm_virtual_network" "main" {
  name                = "vnet-file-transfer-${var.environment}"
  address_space       = var.vnet_cidr
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

# Subnet
resource "azurerm_subnet" "function" {
  name                 = "snet-function"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = var.subnet_cidr
  
  delegation {
    name = "function-delegation"
    
    service_delegation {
      name = "Microsoft.Web/serverFarms"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/action"
      ]
    }
  }
  
  service_endpoints = ["Microsoft.Storage", "Microsoft.KeyVault"]
}
```

### storage.tf

```hcl
# Storage Account
resource "azurerm_storage_account" "files" {
  name                     = "stfiletransfer${var.environment}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  blob_properties {
    versioning_enabled = true
    
    container_delete_retention_policy {
      days = 7
    }
  }
  
  network_rules {
    default_action             = "Deny"
    virtual_network_subnet_ids = [azurerm_subnet.function.id]
  }
}

# Blob Container
resource "azurerm_storage_container" "files" {
  name                  = "files"
  storage_account_name  = azurerm_storage_account.files.name
  container_access_type = "private"
}

# Lifecycle Management
resource "azurerm_storage_management_policy" "lifecycle" {
  storage_account_id = azurerm_storage_account.files.id
  
  rule {
    name    = "tier-policy"
    enabled = true
    
    filters {
      blob_types = ["blockBlob"]
    }
    
    actions {
      base_blob {
        tier_to_cool_after_days_since_modification_greater_than    = 30
        tier_to_archive_after_days_since_modification_greater_than = 90
      }
    }
  }
}
```

### function.tf

```hcl
# App Service Plan (Premium)
resource "azurerm_service_plan" "function" {
  name                = "plan-file-transfer-${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "EP1"
}

# Function App
resource "azurerm_linux_function_app" "main" {
  name                = "func-file-transfer-${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  
  storage_account_name       = azurerm_storage_account.files.name
  storage_account_access_key = azurerm_storage_account.files.primary_access_key
  service_plan_id            = azurerm_service_plan.function.id
  
  site_config {
    application_stack {
      python_version = "3.11"
    }
    
    vnet_route_all_enabled = true
  }
  
  virtual_network_subnet_id = azurerm_subnet.function.id
  
  app_settings = {
    "BUCKET_NAME"  = azurerm_storage_container.files.name
    "VAULT_URL"    = azurerm_key_vault.main.vault_uri
    "ENVIRONMENT"  = var.environment
    "LOG_LEVEL"    = "INFO"
  }
  
  identity {
    type = "SystemAssigned"
  }
}

# RBAC - Storage Blob Data Contributor
resource "azurerm_role_assignment" "function_storage" {
  scope                = azurerm_storage_account.files.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_linux_function_app.main.identity[0].principal_id
}
```

### keyvault.tf

```hcl
# Key Vault
resource "azurerm_key_vault" "main" {
  name                = "kv-filetrans-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
  
  network_acls {
    default_action             = "Deny"
    bypass                     = "AzureServices"
    virtual_network_subnet_ids = [azurerm_subnet.function.id]
  }
}

# Key Vault Access Policy for Function
resource "azurerm_key_vault_access_policy" "function" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_linux_function_app.main.identity[0].principal_id
  
  secret_permissions = [
    "Get",
    "List"
  ]
}

# SFTP Credentials Secret
resource "azurerm_key_vault_secret" "sftp_credentials" {
  name         = "sftp-credentials"
  value        = jsonencode({
    username = "placeholder"
    password = ""
    host     = "sftp.example.com"
    port     = 22
  })
  key_vault_id = azurerm_key_vault.main.id
  
  lifecycle {
    ignore_changes = [value]
  }
  
  depends_on = [azurerm_key_vault_access_policy.function]
}
```

### outputs.tf

```hcl
output "function_name" {
  value = azurerm_linux_function_app.main.name
}

output "storage_account_name" {
  value = azurerm_storage_account.files.name
}

output "key_vault_uri" {
  value = azurerm_key_vault.main.vault_uri
}
```

---

## Comparison Matrix

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Provider Blocks** | `hashicorp/aws` | `hashicorp/google` | `hashicorp/azurerm` |
| **Backend** | S3 | GCS | Azure Storage |
| **Network Resource** | `aws_vpc` | `google_compute_network` | `azurerm_virtual_network` |
| **Subnet Resource** | `aws_subnet` | `google_compute_subnetwork` | `azurerm_subnet` |
| **Function Resource** | `aws_lambda_function` | `google_cloudfunctions2_function` | `azurerm_linux_function_app` |
| **Storage Resource** | `aws_s3_bucket` | `google_storage_bucket` | `azurerm_storage_account` |
| **Secrets Resource** | `aws_secretsmanager_secret` | `google_secret_manager_secret` | `azurerm_key_vault_secret` |
| **IAM Role** | `aws_iam_role` | `google_service_account` | Managed Identity (implicit) |
| **Private Endpoint** | `aws_vpc_endpoint` (Gateway) | `google_vpc_access_connector` | `azurerm_subnet` (delegation) |
| **Scheduler** | `aws_cloudwatch_event_rule` | `google_cloud_scheduler_job` | Timer Trigger (in function) |
| **Logs** | `aws_cloudwatch_log_group` | Auto-created | Auto-created |

---

## Deployment Commands

### AWS
```bash
cd terraform-aws
terraform init
terraform plan
terraform apply
```

### GCP
```bash
cd terraform-gcp
terraform init
terraform plan
terraform apply
```

### Azure
```bash
cd terraform-azure
terraform init
terraform plan
terraform apply
```

---

This comprehensive IaC reference enables teams to deploy the secure file transfer solution on any of the three major cloud providers using consistent, production-ready Terraform code.
