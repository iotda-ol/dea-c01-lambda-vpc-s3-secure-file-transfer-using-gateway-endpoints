# GCP Implementation Guide

## Overview

This guide provides step-by-step instructions for deploying the secure file transfer architecture on Google Cloud Platform (GCP).

---

## Prerequisites

- Google Cloud Project with billing enabled
- `gcloud` CLI installed and configured
- Terraform >= 1.0
- Python >= 3.11
- Git

---

## Architecture Components (GCP-Specific)

| Component | GCP Service | Notes |
|-----------|-------------|-------|
| Virtual Network | Google VPC | Custom subnet mode |
| Serverless Compute | Cloud Functions (2nd gen) | Python 3.11 runtime |
| Object Storage | Cloud Storage | With versioning & lifecycle |
| Private Endpoint | Private Service Connect | Varies by configuration |
| Secrets Vault | Secret Manager | $0.06/secret/month |
| IAM | Cloud IAM | Service accounts |
| Logging | Cloud Logging | 30-day default retention |
| Monitoring | Cloud Monitoring | Standard metrics |
| Scheduler | Cloud Scheduler | Cron-based jobs |
| Network Security | VPC Firewall Rules | Stateful rules |

---

## Deployment Steps

### Step 1: Set Up GCP Project

```bash
# Create new project (optional)
gcloud projects create secure-file-transfer-project --name="Secure File Transfer"

# Set active project
gcloud config set project secure-file-transfer-project

# Enable required APIs
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable monitoring.googleapis.com
gcloud services enable vpcaccess.googleapis.com
gcloud services enable compute.googleapis.com
```

### Step 2: Configure gcloud CLI

```bash
# Initialize gcloud
gcloud init

# Set default region and zone
gcloud config set compute/region us-east1
gcloud config set compute/zone us-east1-b

# Verify configuration
gcloud config list
gcloud auth list
```

### Step 3: Create Terraform Configuration

**main.tf**:
```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Data sources
data "google_project" "project" {
  project_id = var.project_id
}
```

**variables.tf**:
```hcl
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-east1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "secure-transfer"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "VPC CIDR range"
  type        = string
  default     = "10.0.0.0/16"
}

variable "sftp_host" {
  description = "SFTP server hostname"
  type        = string
}

variable "sftp_port" {
  description = "SFTP server port"
  type        = number
  default     = 22
}

variable "sftp_username" {
  description = "SFTP username"
  type        = string
}

variable "schedule" {
  description = "Cron schedule for function"
  type        = string
  default     = "0 2 * * *"  # Daily at 2 AM
}
```

### Step 4: Create VPC Network

**network.tf**:
```hcl
# VPC Network
resource "google_compute_network" "vpc" {
  name                    = "${var.project_name}-${var.environment}-vpc"
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
}

# Private Subnet 1
resource "google_compute_subnetwork" "private_subnet_1" {
  name          = "${var.project_name}-${var.environment}-private-subnet-1"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
  
  private_ip_google_access = true  # Important for accessing Google APIs
}

# Private Subnet 2
resource "google_compute_subnetwork" "private_subnet_2" {
  name          = "${var.project_name}-${var.environment}-private-subnet-2"
  ip_cidr_range = "10.0.2.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
  
  private_ip_google_access = true
}

# Serverless VPC Access Connector (for Cloud Functions)
resource "google_vpc_access_connector" "connector" {
  name          = "${var.project_name}-${var.environment}-connector"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.0.3.0/28"  # Small range for connector
  
  min_instances = 2
  max_instances = 3
}

# Firewall Rules
resource "google_compute_firewall" "allow_https_egress" {
  name    = "${var.project_name}-${var.environment}-allow-https-egress"
  network = google_compute_network.vpc.name
  
  direction = "EGRESS"
  
  allow {
    protocol = "tcp"
    ports    = ["443"]
  }
  
  destination_ranges = ["0.0.0.0/0"]
  description        = "Allow HTTPS to Cloud Storage"
}

resource "google_compute_firewall" "allow_sftp_egress" {
  name    = "${var.project_name}-${var.environment}-allow-sftp-egress"
  network = google_compute_network.vpc.name
  
  direction = "EGRESS"
  
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  
  destination_ranges = ["0.0.0.0/0"]  # Replace with SFTP server IP for better security
  description        = "Allow SSH/SFTP to legacy server"
}
```

