# Component Mapping: AWS ↔ GCP ↔ Azure

## Overview

This document provides detailed mappings between cloud service providers for the secure file transfer infrastructure. Each component is mapped across AWS, Google Cloud Platform (GCP), and Microsoft Azure with equivalent services, features, and configuration considerations.

---

## 1. Virtual Network Infrastructure

### Component: Isolated Network Environment

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Service Name** | Amazon VPC | Virtual Private Cloud (VPC) | Virtual Network (VNet) |
| **CIDR Block** | 10.0.0.0/16 | 10.0.0.0/16 | 10.0.0.0/16 |
| **Private Subnets** | VPC Subnets | VPC Subnets | Subnets |
| **Route Tables** | Route Tables | Routes | Route Tables |
| **DNS Resolution** | Route 53 Private Hosted Zones | Cloud DNS Private Zones | Azure Private DNS |
| **Terraform Resource** | `aws_vpc` | `google_compute_network` | `azurerm_virtual_network` |

**Configuration Notes:**
- **AWS**: Enable DNS hostnames and DNS support
- **GCP**: Use custom subnet mode for flexibility
- **Azure**: Address space can span multiple CIDR blocks

---

## 2. Serverless Compute

### Component: Event-Driven Function Execution

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Service Name** | AWS Lambda | Cloud Functions (2nd gen) | Azure Functions |
| **Runtime** | Python 3.11 | Python 3.11 | Python 3.11 |
| **Memory** | 512 MB | 512 MB | 512 MB |
| **Timeout** | 300 seconds (5 min) | 540 seconds (9 min) | 600 seconds (10 min) |
| **VPC Integration** | VPC Config | VPC Connector | VNet Integration |
| **Environment Variables** | Native support | Native support | Application Settings |
| **Terraform Resource** | `aws_lambda_function` | `google_cloudfunctions2_function` | `azurerm_function_app` |

**Handler Patterns:**
- **AWS**: `lambda_function.lambda_handler(event, context)`
- **GCP**: `main(request)` (HTTP) or `main(event, context)` (Event)
- **Azure**: `main(req: func.HttpRequest)` or similar

**Networking:**
- **AWS**: Attach security groups, deploy in private subnets
- **GCP**: Use Serverless VPC Access Connector
- **Azure**: VNet Integration with subnet delegation

---

## 3. Object Storage

### Component: Scalable File Storage

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Service Name** | Amazon S3 | Cloud Storage | Blob Storage |
| **Bucket/Container** | S3 Bucket | GCS Bucket | Storage Container |
| **Encryption** | SSE-AES256 / SSE-KMS | Google-managed / CMEK | Microsoft-managed / Customer-managed |
| **Versioning** | Native support | Native support | Native support |
| **Lifecycle Policies** | S3 Lifecycle Rules | Object Lifecycle Management | Lifecycle Management |
| **Access Control** | IAM + Bucket Policies | IAM + ACLs | RBAC + SAS Tokens |
| **Terraform Resource** | `aws_s3_bucket` | `google_storage_bucket` | `azurerm_storage_account` |

**Storage Classes:**
| Tier | AWS | GCP | Azure |
|------|-----|-----|-------|
| **Hot/Frequent** | S3 Standard | Standard | Hot Tier |
| **Infrequent** | S3 Standard-IA | Nearline | Cool Tier |
| **Archive** | S3 Glacier | Coldline | Archive Tier |
| **Deep Archive** | S3 Glacier Deep Archive | Archive | Archive Tier |

**Cost Optimization:**
- **AWS**: Transition to Standard-IA (30d), Glacier IR (90d), Deep Archive (180d)
- **GCP**: Transition to Nearline (30d), Coldline (90d), Archive (180d)
- **Azure**: Transition to Cool (30d), Archive (90d)

---

## 4. Private Service Connectivity

### Component: Secure Access to Cloud Services

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Service Name** | VPC Endpoint (Gateway) | Private Service Connect | Private Link |
| **Type** | Gateway Endpoint (S3) | Private Service Connect Endpoint | Private Endpoint |
| **Pricing** | Free for S3 Gateway | Varies by service | $0.01/hour + data |
| **Route Integration** | Automatic to route tables | Automatic via Cloud Router | Manual NSG rules |
| **Supported Services** | S3, DynamoDB (Gateway) | 100+ Google services | 100+ Azure services |
| **Terraform Resource** | `aws_vpc_endpoint` | `google_compute_service_attachment` | `azurerm_private_endpoint` |

