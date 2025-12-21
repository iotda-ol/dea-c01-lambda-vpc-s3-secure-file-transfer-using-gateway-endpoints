# Universal Cloud Architecture Documentation

## Overview

This document describes the cloud-agnostic architecture for secure file transfer from legacy SFTP systems to modern cloud object storage. The architecture is designed to be deployable across **AWS**, **GCP**, and **Azure** with minimal modifications.

---

## 1. Core Architecture Principles

### 1.1 Cloud-Agnostic Design Patterns

The architecture follows these universal patterns:

1. **Network Isolation Pattern**
   - Compute resources run in private virtual networks
   - No direct internet access for cloud service communication
   - Private connectivity to object storage services

2. **Serverless Compute Pattern**
   - Event-driven, pay-per-use execution
   - No server management overhead
   - Automatic scaling and high availability

3. **Least Privilege Security Pattern**
   - Minimal required permissions for each component
   - Identity-based access control
   - No long-lived credentials

4. **Encryption Everywhere Pattern**
   - Data encrypted in transit (TLS/SSH)
   - Data encrypted at rest (AES-256)
   - Managed encryption keys

5. **Cost Optimization Pattern**
   - Serverless pay-per-use pricing
   - Automatic storage tiering
   - No expensive network gateways

---

## 2. Logical Architecture

### 2.1 Component Model

```
External System Layer
    └─ Legacy SFTP Server (external)

Compute Layer
    └─ Serverless Function (event-driven)

Network Layer
    ├─ Virtual Private Network
    ├─ Private Subnets (multi-AZ)
    ├─ Route Tables
    ├─ Private Service Endpoint
    └─ Network Security Controls

Storage Layer
    ├─ Object Storage (primary)
    └─ Lifecycle Policies (automated tiering)

Security Layer
    ├─ Secrets Vault
    ├─ Identity & Access Management
    └─ Encryption Services

Observability Layer
    ├─ Logging Service
    ├─ Metrics Service
    └─ Alerting Service

Orchestration Layer
    └─ Scheduler/Trigger Service
```

### 2.2 Data Flow

```
Step 1: Scheduler triggers Serverless Function
        ↓
Step 2: Function retrieves credentials from Secrets Vault
        ↓
Step 3: Function establishes SFTP connection to external server
        ↓
Step 4: Function downloads files from SFTP server
        ↓
Step 5: Function uploads files to Object Storage via Private Endpoint
        ↓
Step 6: Function logs activity to Logging Service
        ↓
Step 7: Lifecycle policies automatically tier storage (over time)
```

---

## 3. Universal Components

### 3.1 Virtual Network

**Purpose**: Provide isolated network environment for compute resources

**Key Features**:
- Private IP address space (RFC 1918: 10.0.0.0/16)
- Multiple private subnets across availability zones
- Internal DNS resolution
- Route tables for traffic management
- No public internet gateways (for storage traffic)

**Configuration**:
```yaml
Network:
  CIDR: 10.0.0.0/16
  Subnets:
    - Name: PrivateSubnet1
      CIDR: 10.0.1.0/24
      AvailabilityZone: Zone-A
    - Name: PrivateSubnet2
      CIDR: 10.0.2.0/24
      AvailabilityZone: Zone-B
  DNS:
    Enabled: true
    Hostnames: true
```

---

### 3.2 Serverless Compute Function

**Purpose**: Execute file transfer logic on-demand

**Key Features**:
- Event-driven execution
- VPC integration for private networking
- Automatic scaling (0 to N instances)
- Managed runtime environment
- Pay-per-invocation pricing

**Configuration**:
```yaml
Function:
  Runtime: Python 3.11
  Memory: 512 MB
  Timeout: 300 seconds (5 minutes)
  VPC:
    Enabled: true
    Subnets: [PrivateSubnet1, PrivateSubnet2]
  Environment:
    STORAGE_BUCKET: <bucket-name>
    SECRETS_ID: <secrets-identifier>
    SFTP_REMOTE_PATH: /remote/path
    LOG_LEVEL: INFO
```

