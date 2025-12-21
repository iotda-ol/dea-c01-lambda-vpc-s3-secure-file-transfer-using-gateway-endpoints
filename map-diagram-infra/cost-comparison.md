# Multi-Cloud Cost Comparison

## Overview

This document provides a detailed cost analysis for deploying the secure file transfer architecture across AWS, GCP, and Azure.

---

## Baseline Assumptions

All cost estimates are based on the following workload:

- **Function Executions**: 1,000 invocations per month
- **Execution Duration**: 30 seconds average per invocation
- **Memory Allocation**: 512 MB
- **Storage**: 100 GB stored with lifecycle policies
- **Data Transfer**: Minimal egress (SFTP download is ingress)
- **Logging**: 1 GB per month
- **Region**: US East (or equivalent)

---

## Monthly Cost Breakdown by Provider

### AWS (Amazon Web Services)

| Component | Service | Quantity | Unit Cost | Monthly Cost |
|-----------|---------|----------|-----------|--------------|
| **Compute** | Lambda | 1,000 invocations × 30s | $0.0000166667/GB-sec | $0.25 |
| **Storage (Hot)** | S3 Standard | 100 GB | $0.023/GB | $2.30 |
| **Storage Lifecycle** | Transitions | Automatic | Free | $0.00 |
| **Private Endpoint** | VPC Gateway Endpoint (S3) | 1 endpoint | Free | **$0.00** ✅ |
| **Secrets** | Secrets Manager | 1 secret | $0.40/secret | $0.40 |
| **Logging** | CloudWatch Logs | 1 GB | $0.50/GB | $0.50 |
| **Monitoring** | CloudWatch Metrics | Standard | Free | $0.00 |
| **Scheduler** | EventBridge | 1 rule | Free (< 1M events) | $0.00 |
| **Network** | Data Transfer | Minimal | $0.00 | $0.00 |
| | | | **TOTAL** | **$3.45** |

**AWS Advantages**:
- ✅ **FREE S3 Gateway Endpoint** (saves $32-45/month vs NAT Gateway)
- ✅ Mature services with extensive documentation
- ✅ Wide range of regions and availability zones

---

### GCP (Google Cloud Platform)

| Component | Service | Quantity | Unit Cost | Monthly Cost |
|-----------|---------|----------|-----------|--------------|
| **Compute** | Cloud Functions (2nd gen) | 1,000 invocations × 30s | $0.0000024/GB-sec | $0.24 |
| **Storage (Hot)** | Cloud Storage Standard | 100 GB | $0.020/GB | $2.00 |
| **Storage Lifecycle** | Transitions | Automatic | Free | $0.00 |
| **Private Endpoint** | Private Service Connect | Varies | Minimal | $0.00* |
| **Secrets** | Secret Manager | 1 secret | $0.06/secret | $0.06 |
| **Logging** | Cloud Logging | 1 GB | $0.50/GB | $0.50 |
| **Monitoring** | Cloud Monitoring | Standard | Free | $0.00 |
| **Scheduler** | Cloud Scheduler | 1 job | $0.10/job | $0.10** |
| **VPC Connector** | Serverless VPC Access | 1 connector | $0.00-1.00 | $0.00 |
| **Network** | Data Transfer | Minimal | $0.00 | $0.00 |
| | | | **TOTAL** | **$2.90** |

*Private Service Connect costs vary by configuration  
**First 3 jobs free, then $0.10/job

**GCP Advantages**:
- ✅ **Lowest total cost** among all three providers
- ✅ Cheaper secrets management ($0.06 vs $0.40)
- ✅ Slightly lower compute costs
- ✅ Competitive storage pricing

---

### Azure (Microsoft Azure)

| Component | Service | Quantity | Unit Cost | Monthly Cost |
|-----------|---------|----------|-----------|--------------|
| **Compute** | Azure Functions (Consumption) | 1,000 invocations × 30s | $0.000016/GB-sec | $0.20 |
| **Storage (Hot)** | Blob Storage (Hot) | 100 GB | $0.0184/GB | $1.84 |
| **Storage Lifecycle** | Management policies | Automatic | Free | $0.00 |
| **Private Endpoint** | Private Link | 1 endpoint | $0.01/hour | **$7.20** ⚠️ |
| **Secrets** | Key Vault | 1 secret | $0.03/10K operations | $0.03 |
| **Logging** | Azure Monitor Logs | 1 GB | $2.76/GB*** | $2.76 |
| **Monitoring** | Azure Monitor Metrics | Standard | Included | $0.00 |
| **Application Insights** | Telemetry | 1 GB | Included in logs | $0.00 |
| **Scheduler** | Timer Trigger | Built-in | Free | $0.00 |
| **Network** | Data Transfer | Minimal | $0.00 | $0.00 |
| | | | **TOTAL** | **$12.03** |

***First 5 GB free, then $2.76/GB (can be reduced with retention policies)

