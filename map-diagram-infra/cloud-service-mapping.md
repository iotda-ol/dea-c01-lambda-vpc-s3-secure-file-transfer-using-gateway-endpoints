# Cloud Service Mapping Reference

Complete mapping of infrastructure components across AWS, Google Cloud Platform (GCP), and Microsoft Azure.

## Component Mapping Table

| **Component Category** | **Generic Term** | **AWS Service** | **GCP Service** | **Azure Service** |
|------------------------|------------------|-----------------|-----------------|-------------------|
| **Compute** |
| Serverless Functions | Serverless Function | AWS Lambda | Cloud Functions | Azure Functions |
| Function Runtime | Python 3.11 Runtime | Python 3.11 | Python 3.11 | Python 3.11 |
| Function Execution Role | Service Role | IAM Role | Service Account | Managed Identity |
| **Networking** |
| Virtual Network | Virtual Private Network | Amazon VPC | VPC Network | Virtual Network (VNet) |
| Private Subnet | Private Subnet | VPC Subnet | VPC Subnet | Subnet |
| Network Firewall | Security Group | Security Group | Firewall Rules | Network Security Group (NSG) |
| Stateless Firewall | Network ACL | NACL | VPC Firewall Rules | Application Security Groups |
| Private Service Endpoint | Gateway Endpoint | VPC Gateway Endpoint | Private Service Connect | Private Endpoint |
| Network Interface | Network Interface | ENI (Elastic Network Interface) | Network Interface | Network Interface (NIC) |
| Route Management | Route Table | Route Table | Routes | Route Table |
| **Storage** |
| Object Storage | Object Storage Bucket | Amazon S3 | Cloud Storage | Azure Blob Storage |
| Storage Encryption | Server-Side Encryption | SSE-S3 / SSE-KMS | CMEK / Google-managed | SSE / Customer-managed |
| Storage Versioning | Object Versioning | S3 Versioning | Object Versioning | Blob Versioning |
| Storage Lifecycle | Lifecycle Policy | S3 Lifecycle | Object Lifecycle Management | Blob Lifecycle Management |
| Storage Tiers | Storage Classes | Standard, IA, Glacier, Deep Archive | Standard, Nearline, Coldline, Archive | Hot, Cool, Archive |
| **Security & Identity** |
| Identity Management | IAM Service | AWS IAM | Cloud IAM | Azure AD / Entra ID |
| Service Principal | Service Role/Principal | IAM Role | Service Account | Managed Identity |
| Access Policies | Permission Policies | IAM Policy | IAM Policy | RBAC / IAM Role |
| Secret Storage | Secrets Manager | AWS Secrets Manager | Secret Manager | Azure Key Vault |
| Key Management | Key Management | AWS KMS | Cloud KMS | Azure Key Vault |
| Credential Encryption | KMS Encryption | KMS Keys | Cloud KMS Keys | Key Vault Keys |
| **Monitoring & Logging** |
| Centralized Logging | Log Service | CloudWatch Logs | Cloud Logging | Azure Monitor Logs |
| Metrics & Monitoring | Metrics Service | CloudWatch Metrics | Cloud Monitoring | Azure Monitor Metrics |
| Log Retention | Retention Policy | Log Retention | Log Retention | Retention Policy |
| Distributed Tracing | Tracing Service | AWS X-Ray | Cloud Trace | Application Insights |
| **Automation** |
| Event Scheduler | Cron Scheduler | EventBridge / CloudWatch Events | Cloud Scheduler | Azure Logic Apps / Timer Triggers |
| Event-Driven Execution | Event Trigger | EventBridge | Eventarc | Event Grid |
| **Cost Optimization** |
| Reserved Capacity | Reserved Instances | Lambda Reserved Concurrency | Committed Use Discounts | Reserved Instances |
| Savings Plans | Cost Savings | Savings Plans | Committed Use Discounts | Reserved Capacity |

## Detailed Service Comparison

### 1. Serverless Compute

#### AWS Lambda
- **Service Name**: AWS Lambda
- **Pricing Model**: Per-request + duration (GB-seconds)
- **Free Tier**: 1M requests/month, 400,000 GB-seconds
- **Max Timeout**: 15 minutes
- **Memory Range**: 128 MB - 10,240 MB
- **VPC Support**: Native VPC integration with ENI
- **Deployment**: ZIP file or Container image
- **IaC Tools**: Terraform, CloudFormation, SAM

