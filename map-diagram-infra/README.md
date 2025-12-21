# Infrastructure Composer - Multi-Cloud Architecture Diagrams

This directory contains comprehensive infrastructure diagrams and resource mappings for deploying a secure file transfer solution across **AWS**, **GCP**, and **Azure**.

## 📁 Directory Contents

### Universal/Cloud-Agnostic Documents

1. **[infrastructure-composer-universal.yaml](infrastructure-composer-universal.yaml)**
   - Complete cloud-agnostic component definitions
   - Abstract architecture that maps to all three cloud providers
   - Data flow definitions
   - Security architecture
   - Cost optimization strategies
   - Deployment considerations

2. **[diagram-architecture-universal.md](diagram-architecture-universal.md)**
   - Cloud-agnostic Mermaid architecture diagram
   - Component descriptions
   - Data flow visualization
   - Security layers
   - Cost estimates
   - Cloud provider equivalency table

### Cloud-Specific Resource Mappings

3. **[aws-resource-mapping.yaml](aws-resource-mapping.yaml)**
   - Detailed AWS service mappings
   - Terraform resource names
   - Pricing information
   - AWS CLI commands
   - Security checklist
   - Monthly cost: **$3.11** (savings: **91%** vs NAT Gateway)

4. **[gcp-resource-mapping.yaml](gcp-resource-mapping.yaml)**
   - Detailed GCP service mappings
   - Terraform resource names
   - Pricing information
   - gcloud CLI commands
   - Security checklist
   - Monthly cost: **$11.82** (or **$2.37** with Cloud Run)

5. **[azure-resource-mapping.yaml](azure-resource-mapping.yaml)**
   - Detailed Azure service mappings
   - Terraform resource names
   - Pricing information
   - Azure CLI commands
   - Security checklist
   - Monthly cost: **$2.28** (Consumption plan)

### Cloud-Specific Architecture Diagrams

6. **[diagram-architecture-aws.md](diagram-architecture-aws.md)**
   - AWS-specific Mermaid diagram with actual service names
   - Lambda, S3, VPC Gateway Endpoint, CloudWatch, etc.
   - Detailed deployment instructions
   - Monitoring queries
   - Best practices

7. **[diagram-architecture-gcp.md](diagram-architecture-gcp.md)**
   - GCP-specific Mermaid diagram with actual service names
   - Cloud Functions, Cloud Storage, Private Google Access, etc.
   - Detailed deployment instructions
   - Cost optimization tips
   - Migration guide from AWS

8. **[diagram-architecture-azure.md](diagram-architecture-azure.md)**
   - Azure-specific Mermaid diagram with actual service names
   - Azure Functions, Blob Storage, Service Endpoints, etc.
   - Detailed deployment instructions
   - Multiple pricing options
   - Migration guide from AWS/GCP

## 🎯 Purpose

This infrastructure composer provides:

- ✅ **Universal Architecture**: Cloud-agnostic design that works across AWS, GCP, and Azure
- ✅ **Cost Transparency**: Detailed pricing for each cloud provider
- ✅ **Security Best Practices**: Comprehensive security guidelines
- ✅ **Migration Paths**: Clear mappings between cloud services
- ✅ **Deployment Ready**: Complete Terraform resources and CLI commands
- ✅ **Visual Diagrams**: Mermaid diagrams for easy understanding

## 🏗️ Architecture Overview

### Core Components (Cloud-Agnostic)

1. **Virtual Network** - Isolated network for secure compute
2. **Private Subnets** - Network segments without internet access
3. **Serverless Function** - Execute file transfer logic
4. **Object Storage** - Secure file storage with lifecycle policies
5. **Private Service Endpoint** ⭐ - FREE private connectivity to storage (KEY COST SAVER)
6. **Secrets Manager** - Secure credential storage
7. **Identity & Access** - Service identity with least privilege
8. **Monitoring & Logging** - Centralized logging and metrics
9. **Automation** - Scheduled execution

### Key Innovation: Private Service Endpoint ⭐

The **private service endpoint** is the KEY component that makes this architecture cost-effective:

- **AWS**: S3 VPC Gateway Endpoint - **FREE** (saves $32.40/month vs NAT Gateway)
- **GCP**: Private Google Access - **FREE** (saves $32+/month vs NAT Gateway equivalent)
- **Azure**: Storage Service Endpoint - **FREE** (saves on data transfer)

This allows serverless functions to access object storage **without internet connectivity**, eliminating the need for expensive NAT Gateways or Internet Gateways.