**Azure Challenges**:
- ⚠️ **Private Link costs** significantly increase total cost
- ⚠️ Higher logging costs (can be optimized)
- ⚠️ ~3-4x more expensive than GCP

**Azure Advantages**:
- ✅ Lowest compute costs
- ✅ Cheapest secrets management
- ✅ Tight integration with Microsoft ecosystem

**Azure Optimization Options**:
1. **Remove Private Link**: Use Service Endpoints instead → Save $7.20/month
2. **Reduce Log Retention**: 7 days instead of 30 → Save ~$2/month
3. **Optimized Cost**: **~$2.83/month** (comparable to GCP)

---

## Cost Comparison Summary

### Standard Configuration (With Private Connectivity)

| Provider | Monthly Cost | vs Cheapest | Savings vs EC2 ($65) |
|----------|--------------|-------------|---------------------|
| **GCP** | **$2.90** | Baseline | **$62.10 (95.5%)** |
| **AWS** | **$3.45** | +19% | **$61.55 (94.7%)** |
| **Azure** | **$12.03** | +315% | **$52.97 (81.5%)** |

### Optimized Configuration (Azure without Private Link)

| Provider | Monthly Cost | vs Cheapest | Savings vs EC2 ($65) |
|----------|--------------|-------------|---------------------|
| **Azure (optimized)** | **$2.83** | -2% | **$62.17 (95.6%)** |
| **GCP** | **$2.90** | Baseline | **$62.10 (95.5%)** |
| **AWS** | **$3.45** | +19% | **$61.55 (94.7%)** |

---

## Annual Cost Projection

### 5-Year Total Cost of Ownership (TCO)

| Provider | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 | **5-Year Total** |
|----------|--------|--------|--------|--------|--------|------------------|
| **GCP** | $34.80 | $34.80 | $34.80 | $34.80 | $34.80 | **$174.00** |
| **AWS** | $41.40 | $41.40 | $41.40 | $41.40 | $41.40 | **$207.00** |
| **Azure (standard)** | $144.36 | $144.36 | $144.36 | $144.36 | $144.36 | **$721.80** |
| **Azure (optimized)** | $33.96 | $33.96 | $33.96 | $33.96 | $33.96 | **$169.80** |

### vs Traditional EC2 Architecture

| Architecture | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 | **5-Year Total** |
|--------------|--------|--------|--------|--------|--------|------------------|
| **EC2 + NAT Gateway** | $780 | $780 | $780 | $780 | $780 | **$3,900** |
| **GCP (serverless)** | $35 | $35 | $35 | $35 | $35 | **$174** |
| **Savings** | $745 | $745 | $745 | $745 | $745 | **$3,726 (95.5%)** |

---

## Cost Drivers Analysis

### Compute Costs

| Provider | 1,000 invocations | 10,000 invocations | 100,000 invocations |
|----------|-------------------|--------------------|---------------------|
| **GCP** | $0.24 | $2.40 | $24.00 |
| **AWS** | $0.25 | $2.50 | $25.00 |
| **Azure** | $0.20 | $2.00 | $20.00 |

**Winner**: Azure (20% cheaper than AWS)

### Storage Costs (100 GB)

| Provider | Hot Tier | Cool Tier (30d) | Archive (90d) | Deep Archive (180d) |
|----------|----------|-----------------|---------------|---------------------|
| **GCP** | $2.00 | $1.00 | $0.40 | $0.12 |
| **AWS** | $2.30 | $1.25 | $0.40 | $0.10 |
| **Azure** | $1.84 | $1.00 | $0.20 | N/A (Archive only) |

**Winner**: Azure for hot tier, tied for archive tiers

### Secrets Management

| Provider | Per Secret/Month | 10 Secrets | 100 Secrets |
|----------|------------------|------------|-------------|
| **Azure** | $0.03 | $0.30 | $3.00 |
| **GCP** | $0.06 | $0.60 | $6.00 |
| **AWS** | $0.40 | $4.00 | $40.00 |

**Winner**: Azure (90% cheaper than AWS)

### Private Connectivity

| Provider | Service | Cost/Month | Data Charges |
|----------|---------|------------|--------------|
| **AWS** | VPC Gateway Endpoint (S3) | **$0.00** ✅ | $0.00 |
| **GCP** | Private Service Connect | $0.00-1.00 | Varies |
| **Azure** | Private Link | **$7.20** ⚠️ | $0.01/GB processed |

**Winner**: AWS (completely free for S3)

---

## Scaling Cost Analysis

### Scenario: 10x Increase (10,000 invocations/month, 1TB storage)

| Provider | Compute | Storage | Private Endpoint | Secrets | Logging | **Total** |
|----------|---------|---------|------------------|---------|---------|-----------|
| **GCP** | $2.40 | $20.00 | $0.00 | $0.06 | $2.00 | **$24.46** |
| **AWS** | $2.50 | $23.00 | $0.00 | $0.40 | $2.00 | **$27.90** |
| **Azure** | $2.00 | $18.40 | $7.20 | $0.03 | $10.00 | **$37.63** |
| **Azure (opt)** | $2.00 | $18.40 | $0.00 | $0.03 | $3.00 | **$23.43** |