**Traffic Flow:**
- **AWS**: Lambda → VPC → Gateway Endpoint → S3 (stays in AWS network)
- **GCP**: Cloud Function → VPC → Private Service Connect → Cloud Storage
- **Azure**: Azure Function → VNet → Private Endpoint → Blob Storage

**Key Benefits:**
- No internet gateway or NAT gateway required
- Data never leaves cloud provider's network
- Lower latency and improved security

---

## 5. Identity and Access Management

### Component: Authentication and Authorization

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Service Name** | AWS IAM | Cloud IAM | Azure Active Directory + RBAC |
| **Role/Principal** | IAM Role | Service Account | Managed Identity |
| **Policy Format** | JSON (IAM Policy) | JSON (IAM Policy) | JSON (ARM Policy) |
| **Least Privilege** | Fine-grained policies | Fine-grained policies | Fine-grained policies |
| **Assume Role** | Trust Policy | Service Account Impersonation | Managed Identity |
| **Terraform Resource** | `aws_iam_role` | `google_service_account` | `azurerm_user_assigned_identity` |

**Permissions Required:**

| Action | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Storage Write** | `s3:PutObject` | `storage.objects.create` | `Microsoft.Storage/storageAccounts/blobServices/containers/write` |
| **Storage Read** | `s3:GetObject` | `storage.objects.get` | `Microsoft.Storage/storageAccounts/blobServices/containers/read` |
| **Storage List** | `s3:ListBucket` | `storage.objects.list` | `Microsoft.Storage/storageAccounts/blobServices/containers/list` |
| **Logging** | `logs:PutLogEvents` | `logging.logEntries.create` | `Microsoft.Insights/logs/write` |
| **Secrets** | `secretsmanager:GetSecretValue` | `secretmanager.versions.access` | `Microsoft.KeyVault/vaults/secrets/read` |

---

## 6. Secrets Management

### Component: Credential and Secret Storage

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Service Name** | AWS Secrets Manager | Secret Manager | Azure Key Vault |
| **Secret Format** | JSON | Text/Binary | Text/Binary/Certificate |
| **Versioning** | Automatic | Automatic | Automatic |
| **Encryption** | KMS (automatic) | Cloud KMS | Key Vault Encryption |
| **Rotation** | Lambda-based rotation | Cloud Functions rotation | Logic Apps rotation |
| **Pricing** | $0.40/secret/month | $0.06/secret/month | $0.03/secret/month |
| **Terraform Resource** | `aws_secretsmanager_secret` | `google_secret_manager_secret` | `azurerm_key_vault_secret` |

**Best Practices:**
- Store SFTP credentials (username, password/key, host, port)
- Enable automatic rotation where possible
- Use least privilege access policies
- Audit secret access via logging

---

## 7. Logging and Monitoring

### Component: Centralized Logging

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Logging Service** | CloudWatch Logs | Cloud Logging | Azure Monitor Logs |
| **Log Groups** | Log Groups | Log Sinks | Log Analytics Workspace |
| **Retention** | 7 days (configurable) | 30 days default | 30 days default |
| **Query Language** | CloudWatch Insights | Logging Query Language | Kusto Query Language (KQL) |
| **Terraform Resource** | `aws_cloudwatch_log_group` | `google_logging_project_sink` | `azurerm_log_analytics_workspace` |

### Component: Metrics and Alerting

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Metrics Service** | CloudWatch Metrics | Cloud Monitoring | Azure Monitor Metrics |
| **Alarms** | CloudWatch Alarms | Alerting Policies | Metric Alerts |
| **Dashboards** | CloudWatch Dashboards | Cloud Monitoring Dashboards | Azure Dashboards |
| **Terraform Resource** | `aws_cloudwatch_metric_alarm` | `google_monitoring_alert_policy` | `azurerm_monitor_metric_alert` |

---

## 8. Event Scheduling

### Component: Periodic Function Execution

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Service Name** | Amazon EventBridge | Cloud Scheduler | Logic Apps / Azure Scheduler |
| **Schedule Format** | Cron expression | Cron expression | Recurrence pattern |
| **Target** | Lambda Function | Cloud Function / Cloud Run | Azure Function |
| **Timezone** | UTC (default) | Any timezone | Any timezone |
| **Terraform Resource** | `aws_cloudwatch_event_rule` | `google_cloud_scheduler_job` | `azurerm_logic_app_workflow` |