## 💰 Cost Comparison

| Cloud Provider | Monthly Cost | Annual Cost | Key Services |
|---------------|-------------|-------------|--------------|
| **AWS** | **$3.11** | $37.32 | Lambda + S3 + Gateway Endpoint |
| **GCP (Functions)** | $11.82 | $141.84 | Cloud Functions + Storage + VPC Connector |
| **GCP (Cloud Run)** | $2.37 | $28.44 | Cloud Run + Storage (optimized) |
| **Azure (Consumption)** | **$2.28** | $27.36 | Functions + Blob Storage + Service Endpoints |
| **Azure (Premium)** | $145.00 | $1,740 | Premium plan (always-on) |

**Winner**: Azure Consumption Plan ($2.28/month) for cost optimization
**Runner-up**: GCP Cloud Run ($2.37/month)
**AWS**: $3.11/month (still excellent value)

**Note**: All three cloud providers offer FREE private connectivity to object storage, which is the primary cost saver in this architecture.

## 🔒 Security Features (All Clouds)

### Network Security
- ✓ Serverless functions in private network
- ✓ No direct internet access for storage
- ✓ Firewall rules with restrictive egress
- ✓ Private service endpoints (no internet traversal)

### Data Security
- ✓ Encryption at rest (AES-256)
- ✓ Encryption in transit (TLS/HTTPS)
- ✓ Object versioning
- ✓ Public access blocked

### Identity Security
- ✓ Service identities (no hardcoded credentials)
- ✓ Least privilege access policies
- ✓ Secrets manager integration
- ✓ No access keys in code

### Monitoring Security
- ✓ Centralized logging
- ✓ Metrics and alarms
- ✓ Audit trails
- ✓ Retention policies

## 📊 Service Equivalency Matrix

| Component | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| **Virtual Network** | VPC | VPC Network | Virtual Network |
| **Network Segments** | Subnets | Subnets | Subnets |
| **Firewall** | Security Groups | Firewall Rules | NSG |
| **Private Endpoint** ⭐ | S3 Gateway (FREE) | Private Google Access (FREE) | Service Endpoint (FREE) |
| **Serverless** | Lambda | Cloud Functions/Run | Azure Functions |
| **Object Storage** | S3 | Cloud Storage | Blob Storage |
| **Service Identity** | IAM Role | Service Account | Managed Identity |
| **Secrets** | Secrets Manager | Secret Manager | Key Vault |
| **Logging** | CloudWatch Logs | Cloud Logging | Log Analytics |
| **Metrics** | CloudWatch | Cloud Monitoring | Azure Monitor |
| **Scheduler** | EventBridge | Cloud Scheduler | Logic Apps/Timer |

## 🚀 Quick Start

### 1. Choose Your Cloud Provider

**For AWS**:
```bash
cd terraform/aws
terraform init
terraform apply
```

**For GCP**:
```bash
cd terraform/gcp
terraform init
terraform apply
```

**For Azure**:
```bash
cd terraform/azure
terraform init
terraform apply
```

### 2. Review Architecture Diagrams

- **Universal**: [diagram-architecture-universal.md](diagram-architecture-universal.md)
- **AWS**: [diagram-architecture-aws.md](diagram-architecture-aws.md)
- **GCP**: [diagram-architecture-gcp.md](diagram-architecture-gcp.md)
- **Azure**: [diagram-architecture-azure.md](diagram-architecture-azure.md)

### 3. Review Resource Mappings

- **AWS**: [aws-resource-mapping.yaml](aws-resource-mapping.yaml)
- **GCP**: [gcp-resource-mapping.yaml](gcp-resource-mapping.yaml)
- **Azure**: [azure-resource-mapping.yaml](azure-resource-mapping.yaml)

## 📖 How to Use These Documents

### For Architects
- Review [infrastructure-composer-universal.yaml](infrastructure-composer-universal.yaml) for the abstract architecture
- Use [diagram-architecture-universal.md](diagram-architecture-universal.md) for presentations
- Reference cloud-specific diagrams for implementation details

### For Developers
- Use cloud-specific resource mappings for Terraform implementation
- Follow CLI commands for manual deployment and testing
- Reference monitoring queries for observability setup

### For Cost Analysts
- Compare monthly costs across cloud providers
- Review cost optimization strategies in each mapping file
- Analyze lifecycle policies and storage tiers