**Handler Pattern**:
```python
def handler(event, context):
    """
    Universal handler pattern for file transfer
    """
    # 1. Get SFTP credentials from secrets vault
    credentials = get_secret(SECRETS_ID)
    
    # 2. Connect to SFTP server
    sftp_client = connect_sftp(credentials)
    
    # 3. Download files
    files = download_files(sftp_client, REMOTE_PATH)
    
    # 4. Upload to object storage
    for file in files:
        upload_to_storage(file, STORAGE_BUCKET)
    
    # 5. Log results
    log_activity(files)
    
    return {
        'status': 'success',
        'files_transferred': len(files)
    }
```

---

### 3.3 Object Storage

**Purpose**: Scalable, durable storage for transferred files

**Key Features**:
- Virtually unlimited capacity
- 99.999999999% (11 nines) durability
- Automatic replication across zones
- Object versioning
- Lifecycle policies for cost optimization
- Server-side encryption

**Configuration**:
```yaml
Storage:
  Name: file-transfer-bucket
  Encryption:
    Type: AES-256
    Managed: true
  Versioning:
    Enabled: true
  PublicAccess:
    Blocked: true
  Lifecycle:
    Rules:
      - ID: transition-to-infrequent
        Enabled: true
        Days: 30
        TargetClass: InfrequentAccess
      - ID: transition-to-archive
        Enabled: true
        Days: 90
        TargetClass: Archive
      - ID: transition-to-deep-archive
        Enabled: true
        Days: 180
        TargetClass: DeepArchive
      - ID: delete-old-versions
        Enabled: true
        NoncurrentDays: 90
        Action: Delete
```

**Storage Tiers**:
| Days | Tier | Use Case | Cost (relative) |
|------|------|----------|-----------------|
| 0-30 | Standard | Frequent access | 100% |
| 30-90 | Infrequent Access | Monthly access | 50% |
| 90-180 | Archive | Rare access | 20% |
| 180+ | Deep Archive | Compliance/backup | 5% |

---

### 3.4 Private Service Endpoint

**Purpose**: Secure, private connectivity to object storage

**Key Features**:
- Traffic never leaves cloud provider network
- No internet gateway or NAT gateway required
- Lower latency than internet routing
- Cost-effective (free or low-cost depending on provider)
- Automatic route table integration

**Benefits**:
- **Security**: Data never exposed to internet
- **Performance**: Lower latency, higher throughput
- **Cost**: Eliminates NAT gateway costs ($32-45/month per AZ)
- **Compliance**: Meets data residency requirements

**Configuration**:
```yaml
PrivateEndpoint:
  Type: Gateway  # or Interface depending on service
  Service: ObjectStorage
  VPC: <vpc-id>
  RouteTables: [<route-table-id>]
  Policy:
    Effect: Allow
    Principal: <function-role>
    Actions:
      - PutObject
      - GetObject
      - ListBucket
    Resources:
      - <storage-bucket-arn>
```

---

### 3.5 Secrets Vault

**Purpose**: Secure storage for sensitive credentials

**Key Features**:
- Encrypted storage with managed keys
- Automatic versioning
- Access logging and auditing
- Programmatic retrieval
- Optional automatic rotation

**Stored Secrets**:
```json
{
  "sftp_host": "sftp.example.com",
  "sftp_port": 22,
  "sftp_username": "transfer_user",
  "sftp_password": "encrypted_password",
  "sftp_private_key": "-----BEGIN RSA PRIVATE KEY-----..."
}
```

**Access Pattern**:
```python
def get_secret(secret_id):
    """
    Retrieve secret from vault (cloud-agnostic pattern)
    """
    # AWS: boto3.client('secretsmanager').get_secret_value()
    # GCP: secretmanager.SecretManagerServiceClient().access_secret_version()
    # Azure: SecretClient().get_secret()
    
    return parse_secret(response)
```

---

### 3.6 Identity & Access Management

**Purpose**: Control who/what can access resources

**Principles**:
1. **Least Privilege**: Grant minimum required permissions
2. **Service Identity**: Use managed identities (not users)
3. **No Long-term Credentials**: Temporary credentials only
4. **Explicit Deny**: Default deny all, explicitly allow