---

## Cost Optimization Strategies

### Universal Strategies (All Clouds)

1. **Storage Lifecycle Policies**
   - Transition to cheaper tiers after 30/90/180 days
   - Can save 50-95% on storage costs
   - Automatic with no manual intervention

2. **Right-size Compute**
   - Start with 512 MB memory
   - Monitor and adjust based on actual usage
   - 256 MB may be sufficient for small files

3. **Optimize Logging**
   - 7-14 day retention for most use cases
   - Use log sampling in high-volume scenarios
   - Archive old logs to object storage

4. **Minimize Secrets**
   - Use single secret with JSON structure
   - Avoid creating separate secrets for each credential

5. **Use Spot/Preemptible Instances** (if using VMs)
   - Not applicable to serverless, but relevant for EC2/GCE/VMs

### AWS-Specific Optimizations

1. ✅ Use VPC Gateway Endpoint (already free)
2. Use S3 Intelligent-Tiering for automatic optimization
3. Enable S3 Bucket Key to reduce KMS costs
4. Use AWS Budgets to track spending

### GCP-Specific Optimizations

1. Use Committed Use Discounts (CUD) for predictable workloads
2. Autoclass for Cloud Storage (automatic tiering)
3. Set up billing alerts and budgets
4. Use Nearline/Coldline/Archive aggressively

### Azure-Specific Optimizations

1. ⚠️ **Remove Private Link** if security allows (save $7.20/month)
2. Use Service Endpoints instead of Private Link (free)
3. Reduce Application Insights sampling rate
4. Use 7-day log retention
5. Consider Azure Reservations for predictable workloads

---

## Break-Even Analysis

### When does each provider become most cost-effective?

**Small Scale (< 5,000 invocations/month)**:
- **Winner: GCP** ($2.90-12.00/month)
- Close second: Azure (optimized) ($2.83-10.00/month)

**Medium Scale (5,000-50,000 invocations/month)**:
- **Winner: GCP** ($10-100/month)
- AWS competitive if S3-heavy workload

**Large Scale (> 50,000 invocations/month)**:
- **Winner: Azure (compute-heavy)** or **GCP (balanced)**
- AWS competitive with volume discounts

**Storage-Heavy Workloads (> 1 TB)**:
- **Winner: GCP** (cheaper storage with lifecycle)
- Azure close second for hot tier

---

## Hidden Costs to Consider

### AWS
- Data transfer OUT (first 1 GB free, then $0.09/GB)
- KMS requests (if using customer-managed keys)
- NAT Gateway if not using VPC endpoint ($0.045/GB + $0.045/hour)

### GCP
- Network egress (first 1 GB free, then varies)
- VPC Connector costs (can add $0-2/month)
- Cloud Scheduler beyond 3 jobs

### Azure
- Private Link data processing ($0.01/GB)
- Application Insights data ingestion (beyond 5 GB)
- Storage transaction costs

---

## Recommendations by Use Case

### Best for Cost-Conscious Projects
**Winner: GCP** ($2.90/month)
- Lowest baseline cost
- Predictable pricing
- Great for startups and small teams

### Best for AWS-Native Environments
**Winner: AWS** ($3.45/month)
- Free S3 Gateway Endpoint
- Mature ecosystem
- Best for existing AWS customers

### Best for Enterprise/Microsoft Shops
**Winner: Azure (optimized)** ($2.83/month)
- Tight Azure AD integration
- Excellent for Microsoft-centric organizations
- Requires optimization (remove Private Link)

### Best for Multi-Cloud Strategy
**Winner: GCP or AWS**
- Both have competitive pricing
- Terraform support for both is excellent
- Avoid Azure if Private Link is required

---

## Cost Monitoring Tools

### AWS
- AWS Cost Explorer
- AWS Budgets
- AWS Cost and Usage Reports
- CloudWatch Billing Alarms

### GCP
- Cloud Billing Reports
- Budget Alerts
- Cost Table Reports
- Recommender (cost optimization suggestions)

### Azure
- Cost Management + Billing
- Azure Advisor (cost recommendations)
- Budget Alerts
- Cost Analysis

---

## Conclusion

**Summary**:
1. **GCP is the most cost-effective** for standard configurations ($2.90/month)
2. **Azure can be competitive** if optimized ($2.83/month without Private Link)
3. **AWS offers best value** when S3 Gateway Endpoint advantage is considered
4. **All three are 90-95% cheaper** than traditional EC2/VM-based solutions

**Recommendation**:
- **Choose GCP** for greenfield projects or cost-sensitive workloads
- **Choose AWS** if already in AWS ecosystem or need S3-specific features
- **Choose Azure** (optimized) if in Microsoft ecosystem and can use Service Endpoints

**Bottom Line**: Any of these serverless architectures will save you **$60+/month** compared to traditional EC2 + NAT Gateway solutions.