#### Google Cloud Functions
- **Service Name**: Cloud Functions (2nd Gen)
- **Pricing Model**: Per-request + duration (GB-seconds)
- **Free Tier**: 2M requests/month, 400,000 GB-seconds
- **Max Timeout**: 60 minutes (2nd gen)
- **Memory Range**: 128 MB - 32 GB
- **VPC Support**: VPC connector or Private Service Connect
- **Deployment**: ZIP file, Container image
- **IaC Tools**: Terraform, Deployment Manager

#### Azure Functions
- **Service Name**: Azure Functions
- **Pricing Model**: Per-request + duration (GB-seconds) or App Service Plan
- **Free Tier**: 1M requests/month, 400,000 GB-seconds
- **Max Timeout**: 10 minutes (Consumption), Unlimited (Premium/Dedicated)
- **Memory Range**: Varies by plan
- **VNet Support**: VNet integration (Premium/Dedicated)
- **Deployment**: ZIP file, Container image
- **IaC Tools**: Terraform, ARM Templates, Bicep

### 2. Virtual Networking

#### AWS VPC
- **CIDR Range**: Customizable (/16 to /28)
- **Subnets**: Multiple AZs, Public/Private
- **DNS**: Route 53 integration
- **Peering**: VPC Peering, Transit Gateway
- **Endpoints**: Gateway Endpoint (S3, DynamoDB), Interface Endpoints
- **Cost**: VPC is free; endpoints vary (Gateway=Free, Interface=$0.01/hr)

#### GCP VPC
- **CIDR Range**: Global VPC, regional subnets
- **Subnets**: Auto-mode or Custom-mode
- **DNS**: Cloud DNS integration
- **Peering**: VPC Peering, Cloud VPN
- **Private Access**: Private Google Access, Private Service Connect
- **Cost**: VPC is free; Private Service Connect varies

#### Azure VNet
- **CIDR Range**: Customizable address space
- **Subnets**: Regional subnets
- **DNS**: Azure DNS integration
- **Peering**: VNet Peering, VPN Gateway
- **Endpoints**: Service Endpoints, Private Endpoints
- **Cost**: VNet is free; Private Endpoints ~$0.01/hr

### 3. Object Storage

#### Amazon S3
- **Storage Classes**: 
  - Standard: $0.023/GB
  - Standard-IA: $0.0125/GB (30-day minimum)
  - Glacier Instant Retrieval: $0.004/GB
  - Deep Archive: $0.00099/GB
- **Features**: Versioning, Lifecycle, Replication, Event Notifications
- **Encryption**: SSE-S3, SSE-KMS, SSE-C
- **Access Control**: Bucket policies, ACLs, IAM policies
- **SLA**: 99.99% availability

#### Google Cloud Storage
- **Storage Classes**:
  - Standard: $0.020/GB
  - Nearline: $0.010/GB (30-day minimum)
  - Coldline: $0.004/GB (90-day minimum)
  - Archive: $0.0012/GB (365-day minimum)
- **Features**: Versioning, Lifecycle, Replication, Cloud Pub/Sub notifications
- **Encryption**: Google-managed, Customer-managed (CMEK)
- **Access Control**: IAM policies, ACLs
- **SLA**: 99.95% availability (Standard)

#### Azure Blob Storage
- **Storage Tiers**:
  - Hot: $0.0184/GB
  - Cool: $0.01/GB (30-day minimum)
  - Archive: $0.00099/GB (180-day minimum)
- **Features**: Versioning, Lifecycle, Replication, Event Grid
- **Encryption**: SSE with Microsoft-managed or Customer-managed keys
- **Access Control**: RBAC, SAS tokens
- **SLA**: 99.9% availability (LRS)

### 4. Secrets Management

#### AWS Secrets Manager
- **Cost**: $0.40/secret/month + $0.05 per 10,000 API calls
- **Features**: Automatic rotation, Cross-account access, Lambda integration
- **Encryption**: KMS encryption
- **Rotation**: Built-in for RDS, Redshift, DocumentDB
- **Versioning**: Automatic version tracking

