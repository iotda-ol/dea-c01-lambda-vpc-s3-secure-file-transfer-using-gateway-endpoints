# Cloud-Agnostic Architecture Diagram
# Universal infrastructure diagram using Mermaid

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#E8F4F8','secondaryColor':'#D4E9F7','tertiaryColor':'#C0DDF5'}}}%%

graph TB
    subgraph External["🌐 External Systems"]
        SFTP[("Legacy SFTP Server<br/>Port 22<br/>SSH Protocol")]
        Admin["👤 Administrator"]
    end

    subgraph CloudProvider["☁️ Cloud Provider (AWS/GCP/Azure)"]
        
        subgraph VirtualNetwork["🔒 Virtual Network (10.0.0.0/16)"]
            
            subgraph PrivateSubnet1["Private Subnet 1<br/>10.0.1.0/24<br/>Zone A"]
                Function1["⚡ Serverless Function<br/>Runtime: Python 3.11<br/>Memory: 512MB<br/>Timeout: 300s"]
            end
            
            subgraph PrivateSubnet2["Private Subnet 2<br/>10.0.2.0/24<br/>Zone B"]
                Function2["⚡ Serverless Function<br/>(Standby/HA)"]
            end
            
            subgraph NetworkSecurity["🛡️ Network Security"]
                Firewall["Firewall Rules<br/>- Allow HTTPS (443) to Storage<br/>- Allow SSH (22) to SFTP<br/>- Deny all other egress"]
            end
            
            subgraph ServiceEndpoint["🔌 Private Service Endpoint"]
                Gateway["Storage Gateway<br/>Type: Gateway/Private<br/>Cost: FREE<br/>No Internet Traversal"]
            end
        end
        
        subgraph ObjectStorage["💾 Object Storage"]
            Bucket["Storage Bucket<br/>✓ Encryption at rest<br/>✓ Versioning enabled<br/>✓ Public access blocked"]
            Lifecycle["Lifecycle Policies<br/>Day 30 → Infrequent Access<br/>Day 90 → Archive<br/>Day 180 → Deep Archive"]
        end
        
        subgraph IAM["🔐 Identity & Access"]
            ServiceIdentity["Service Identity<br/>for Serverless Function"]
            Policies["Access Policies<br/>- Read/Write Storage<br/>- Read Secrets<br/>- Write Logs<br/>- Network Interface"]
        end
        
        subgraph Secrets["🔑 Secrets Management"]
            SecretStore["Secrets Vault<br/>Encrypted Credentials<br/>- SFTP Username<br/>- SFTP Password<br/>- SFTP Host<br/>- SFTP Port"]
        end
        
        subgraph Monitoring["📊 Monitoring & Logging"]
            Logs["Centralized Logging<br/>Retention: 7-30 days"]
            Metrics["Metrics<br/>- Invocations<br/>- Duration<br/>- Errors<br/>- Memory"]
            Alarms["Alarms<br/>Threshold: >5 errors/5min"]
        end
        
        subgraph Automation["⏰ Automation"]
            Scheduler["Event Scheduler<br/>Schedule: Daily 2 AM UTC<br/>cron(0 2 * * *)"]
        end
    end

    %% Data Flow - Scheduled Execution
    Scheduler -->|"1. Trigger"| Function1
    
    %% Function initialization
    Function1 -->|"2. Retrieve Credentials"| SecretStore
    
    %% SFTP Connection
    Function1 -.->|"3. Connect SSH/SFTP<br/>Port 22<br/>Internet"| SFTP
    SFTP -.->|"4. Download Files"| Function1
    
    %% Storage Upload via Private Endpoint
    Function1 -->|"5. Upload via Private Endpoint<br/>HTTPS (443)<br/>No Internet"| Gateway
    Gateway -->|"Private Network<br/>No Data Charges"| Bucket
    
    %% Lifecycle
    Bucket -->|"Automatic Transition"| Lifecycle
    
    %% Logging
    Function1 -->|"6. Log Events"| Logs
    Function1 -->|"Emit Metrics"| Metrics
    Metrics -->|"Check Thresholds"| Alarms
    
    %% IAM
    Function1 -.->|"Assumes Identity"| ServiceIdentity
    ServiceIdentity -.->|"Grants Permissions"| Policies
    
    %% Security Rules
    Firewall -.->|"Enforces Rules"| Function1
    
    %% Admin Access
    Admin -.->|"View Logs & Metrics"| Monitoring
    Admin -.->|"Monitor Bucket"| Bucket

    %% Styling
    classDef externalClass fill:#FFE6E6,stroke:#FF6B6B,stroke-width:2px
    classDef computeClass fill:#E6F3FF,stroke:#4A90E2,stroke-width:2px
    classDef storageClass fill:#E6FFE6,stroke:#66BB6A,stroke-width:2px
    classDef securityClass fill:#FFF4E6,stroke:#FFA726,stroke-width:2px
    classDef monitorClass fill:#F3E5F5,stroke:#AB47BC,stroke-width:2px
    
    class SFTP,Admin externalClass
    class Function1,Function2,Scheduler computeClass
    class Bucket,Lifecycle,Gateway storageClass
    class Firewall,ServiceIdentity,Policies,SecretStore securityClass
    class Logs,Metrics,Alarms monitorClass