**Example Schedule:**
- **AWS**: `cron(0 2 * * ? *)` - Daily at 2 AM UTC
- **GCP**: `0 2 * * *` - Daily at 2 AM
- **Azure**: Recurrence with interval 1 day, start time 02:00

---

## 9. Network Security

### Component: Firewall Rules

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Service Name** | Security Groups | Firewall Rules | Network Security Groups (NSG) |
| **Rule Type** | Ingress/Egress | Ingress/Egress | Inbound/Outbound |
| **Stateful** | Yes | Yes (ingress rules) | Yes |
| **Default Deny** | Yes | Yes | Yes |
| **Terraform Resource** | `aws_security_group` | `google_compute_firewall` | `azurerm_network_security_group` |

**Required Rules:**

| Direction | Protocol | Port | Purpose | AWS | GCP | Azure |
|-----------|----------|------|---------|-----|-----|-------|
| **Egress** | TCP | 443 | HTTPS to Storage | 0.0.0.0/0 | 0.0.0.0/0 | Internet |
| **Egress** | TCP | 22 | SSH/SFTP | SFTP Server IP | SFTP Server IP | SFTP Server IP |

---

## 10. Infrastructure as Code

### Terraform Provider Configuration

**AWS:**
```hcl
provider "aws" {
  region = "us-east-1"
}
```

**GCP:**
```hcl
provider "google" {
  project = "my-project-id"
  region  = "us-east1"
}
```

**Azure:**
```hcl
provider "azurerm" {
  features {}
  subscription_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

---

## 11. Cost Comparison (Monthly Estimates)

Assumptions: 1,000 function executions, 30s avg duration, 100GB storage

| Component | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| **Compute** | $0.25 | $0.24 | $0.20 |
| **Storage (100GB)** | $2.30 | $2.00 | $1.80 |
| **Secrets** | $0.40 | $0.06 | $0.03 |
| **Logging** | $0.50 | $0.50 | $0.50 |
| **Private Endpoint** | $0.00 (S3 Gateway) | $0.00* | $7.20 |
| **Total** | **~$3.45** | **~$2.80** | **~$9.73** |

*GCP Private Service Connect may have costs depending on configuration

---

## 12. Migration Considerations

### AWS → GCP
- Replace VPC Gateway Endpoint with Private Service Connect
- Convert Lambda to Cloud Functions (2nd gen)
- Migrate S3 buckets to Cloud Storage (use gsutil or Transfer Service)
- Update IAM policies to Cloud IAM format
- Replace Secrets Manager with Secret Manager

### AWS → Azure
- Replace VPC with Virtual Network
- Convert Lambda to Azure Functions (consumption plan)
- Migrate S3 to Blob Storage (use AzCopy or Data Factory)
- Replace VPC Endpoint with Private Link (incurs costs)
- Update IAM to Azure AD + RBAC
- Replace Secrets Manager with Key Vault

### GCP → AWS
- Reverse of AWS → GCP mapping
- Consider S3 Gateway Endpoint cost savings

### Azure → AWS
- Reverse of AWS → Azure mapping
- Save costs on Private Endpoint by using free S3 Gateway Endpoint

---

## 13. Feature Parity Matrix

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Free Private Endpoint** | ✅ (S3 Gateway) | ⚠️ (Some services) | ❌ (Costs apply) |
| **Serverless VPC Integration** | ✅ | ✅ | ✅ |
| **Object Versioning** | ✅ | ✅ | ✅ |
| **Lifecycle Policies** | ✅ | ✅ | ✅ |
| **Encryption at Rest** | ✅ | ✅ | ✅ |
| **Managed Secrets** | ✅ | ✅ | ✅ |
| **Scheduled Execution** | ✅ | ✅ | ✅ |
| **Centralized Logging** | ✅ | ✅ | ✅ |

---

## Conclusion

This mapping enables teams to:
1. Deploy the same architecture across multiple cloud providers
2. Understand service equivalents and configuration differences
3. Estimate costs across different platforms
4. Plan migrations between cloud providers
5. Implement multi-cloud strategies

All three cloud providers support the core architecture patterns required for secure file transfer from SFTP to cloud object storage.
