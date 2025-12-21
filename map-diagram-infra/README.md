# Infrastructure Composer - Multi-Cloud Architecture Diagrams

## Overview

This directory contains comprehensive infrastructure composition diagrams and mappings for implementing the secure file transfer solution across **AWS**, **Google Cloud Platform (GCP)**, and **Microsoft Azure**.

The infrastructure composer provides a universal, cloud-agnostic framework that enables:
- ✅ Understanding of architectural equivalents across cloud providers
- ✅ Cost comparison and optimization strategies
- ✅ Migration planning between cloud platforms
- ✅ Multi-cloud deployment strategies
- ✅ Standardized security and compliance practices

---

## Directory Contents

### 📄 [INFRASTRUCTURE-COMPOSER.md](./INFRASTRUCTURE-COMPOSER.md)
**Primary Documentation - Comprehensive Infrastructure Architecture**

This is the main document containing:
- Universal architecture diagrams
- Detailed component descriptions for AWS, GCP, and Azure
- Infrastructure as Code (Terraform) examples for all three providers
- Network architecture patterns
- Security architecture (defense in depth)
- Data flow diagrams
- Cost comparison analysis
- Migration considerations and checklists

**Use this document for:**
- Understanding the overall architecture
- Planning deployments on any cloud provider
- Cost-benefit analysis
- Security design and implementation
- Migration planning

---

### 📊 [COMPONENT-MAPPING-TABLE.md](./COMPONENT-MAPPING-TABLE.md)
**Detailed Resource Equivalency Matrix**

A comprehensive reference table mapping every infrastructure component across clouds:
- Core infrastructure components (Compute, Storage, Networking)
- Security services (IAM, Secrets, Encryption, Monitoring)
- Database and analytics services
- DevOps and CI/CD tools
- AI/ML services
- Detailed serverless file transfer component matrix
- Networking deep dive (Private connectivity models)
- Cost optimization with storage lifecycle policies
- Security best practices checklist

**Use this document for:**
- Quick reference when choosing cloud services
- Finding equivalent services across providers
- Understanding cost implications
- Implementing security best practices
- Planning infrastructure migrations

---

## Architecture Summary

### High-Level Universal Pattern

```
Legacy SFTP Server
        ↓
Cloud Platform (AWS/GCP/Azure)
        ↓
Virtual Private Network (VPC/VNet)
        ↓
Private Subnet
        ↓
Serverless Function (Lambda/Cloud Functions/Azure Functions)
        ↓
Private Service Endpoint (Gateway Endpoint/Private Google Access/Service Endpoint)
        ↓
Object Storage (S3/Cloud Storage/Blob Storage)
```

### Key Benefits Across All Providers
- **No NAT Gateway Required** - Cost savings of $30-50/month
- **Private Connectivity** - Traffic never leaves cloud provider network
- **Serverless Architecture** - Pay only for actual usage
- **Encryption End-to-End** - At rest and in transit
- **Least Privilege Security** - IAM/RBAC with minimal permissions
- **Automated Lifecycle** - Cost optimization through storage tiering

---

## Cloud Provider Comparison

### When to Choose Each Provider

#### AWS ✅
**Best For:**
- Mature ecosystem and extensive documentation
- Free VPC Gateway Endpoint (no cost for private S3 access)
- Comprehensive IAM and security features
- Existing AWS infrastructure
- Wide range of integrated services

**Monthly Cost:** ~$3.46 (1,000 transfers, 100 MB avg file size)

---

#### GCP 🌐
**Best For:**
- BigQuery integration for analytics
- Slightly cheaper object storage
- Uniform bucket-level access (simpler IAM)
- Existing GCP infrastructure
- Advanced data processing pipelines

**Monthly Cost:** ~$3.11 (without VPC Connector) or ~$54.21 (with VPC Connector)

*Note: VPC Connector may be required for Cloud Functions to access private network*

---

#### Azure ☁️
**Best For:**
- Microsoft/Azure ecosystem integration
- Active Directory and Office 365 integration
- Managed identities (simpler than service accounts)
- Enterprise compliance requirements
- Hybrid cloud scenarios

**Monthly Cost:** ~$4.80 (1,000 transfers, 100 MB avg file size)

---

## Core Components Mapping

| Component | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| **Serverless Compute** | Lambda | Cloud Functions | Azure Functions |
| **Object Storage** | S3 | Cloud Storage | Blob Storage |
| **Virtual Network** | VPC | VPC | Virtual Network |
| **Private Endpoint** | VPC Gateway Endpoint | Private Google Access | Service Endpoint |
| **IAM** | IAM Roles | Service Accounts | Managed Identity |
| **Secrets** | Secrets Manager | Secret Manager | Key Vault |
| **Logging** | CloudWatch | Cloud Logging | Monitor Logs |
| **Scheduler** | EventBridge | Cloud Scheduler | Timer Trigger |

---

## Infrastructure as Code (Terraform)

All three cloud providers are supported through Terraform with specific providers:

### AWS Provider
```hcl
provider "aws" {
  region = "us-east-1"
}
```

### GCP Provider
```hcl
provider "google" {
  project = "my-project-id"
  region  = "us-central1"
}
```

### Azure Provider
```hcl
provider "azurerm" {
  features {}
}
```

Full Terraform examples for each provider are included in the documentation.

---

## Security Architecture

All implementations follow defense-in-depth principles:

1. **Network Security**
   - Private subnets/networks only
   - Restrictive security groups/firewall rules
   - No public internet exposure for storage access