#### Google Secret Manager
- **Cost**: $0.06/secret/month + $0.03 per 10,000 API calls
- **Features**: Automatic rotation (manual setup), Replication
- **Encryption**: Automatic encryption at rest
- **Rotation**: Customer-managed via Cloud Functions
- **Versioning**: Automatic version tracking

#### Azure Key Vault
- **Cost**: $0.03/secret/month + $0.03 per 10,000 operations
- **Features**: Automatic rotation (managed identities), RBAC
- **Encryption**: Automatic encryption
- **Rotation**: Supports automatic rotation
- **Versioning**: Automatic version tracking

### 5. Identity & Access Management

#### AWS IAM
- **Principal Types**: Users, Roles, Groups, Service Accounts
- **Policy Types**: Identity-based, Resource-based, Permission boundaries
- **Authentication**: Access keys, MFA, Federation (SAML, OIDC)
- **Service Integration**: IAM Roles for EC2, Lambda, etc.
- **Cost**: Free

#### Google Cloud IAM
- **Principal Types**: Users, Service Accounts, Groups
- **Policy Types**: Resource-based policies, Conditions
- **Authentication**: Service account keys, Workload Identity
- **Service Integration**: Service Accounts for all services
- **Cost**: Free

#### Azure IAM (Entra ID)
- **Principal Types**: Users, Managed Identities, Service Principals
- **Policy Types**: RBAC, Custom roles
- **Authentication**: Service principal credentials, Managed identities
- **Service Integration**: Managed Identities for Azure resources
- **Cost**: Free for basic features

### 6. Monitoring & Logging

#### AWS CloudWatch
- **Logs**: $0.50/GB ingested, $0.03/GB storage
- **Metrics**: $0.30 per custom metric
- **Dashboards**: $3/dashboard/month
- **Alarms**: $0.10 per alarm
- **Retention**: Configurable (1 day to infinite)

#### Google Cloud Operations (Stackdriver)
- **Logs**: $0.50/GB ingested (after 50 GB free)
- **Metrics**: Free for system metrics, $2.5030 per million data points for custom
- **Dashboards**: Free
- **Alerts**: Free
- **Retention**: 30 days (logs), varies (metrics)

#### Azure Monitor
- **Logs**: $2.76/GB ingested
- **Metrics**: Included with resources
- **Dashboards**: Free
- **Alerts**: $0.10 per alert rule + $0.001 per notification
- **Retention**: 30 days default (logs)

## Architecture Pattern Mapping

### Pattern: Private Connectivity to Object Storage

| **AWS** | **GCP** | **Azure** |
|---------|---------|-----------|
| VPC Gateway Endpoint (FREE) | Private Google Access (FREE) | Service Endpoint (FREE) |
| S3 Gateway Endpoint | Enable on subnet for Cloud Storage | Microsoft.Storage endpoint |
| Configured in Route Table | Configure subnet with Private Google Access | Configure on subnet |
| No data transfer charges | No data transfer charges | No additional charges |

### Pattern: Serverless Function in Private Network

| **AWS** | **GCP** | **Azure** |
|---------|---------|-----------|
| Lambda in VPC with ENI | Cloud Functions with VPC Connector | Azure Functions with VNet Integration |
| ENI created in private subnets | VPC Serverless Access Connector | VNet integration (requires Premium plan) |
| Security Groups for egress control | Firewall rules on connector | NSG for subnet |
| Cold start penalty (ENI creation) | Cold start penalty (connector) | Better cold start with Premium plan |

### Pattern: Scheduled Execution

| **AWS** | **GCP** | **Azure** |
|---------|---------|-----------|
| EventBridge (CloudWatch Events) | Cloud Scheduler | Logic Apps / Timer Trigger |
| Cron expression support | Cron expression support | Cron expression support |
| Free tier: None (minimal cost) | Free tier: 3 jobs | Logic Apps: Pay per execution |
| Direct Lambda integration | Pub/Sub + Cloud Functions | Direct Function trigger |

## Cost Comparison Example

**Scenario**: 1,000 file transfers per month, 100 MB average file size, 30-second average execution time

### AWS
- **Lambda**: 1,000 requests × 0.512 GB × 30s = 15,360 GB-s = ~$0.26
- **S3**: 100 GB storage × $0.023 = $2.30
- **Gateway Endpoint**: FREE
- **Secrets Manager**: $0.40
- **CloudWatch Logs**: ~$0.50
- **Total**: ~$3.46/month

