# Infrastructure Composer - Quick Reference

## 📍 Location
All infrastructure diagrams and resource mappings are located in the **`map-diagram-infra/`** directory.

## 📚 Available Documents

### 1. Universal Architecture
- **[infrastructure-composer-universal.yaml](map-diagram-infra/infrastructure-composer-universal.yaml)** - Cloud-agnostic YAML mapping
- **[diagram-architecture-universal.md](map-diagram-infra/diagram-architecture-universal.md)** - Universal Mermaid diagram

### 2. AWS Implementation
- **[aws-resource-mapping.yaml](map-diagram-infra/aws-resource-mapping.yaml)** - AWS service mappings
- **[diagram-architecture-aws.md](map-diagram-infra/diagram-architecture-aws.md)** - AWS architecture diagram

### 3. GCP Implementation
- **[gcp-resource-mapping.yaml](map-diagram-infra/gcp-resource-mapping.yaml)** - GCP service mappings
- **[diagram-architecture-gcp.md](map-diagram-infra/diagram-architecture-gcp.md)** - GCP architecture diagram

### 4. Azure Implementation
- **[azure-resource-mapping.yaml](map-diagram-infra/azure-resource-mapping.yaml)** - Azure service mappings
- **[diagram-architecture-azure.md](map-diagram-infra/diagram-architecture-azure.md)** - Azure architecture diagram

### 5. Comprehensive Guides
- **[README.md](map-diagram-infra/README.md)** - Complete guide to all diagrams
- **[cloud-comparison-matrix.md](map-diagram-infra/cloud-comparison-matrix.md)** - Side-by-side cloud comparison

## 🎯 Quick Access by Use Case

### I want to understand the architecture
→ Start with [diagram-architecture-universal.md](map-diagram-infra/diagram-architecture-universal.md)

### I'm deploying to AWS
→ See [diagram-architecture-aws.md](map-diagram-infra/diagram-architecture-aws.md)
→ Reference [aws-resource-mapping.yaml](map-diagram-infra/aws-resource-mapping.yaml)

### I'm deploying to GCP
→ See [diagram-architecture-gcp.md](map-diagram-infra/diagram-architecture-gcp.md)
→ Reference [gcp-resource-mapping.yaml](map-diagram-infra/gcp-resource-mapping.yaml)

### I'm deploying to Azure
→ See [diagram-architecture-azure.md](map-diagram-infra/diagram-architecture-azure.md)
→ Reference [azure-resource-mapping.yaml](map-diagram-infra/azure-resource-mapping.yaml)

### I need to compare costs across clouds
→ See [cloud-comparison-matrix.md](map-diagram-infra/cloud-comparison-matrix.md)

### I'm migrating between clouds
→ See [cloud-comparison-matrix.md](map-diagram-infra/cloud-comparison-matrix.md)
→ Check the service equivalency matrix

## 💰 Cost Summary

| Cloud | Monthly Cost | Best For |
|-------|-------------|----------|
| **AWS** | $3.11 | AWS ecosystem integration |
| **GCP (Cloud Run)** | $2.37 | Long-running tasks (60 min timeout) |
| **GCP (Cloud Functions)** | $11.82 | N/A - use Cloud Run instead |
| **Azure (Consumption)** | $2.28 ⭐ | Lowest cost |
| **Azure (Premium)** | $145.00 | Always-on, <1s response time |

**All three clouds offer FREE private connectivity to object storage!**

## 🔑 Key Components

All three cloud implementations include:
- ✅ Virtual Network (VPC/VNet)
- ✅ Private Subnets
- ✅ Serverless Function (Lambda/Cloud Functions/Azure Functions)
- ✅ Object Storage (S3/Cloud Storage/Blob Storage)
- ✅ **Private Service Endpoint (FREE)** ⭐ Key Cost Saver
- ✅ Secrets Manager (Secrets Manager/Secret Manager/Key Vault)
- ✅ Identity & Access Management (IAM/Service Account/Managed Identity)
- ✅ Monitoring & Logging (CloudWatch/Cloud Logging/Azure Monitor)
- ✅ Automation (EventBridge/Cloud Scheduler/Logic Apps or Timer)

## 🛡️ Security Features

All implementations include:
- Network isolation with private subnets
- Encryption at rest and in transit
- No hardcoded credentials
- Least privilege access policies
- Centralized logging and monitoring
- Network firewall rules

## 📖 How to Use

1. **Choose your cloud provider** (or review all three)
2. **Read the universal architecture** to understand the design
3. **Review the cloud-specific diagram** for your chosen provider
4. **Reference the resource mapping** for Terraform/CLI deployment
5. **Follow the deployment instructions** in the diagram document
6. **Set up monitoring** using the provided queries

## 🚀 Deployment Commands

### AWS
```bash
cd terraform/aws
terraform init && terraform apply
```

### GCP
```bash
cd terraform/gcp
terraform init && terraform apply
```

### Azure
```bash
cd terraform/azure
terraform init && terraform apply
```

## 📞 Support

For detailed information, see:
- [map-diagram-infra/README.md](map-diagram-infra/README.md) - Complete guide
- Individual diagram files for specific cloud implementations
- Resource mapping YAML files for Terraform details

---

**These diagrams provide production-ready blueprints for secure, cost-effective file transfer across any major cloud provider!**