**Function Permissions**:
```yaml
Permissions:
  - Resource: ObjectStorage
    Actions:
      - PutObject
      - PutObjectAcl
      - GetObject
      - ListBucket
    Scope: <storage-bucket>
  
  - Resource: SecretsVault
    Actions:
      - GetSecretValue
      - DescribeSecret
    Scope: <secret-id>
  
  - Resource: LoggingService
    Actions:
      - CreateLogStream
      - PutLogEvents
    Scope: <log-group>
  
  - Resource: NetworkInterfaces
    Actions:
      - CreateNetworkInterface
      - DescribeNetworkInterfaces
      - DeleteNetworkInterface
    Scope: "*"  # Required for VPC-enabled functions
```

---

### 3.7 Logging & Monitoring

**Purpose**: Operational visibility and troubleshooting

**Key Features**:
- Centralized log aggregation
- Structured logging (JSON format)
- Real-time log streaming
- Log retention policies
- Query and analysis tools

**Logged Data**:
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "function": "file-transfer",
  "event": "transfer_completed",
  "details": {
    "sftp_host": "sftp.example.com",
    "files_transferred": 15,
    "total_size_bytes": 104857600,
    "duration_seconds": 45,
    "storage_bucket": "file-transfer-bucket",
    "storage_prefix": "uploads/2024-01-15/"
  }
}
```

**Metrics**:
- Function invocations (count)
- Function duration (milliseconds)
- Function errors (count)
- Function memory usage (MB)
- Storage operations (count)
- Data transferred (bytes)

**Alerts**:
- Function errors > threshold
- Function duration > timeout threshold
- Storage operation failures
- Unexpected SFTP connection failures

---

### 3.8 Scheduler

**Purpose**: Trigger periodic function execution

**Key Features**:
- Cron-based scheduling
- Timezone support
- Automatic retry on failure
- Event payload customization

**Configuration**:
```yaml
Schedule:
  Enabled: true
  Expression: "cron(0 2 * * ? *)"  # Daily at 2:00 AM UTC
  Timezone: UTC
  Target: <function-identifier>
  Payload:
    mode: batch
    source_path: /incoming
    destination_prefix: uploads/
```

**Schedule Examples**:
- Daily: `cron(0 2 * * ? *)`
- Hourly: `cron(0 * * * ? *)`
- Every 15 minutes: `cron(0/15 * * * ? *)`
- Weekdays only: `cron(0 8 ? * MON-FRI *)`

---

### 3.9 Network Security

**Purpose**: Control network traffic to/from function

**Firewall Rules**:
```yaml
Ingress:
  - Action: DENY
    Protocol: ALL
    Source: 0.0.0.0/0
    Description: "Deny all inbound (functions don't need ingress)"

Egress:
  - Action: ALLOW
    Protocol: TCP
    Port: 443
    Destination: 0.0.0.0/0
    Description: "HTTPS to object storage via private endpoint"
  
  - Action: ALLOW
    Protocol: TCP
    Port: 22
    Destination: <sftp-server-ip>
    Description: "SSH/SFTP to legacy server"
  
  - Action: DENY
    Protocol: ALL
    Destination: 0.0.0.0/0
    Description: "Deny all other outbound"
```

---

## 4. Deployment Architecture

### 4.1 Infrastructure as Code

**Recommended Tools**:
- **Terraform**: Multi-cloud support, large ecosystem
- **Pulumi**: Programming language-based (Python, TypeScript, Go)
- **Crossplane**: Kubernetes-based, cloud-agnostic

**Directory Structure**:
```
infrastructure/
├── main.tf                    # Provider and backend config
├── variables.tf               # Input variables
├── outputs.tf                 # Output values
├── modules/
│   ├── network/              # VPC, subnets, routing
│   ├── compute/              # Serverless function
│   ├── storage/              # Object storage, lifecycle
│   ├── security/             # IAM, secrets, firewall
│   ├── monitoring/           # Logging, metrics, alerts
│   └── orchestration/        # Scheduler
└── environments/
    ├── dev/                  # Development environment
    ├── staging/              # Staging environment
    └── prod/                 # Production environment