2. **Identity & Access Control**
   - Least privilege IAM/RBAC policies
   - Temporary credentials only
   - Service-specific roles

3. **Data Protection**
   - Encryption in transit (TLS 1.2+)
   - Encryption at rest (AES-256)
   - Versioning enabled

4. **Secrets Management**
   - Centralized secrets storage
   - Encrypted credentials
   - Audit logging

5. **Monitoring & Audit**
   - Comprehensive logging
   - Real-time alerting
   - Compliance reporting

---

## Cost Optimization

### Storage Lifecycle Comparison

**AWS S3:**
- Day 30: Standard-IA (46% savings)
- Day 90: Glacier Instant Retrieval (83% savings)
- Day 180: Glacier Deep Archive (96% savings)

**GCP Cloud Storage:**
- Day 30: Nearline (50% savings)
- Day 90: Coldline (80% savings)
- Day 365: Archive (94% savings)

**Azure Blob Storage:**
- Day 30: Cool (44% savings)
- Day 90: Archive (95% savings)

All providers support automatic lifecycle transitions to reduce costs.

---

## Migration Guide

### Portability Assessment

**Highly Portable (Easy to migrate):**
- ✅ Python application code
- ✅ SFTP client library (Paramiko)
- ✅ Logging patterns
- ✅ Error handling logic
- ✅ Configuration management

**Provider-Specific (Requires adaptation):**
- ⚠️ Infrastructure as Code (Terraform resources)
- ⚠️ IAM/RBAC policies
- ⚠️ Secrets management API calls
- ⚠️ Object storage API calls
- ⚠️ Logging/monitoring integration

### Migration Checklist

See [INFRASTRUCTURE-COMPOSER.md](./INFRASTRUCTURE-COMPOSER.md#migration-checklist) for detailed migration steps.

---

## Use Cases

### 1. Single Cloud Deployment
Deploy on AWS, GCP, or Azure based on your organization's existing infrastructure and requirements.

### 2. Multi-Cloud Redundancy
Deploy the same architecture on multiple clouds for disaster recovery and high availability.

### 3. Cloud Migration
Use the component mapping to plan and execute migrations between cloud providers.

### 4. Hybrid Cloud
Implement on multiple providers with data replication for hybrid cloud scenarios.

### 5. Cost Optimization
Compare costs across providers and choose the most cost-effective option for your use case.

---

## Getting Started

### Step 1: Review Architecture
Read [INFRASTRUCTURE-COMPOSER.md](./INFRASTRUCTURE-COMPOSER.md) to understand the universal architecture.

### Step 2: Choose Cloud Provider
Evaluate your requirements against the provider comparison to select AWS, GCP, or Azure.

### Step 3: Review Component Mapping
Use [COMPONENT-MAPPING-TABLE.md](./COMPONENT-MAPPING-TABLE.md) to find specific services for your chosen provider.

### Step 4: Implement Infrastructure
Follow the Terraform examples in the main documentation to deploy infrastructure.

### Step 5: Deploy Application
Deploy the serverless function code adapted for your chosen provider.

### Step 6: Configure Monitoring
Set up logging, metrics, and alerts using the provider's monitoring services.

### Step 7: Test & Validate
Thoroughly test the file transfer functionality and security controls.

---

## Additional Resources

### AWS Resources
- [AWS Lambda VPC Networking](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html)
- [VPC Gateway Endpoints for S3](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### GCP Resources
- [Cloud Functions VPC Connectivity](https://cloud.google.com/functions/docs/networking/network-settings)
- [Private Google Access](https://cloud.google.com/vpc/docs/private-google-access)
- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)

### Azure Resources
- [Azure Functions VNet Integration](https://docs.microsoft.com/en-us/azure/azure-functions/functions-networking-options)
- [Virtual Network Service Endpoints](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview)
- [Azure Well-Architected Framework](https://docs.microsoft.com/en-us/azure/architecture/framework/)

### Multi-Cloud Terraform
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Terraform AzureRM Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)

---

## Contributing

Contributions to improve the infrastructure composer are welcome! Please:

1. Review the existing documentation
2. Identify areas for improvement or missing information
3. Submit pull requests with clear descriptions
4. Ensure documentation remains cloud-agnostic where possible

---

## License

This documentation is part of the DEA-C01 Secure File Transfer project and is licensed under the MIT License.

---

## Support

For questions or issues:
- Review the detailed documentation in this directory
- Check the main repository README
- Open an issue in the GitHub repository
- Consult cloud provider documentation

---

## Document Information

**Version:** 1.0  
**Last Updated:** 2025-12-21  
**Maintained By:** Infrastructure Team  
**Purpose:** Multi-cloud architecture reference and migration guide

---

## Quick Reference

### Key Takeaways

1. **Architecture is universal** - Same pattern works across AWS, GCP, and Azure
2. **Costs are comparable** - All providers offer similar pricing for this use case
3. **Security is consistent** - Defense-in-depth approach works everywhere
4. **Terraform enables IaC** - Infrastructure can be version controlled and automated
5. **Migration is feasible** - With proper planning, moving between clouds is achievable

### Next Steps

- [ ] Read INFRASTRUCTURE-COMPOSER.md for comprehensive overview
- [ ] Review COMPONENT-MAPPING-TABLE.md for specific service mappings
- [ ] Choose your cloud provider based on requirements
- [ ] Implement infrastructure using Terraform examples
- [ ] Deploy and test the solution
- [ ] Set up monitoring and alerts
- [ ] Document your specific implementation

---

**For detailed technical information, refer to the individual documentation files in this directory.**