### GCP
- **Cloud Functions**: 1,000 requests × 0.512 GB × 30s = 15,360 GB-s = ~$0.24
- **Cloud Storage**: 100 GB × $0.020 = $2.00
- **Private Google Access**: FREE
- **Secret Manager**: $0.06 × 1 secret = $0.06
- **Cloud Logging**: ~$0.25 (within free tier)
- **Total**: ~$2.55/month

### Azure
- **Azure Functions**: 1,000 requests × 0.512 GB × 30s = ~$0.20 (Consumption)
- **Blob Storage**: 100 GB × $0.0184 = $1.84
- **Service Endpoint**: FREE
- **Key Vault**: $0.03 × 1 secret = $0.03
- **Monitor Logs**: ~$0.10
- **Total**: ~$2.20/month

**Note**: VNet Integration requires Premium plan (~$167/month), making Consumption plan unsuitable for VNet scenarios without additional architecture changes.

## Infrastructure-as-Code Examples

### Terraform Provider Requirements

```hcl
# AWS
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# GCP
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Azure
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}
```

## Migration Considerations

### From AWS to GCP
1. **VPC**: Similar concepts, GCP VPC is global vs AWS regional
2. **Lambda → Cloud Functions**: Similar programming model, note timeout differences
3. **S3 → Cloud Storage**: Similar API, consider storage class differences
4. **IAM Roles → Service Accounts**: Different authentication model
5. **Gateway Endpoint → Private Google Access**: Enable at subnet level

### From AWS to Azure
1. **VPC → VNet**: Similar concepts, address space planning
2. **Lambda → Functions**: Consider Premium plan for VNet integration
3. **S3 → Blob Storage**: Different API, use SDK
4. **IAM Roles → Managed Identity**: Different authentication model
5. **Gateway Endpoint → Service Endpoint**: Enable at subnet level

### From GCP to AWS
1. **VPC Network → VPC**: Regional vs global model difference
2. **Cloud Functions → Lambda**: Similar model, VPC integration differs
3. **Cloud Storage → S3**: API differences, consider multi-region strategy
4. **Service Account → IAM Role**: Role assumption model
5. **Private Google Access → Gateway Endpoint**: Configure route table

## Best Practices Across Clouds

### Security
- ✅ Always use private networking for sensitive data
- ✅ Enable encryption at rest and in transit
- ✅ Implement least privilege access policies
- ✅ Use managed secrets services, never hardcode
- ✅ Enable logging and monitoring
- ✅ Block all public access to storage unless required

### Cost Optimization
- ✅ Use serverless compute to avoid idle costs
- ✅ Implement storage lifecycle policies
- ✅ Use free/low-cost private endpoints
- ✅ Right-size compute memory and timeout
- ✅ Set appropriate log retention periods
- ✅ Monitor and set up budget alerts

### Operational Excellence
- ✅ Use Infrastructure as Code (Terraform)
- ✅ Implement CI/CD pipelines
- ✅ Set up comprehensive monitoring and alerting
- ✅ Document architecture and runbooks
- ✅ Implement automated testing
- ✅ Plan for disaster recovery

### Performance
- ✅ Deploy in multiple availability zones
- ✅ Use appropriate storage tiers for access patterns
- ✅ Implement retry logic with exponential backoff
- ✅ Monitor cold start times
- ✅ Consider reserved capacity for predictable workloads

## Conclusion

This mapping demonstrates that the secure file transfer architecture can be implemented across all three major cloud providers with similar functionality, security posture, and cost efficiency. The choice of cloud provider should be based on:

1. **Existing Infrastructure**: Leverage existing cloud investments
2. **Cost**: GCP and Azure may offer slight cost advantages
3. **Features**: AWS has the most mature serverless ecosystem
4. **Compliance**: Region availability and compliance requirements
5. **Team Expertise**: Existing skills and certifications
6. **Enterprise Agreements**: Negotiated pricing and support

All three platforms support the core requirements:
- ✅ Serverless compute in private networks
- ✅ Private connectivity to object storage (FREE/low-cost)
- ✅ Comprehensive security features
- ✅ Monitoring and logging capabilities
- ✅ Secrets management
- ✅ Cost optimization through lifecycle policies