```

### 4.2 Multi-Environment Strategy

**Environments**:
1. **Development**: Testing, rapid iteration, minimal costs
2. **Staging**: Pre-production validation, mirrored config
3. **Production**: Live workloads, high availability, monitoring

**Environment Variables**:
```yaml
# Dev
Environment: dev
VPC_CIDR: 10.0.0.0/16
Function_Memory: 512
Function_Timeout: 300
Storage_Lifecycle: Disabled
Log_Retention: 3

# Staging
Environment: staging
VPC_CIDR: 10.1.0.0/16
Function_Memory: 512
Function_Timeout: 300
Storage_Lifecycle: Enabled
Log_Retention: 7

# Production
Environment: prod
VPC_CIDR: 10.2.0.0/16
Function_Memory: 1024  # Higher for prod
Function_Timeout: 600
Storage_Lifecycle: Enabled
Log_Retention: 30
```

---

## 5. Operational Patterns

### 5.1 Deployment Pipeline

```
1. Code Commit → Git Repository
2. Automated Tests → Unit, Integration, Security
3. Build Artifact → Function package (ZIP)
4. Infrastructure Validation → terraform plan
5. Deploy Infrastructure → terraform apply
6. Deploy Function Code → Upload to cloud provider
7. Smoke Tests → Basic functionality check
8. Production Traffic → Enable scheduler
```

### 5.2 Monitoring Strategy

**Key Metrics**:
- Function success rate: Target > 99.5%
- Function duration: Target < 60 seconds
- File transfer rate: Files/hour
- Error rate: < 0.5% of invocations

**Alerting**:
- Critical: Function failure rate > 5%
- Warning: Function duration > 80% of timeout
- Info: Storage lifecycle transitions

### 5.3 Disaster Recovery

**Backup Strategy**:
- Object storage: Versioning + Cross-region replication
- Secrets: Automated backups
- Infrastructure: Version-controlled IaC

**Recovery Objectives**:
- RPO (Recovery Point Objective): 1 hour
- RTO (Recovery Time Objective): 4 hours

---

## 6. Cost Optimization

### 6.1 Cost Drivers

1. **Compute**: Pay per invocation + duration
2. **Storage**: Pay per GB stored + lifecycle tier
3. **Network**: Private endpoint costs (varies by provider)
4. **Secrets**: Per secret per month
5. **Logging**: Per GB ingested + storage

### 6.2 Optimization Strategies

1. **Use Private Endpoints**: Save $32-45/month (no NAT gateway)
2. **Serverless Compute**: No idle costs
3. **Storage Lifecycle**: Automatic tiering saves 50-95%
4. **Log Retention**: 7-30 days, not indefinite
5. **Right-size Function**: 512MB is often optimal

### 6.3 Cost Comparison

| Architecture | Monthly Cost |
|--------------|--------------|
| EC2 + NAT Gateway | $65-100 |
| **This Architecture** | **$2.80-9.73** |
| **Savings** | **90-95%** |

---

## 7. Security Best Practices

1. **Network**: Private subnets, no public IPs
2. **Encryption**: TLS in transit, AES-256 at rest
3. **Secrets**: Vault storage, no hardcoded credentials
4. **IAM**: Least privilege, service identities
5. **Logging**: Comprehensive audit trail
6. **Compliance**: GDPR, HIPAA, SOC2 ready

---

## 8. Conclusion

This universal architecture provides:
- ✅ **Multi-cloud portability** across AWS, GCP, Azure
- ✅ **90-95% cost reduction** vs traditional architectures
- ✅ **Enterprise-grade security** with defense-in-depth
- ✅ **High availability** with multi-AZ deployment
- ✅ **Operational excellence** with IaC and monitoring
- ✅ **Scalability** from 1 to 1M+ file transfers

The architecture can be deployed on any major cloud provider with minimal modifications, making it ideal for multi-cloud strategies or cloud migrations.