```

## Architecture Components

### 1. **Virtual Network (VPC/VNet)**
- **Purpose**: Isolated network for secure compute resources
- **CIDR**: 10.0.0.0/16
- **Subnets**: 2 private subnets across availability zones

### 2. **Serverless Function**
- **Runtime**: Python 3.11
- **Memory**: 512 MB
- **Timeout**: 300 seconds (5 minutes)
- **Network**: Deployed in private subnets
- **HA**: Distributed across multiple zones

### 3. **Private Service Endpoint** ⭐ KEY COST SAVER
- **Type**: Gateway/Private endpoint to object storage
- **Cost**: **FREE** (saves ~$32/month vs NAT Gateway)
- **Benefit**: Private connectivity without internet traversal
- **Implementation**:
  - **AWS**: S3 VPC Gateway Endpoint
  - **GCP**: Private Google Access
  - **Azure**: Storage Service Endpoint

### 4. **Object Storage**
- **Features**:
  - Server-side encryption (AES-256)
  - Versioning enabled
  - Public access blocked
  - Lifecycle policies for cost optimization

### 5. **Network Security**
- **Firewall Rules**:
  - Allow HTTPS (443) to storage via private endpoint
  - Allow SSH (22) to legacy SFTP server
  - Deny all other outbound traffic

### 6. **Identity & Access Management**
- Service identity for serverless function
- Least privilege access policies
- No hardcoded credentials

### 7. **Secrets Management**
- Encrypted storage for SFTP credentials
- Accessed by function at runtime
- Automatic rotation support

### 8. **Monitoring & Logging**
- Centralized logging with configurable retention
- Metrics for performance tracking
- Alarms for error detection

### 9. **Automation**
- Scheduled trigger (daily, weekly, etc.)
- Event-driven execution

## Data Flow

```
┌─────────────┐
│  Scheduler  │ Daily at 2 AM UTC
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  Step 1: Trigger Serverless Function        │
└──────┬──────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  Step 2: Retrieve SFTP Credentials          │
│  from Secrets Manager                       │
└──────┬──────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  Step 3: Connect to SFTP Server             │
│  (over internet, port 22)                   │
└──────┬──────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  Step 4: Download Files from SFTP           │
└──────┬──────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  Step 5: Upload to Object Storage           │
│  via Private Service Endpoint               │
│  (no internet, no NAT, FREE)                │
└──────┬──────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│  Step 6: Log Execution Details              │
│  and Emit Metrics                           │
└─────────────────────────────────────────────┘
```

## Security Layers

### Network Security
- ✓ Private subnets (no direct internet for storage)
- ✓ Firewall rules (restrictive outbound)
- ✓ Private service endpoint (no internet traversal)

### Data Security
- ✓ Encryption in transit (SFTP, TLS/HTTPS)
- ✓ Encryption at rest (storage service)
- ✓ Versioning enabled

### Identity Security
- ✓ Service identity (no access keys)
- ✓ Least privilege IAM policies
- ✓ Secrets manager for credentials

### Monitoring Security
- ✓ Centralized logging
- ✓ Metrics and alarms
- ✓ Audit trail

## Cost Optimization

### Key Savings
1. **Private Service Endpoint**: FREE (saves $32/month vs NAT Gateway)
2. **Serverless Compute**: Pay per execution (~$0.25/month for 1000 executions)
3. **Lifecycle Policies**: Up to 96% savings on archived data
4. **Log Retention**: 7-30 days to minimize storage costs

### Monthly Cost Estimate (1000 executions, 100GB data)
| Component | Cost |
|-----------|------|
| Serverless Function | $0.25 |
| Object Storage (with lifecycle) | $2.00-2.30 |
| Storage Requests | $0.01 |
| Secrets Manager | $0.06-0.40 |
| Logging | $0.05 |
| Private Endpoint | **$0.00** (FREE) ⭐ |
| **Total** | **$2.37-3.01/month** |

**Savings vs NAT Gateway**: ~91-93% cost reduction

## High Availability

- Multi-zone deployment
- Automatic failover
- Distributed function instances
- Redundant storage (multiple copies)

## Scalability

- Serverless auto-scaling
- Concurrent executions
- No infrastructure management
- Pay per use

## Cloud Provider Equivalents

| Component | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| Virtual Network | VPC | VPC Network | Virtual Network |
| Private Subnet | Subnet | Subnet | Subnet |
| Firewall | Security Group | Firewall Rules | NSG |
| **Private Endpoint** | **S3 Gateway Endpoint (FREE)** | **Private Google Access (FREE)** | **Service Endpoint (FREE)** |
| Serverless Function | Lambda | Cloud Functions / Cloud Run | Azure Functions |
| Object Storage | S3 | Cloud Storage | Blob Storage |
| Service Identity | IAM Role | Service Account | Managed Identity |
| Secrets | Secrets Manager | Secret Manager | Key Vault |
| Logging | CloudWatch Logs | Cloud Logging | Log Analytics |
| Metrics | CloudWatch | Cloud Monitoring | Azure Monitor |
| Scheduler | EventBridge | Cloud Scheduler | Logic Apps / Timer |