### Step 5: Create Cloud Storage Bucket

**storage.tf**:
```hcl
# Cloud Storage Bucket
resource "google_storage_bucket" "file_transfer" {
  name          = "${var.project_name}-${var.environment}-files-${random_id.bucket_suffix.hex}"
  location      = var.region
  storage_class = "STANDARD"
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
  
  encryption {
    default_kms_key_name = null  # Use Google-managed encryption
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
  
  lifecycle_rule {
    condition {
      age                   = 90
      with_state            = "ARCHIVED"
      num_newer_versions    = 0
    }
    action {
      type = "Delete"
    }
  }
  
  labels = {
    project     = var.project_name
    environment = var.environment
    managed_by  = "terraform"
  }
}

# Random suffix for globally unique bucket name
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Block public access
resource "google_storage_bucket_iam_binding" "prevent_public_access" {
  bucket = google_storage_bucket.file_transfer.name
  role   = "roles/storage.objectViewer"
  
  members = []  # Empty list prevents public access
}
```

### Step 6: Create Secret Manager Secret

**secrets.tf**:
```hcl
# Secret for SFTP credentials
resource "google_secret_manager_secret" "sftp_credentials" {
  secret_id = "${var.project_name}-${var.environment}-sftp-credentials"
  
  replication {
    automatic = true
  }
  
  labels = {
    project     = var.project_name
    environment = var.environment
  }
}

# Secret version (will be updated manually)
resource "google_secret_manager_secret_version" "sftp_credentials" {
  secret = google_secret_manager_secret.sftp_credentials.id
  
  secret_data = jsonencode({
    username    = var.sftp_username
    password    = ""  # Update manually
    private_key = ""  # Update manually
    host        = var.sftp_host
    port        = var.sftp_port
  })
  
  lifecycle {
    ignore_changes = [secret_data]
  }
}
```

### Step 7: Create Service Account and IAM

**iam.tf**:
```hcl
# Service Account for Cloud Function
resource "google_service_account" "function_sa" {
  account_id   = "${var.project_name}-${var.environment}-function"
  display_name = "Service Account for File Transfer Function"
  description  = "Used by Cloud Function to access Storage and Secrets"
}

# Grant Storage Object Admin to bucket
resource "google_storage_bucket_iam_member" "function_storage_admin" {
  bucket = google_storage_bucket.file_transfer.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.function_sa.email}"
}

# Grant Secret Accessor
resource "google_secret_manager_secret_iam_member" "function_secret_accessor" {
  secret_id = google_secret_manager_secret.sftp_credentials.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.function_sa.email}"
}

# Grant Logging permissions
resource "google_project_iam_member" "function_log_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}
```

### Step 8: Create Cloud Function

**function.tf**:
```hcl
# Package function code
data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda"
  output_path = "${path.module}/function-source.zip"
}

# Upload to Cloud Storage
resource "google_storage_bucket" "function_source" {
  name     = "${var.project_name}-${var.environment}-function-source-${random_id.bucket_suffix.hex}"
  location = var.region
}

resource "google_storage_bucket_object" "function_source" {
  name   = "function-source-${data.archive_file.function_source.output_md5}.zip"
  bucket = google_storage_bucket.function_source.name
  source = data.archive_file.function_source.output_path
}

# Cloud Function (2nd gen)
resource "google_cloudfunctions2_function" "file_transfer" {
  name        = "${var.project_name}-${var.environment}-file-transfer"
  location    = var.region
  description = "Secure file transfer from SFTP to Cloud Storage"
  
  build_config {
    runtime     = "python311"
    entry_point = "handler"
    
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.function_source.name
      }
    }
  }
  
  service_config {
    max_instance_count    = 10
    min_instance_count    = 0
    available_memory      = "512Mi"
    timeout_seconds       = 300
    service_account_email = google_service_account.function_sa.email
    
    vpc_connector                 = google_vpc_access_connector.connector.name
    vpc_connector_egress_settings = "ALL_TRAFFIC"
    
    environment_variables = {
      STORAGE_BUCKET = google_storage_bucket.file_transfer.name
      SECRET_ID      = google_secret_manager_secret.sftp_credentials.secret_id
      PROJECT_ID     = var.project_id
      LOG_LEVEL      = "INFO"
    }
  }
  
  labels = {
    project     = var.project_name
    environment = var.environment
  }
}
```