### For Security Teams
- Review security checklists in each cloud-specific file
- Validate network security configurations
- Ensure compliance with security best practices

### For Migration Teams
- Use service equivalency matrix for cloud-to-cloud migrations
- Follow migration guides in cloud-specific diagrams
- Reference resource mappings for detailed service comparisons

## 🎓 Learning Path

1. **Start with Universal Architecture**: Understand the cloud-agnostic design
2. **Compare Service Mappings**: Learn how each cloud implements the same concepts
3. **Review Cost Breakdowns**: Understand pricing differences
4. **Examine Security Features**: See how each cloud handles security
5. **Practice Deployment**: Try deploying on your preferred cloud
6. **Optimize Costs**: Apply cost optimization strategies from the mappings

## 📝 Document Structure

### YAML Files (Resource Mappings)
```yaml
metadata:
  # Project information
  
components:
  # Component definitions with cloud mappings
  
cloud_service_mapping:
  # Service equivalency table
  
cost_estimate:
  # Detailed cost breakdown
  
best_practices:
  # Cloud-specific recommendations
  
deployment:
  # Terraform and CLI commands
```

### Markdown Files (Diagrams)
```markdown
# Mermaid Diagram
  - Visual architecture

## Component Details
  - Service descriptions
  - Configuration details
  
## Cost Breakdown
  - Pricing tables
  
## Deployment
  - Step-by-step instructions
  
## Monitoring
  - Query examples
  
## Best Practices
  - Recommendations
```

## 🔧 Customization

All diagrams and mappings can be customized for your specific needs:

1. **Update CIDR ranges**: Change network addressing in YAML files
2. **Modify retention periods**: Adjust log retention in monitoring sections
3. **Change regions**: Update region/location in cloud-specific files
4. **Add custom metrics**: Extend monitoring queries
5. **Adjust costs**: Update pricing based on your negotiated rates

## 🌟 Key Features

### Universal Design
- Works across all major cloud providers
- Consistent architecture principles
- Portable knowledge and skills

### Cost Optimized
- FREE private connectivity to storage
- Serverless architecture (pay per use)
- Lifecycle policies for storage optimization
- Minimal logging retention

### Production Ready
- High availability across zones
- Automated scaling
- Comprehensive monitoring
- Security best practices

### Well Documented
- Visual diagrams for each cloud
- Detailed resource mappings
- CLI commands for deployment
- Monitoring queries included

## 📞 Support

For questions or issues:
- Review the README files in each YAML/MD file
- Check the cloud-specific documentation links
- Open an issue in the repository
- Consult cloud provider documentation

## 🏆 Certification Alignment

This architecture aligns with:
- ✅ **AWS Certified Data Engineer Associate (DEA-C01)**
- ✅ AWS Certified Solutions Architect Associate
- ✅ Google Cloud Professional Cloud Architect
- ✅ Microsoft Certified: Azure Solutions Architect Expert

Covers domains:
- Data ingestion and transformation
- Data storage and management
- Security and compliance
- Cost optimization
- Operational excellence
- Networking and connectivity

## 📚 Additional Resources

### AWS
- [AWS VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html)
- [AWS Lambda in VPC](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### GCP
- [Private Google Access](https://cloud.google.com/vpc/docs/private-google-access)
- [Cloud Functions VPC](https://cloud.google.com/functions/docs/networking/connecting-vpc)
- [GCP Architecture Center](https://cloud.google.com/architecture)

### Azure
- [VNet Service Endpoints](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview)
- [Azure Functions VNet Integration](https://docs.microsoft.com/en-us/azure/azure-functions/functions-networking-options)
- [Azure Architecture Center](https://docs.microsoft.com/en-us/azure/architecture/)

## 📅 Version History

- **v1.0.0** (2025-12-21): Initial release
  - Universal infrastructure composer
  - AWS, GCP, Azure resource mappings
  - Cloud-specific architecture diagrams
  - Cost comparisons and optimizations
  - Security best practices
  - Deployment guides

## 🤝 Contributing

To contribute improvements:
1. Update the universal YAML for cloud-agnostic changes
2. Update cloud-specific YAMLs for service-specific changes
3. Update Mermaid diagrams in markdown files
4. Update cost estimates with current pricing
5. Add new best practices or optimization tips

## 📄 License

This documentation is part of the DEA-C01 Secure File Transfer project and is licensed under the MIT License.

---

**⭐ These diagrams provide a complete blueprint for deploying secure, cost-effective file transfer solutions across any major cloud provider!**