### Step 9: Create Cloud Scheduler Job

**scheduler.tf**:
```hcl
# Cloud Scheduler Job
resource "google_cloud_scheduler_job" "file_transfer" {
  name        = "${var.project_name}-${var.environment}-file-transfer-schedule"
  description = "Trigger file transfer function on schedule"
  schedule    = var.schedule
  time_zone   = "UTC"
  region      = var.region
  
  http_target {
    uri         = google_cloudfunctions2_function.file_transfer.service_config[0].uri
    http_method = "POST"
    
    oidc_token {
      service_account_email = google_service_account.function_sa.email
    }
    
    body = base64encode(jsonencode({
      mode = "scheduled"
    }))
  }
  
  retry_config {
    retry_count = 3
  }
}

# Grant invoker permission to service account
resource "google_cloud_run_service_iam_member" "scheduler_invoker" {
  location = google_cloudfunctions2_function.file_transfer.location
  service  = google_cloudfunctions2_function.file_transfer.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.function_sa.email}"
}
```

### Step 10: Deploy Infrastructure

```bash
# Initialize Terraform
terraform init

# Plan deployment
terraform plan -out=tfplan

# Apply deployment
terraform apply tfplan
```

### Step 11: Update SFTP Credentials

```bash
# Get secret name
SECRET_NAME=$(terraform output -raw secret_name)

# Update secret with actual credentials
# Password authentication
echo -n '{
  "username": "your-username",
  "password": "your-password",
  "host": "sftp.example.com",
  "port": 22
}' | gcloud secrets versions add $SECRET_NAME --data-file=-

# OR SSH key authentication
echo -n '{
  "username": "your-username",
  "private_key": "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----",
  "host": "sftp.example.com",
  "port": 22
}' | gcloud secrets versions add $SECRET_NAME --data-file=-
```

### Step 12: Test Function

```bash
# Get function URL
FUNCTION_URL=$(gcloud functions describe ${var.project_name}-${var.environment}-file-transfer \
  --region=${var.region} \
  --gen2 \
  --format='value(serviceConfig.uri)')

# Invoke function
curl -X POST $FUNCTION_URL \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H "Content-Type: application/json" \
  -d '{"test": true}'

# View logs
gcloud functions logs read ${var.project_name}-${var.environment}-file-transfer \
  --region=${var.region} \
  --gen2 \
  --limit=50
```

---

## Monitoring & Operations

### View Logs

```bash
# View function logs
gcloud logging read "resource.type=cloud_function AND resource.labels.function_name=${FUNCTION_NAME}" \
  --limit=50 \
  --format=json

# Tail logs in real-time
gcloud logging tail "resource.type=cloud_function"
```

### View Metrics

```bash
# Function invocations
gcloud monitoring time-series list \
  --filter='metric.type="cloudfunctions.googleapis.com/function/execution_count"' \
  --format=json
```

---

## Estimated Monthly Costs (GCP)

| Resource | Cost |
|----------|------|
| Cloud Functions (1,000 invocations) | $0.24 |
| Cloud Storage (100 GB) | $2.00 |
| VPC Connector | $0.00-1.00 |
| Secret Manager | $0.06 |
| Cloud Logging (1 GB) | $0.50 |
| **Total** | **~$2.80/month** |

**Lowest cost among all three cloud providers!**

---

## Cleanup

```bash
terraform destroy
```
