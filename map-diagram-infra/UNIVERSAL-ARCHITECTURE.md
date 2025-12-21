# Universal Cloud Architecture - Secure File Transfer Solution

## Overview

This document describes a cloud-agnostic architecture for securely transferring files from legacy SFTP systems to cloud object storage using serverless compute with private network connectivity.

---

## High-Level Architecture (Universal)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLOUD PLATFORM                                     │
│                        (AWS / GCP / Azure)                                   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    VIRTUAL PRIVATE NETWORK                              │ │
│  │                     (VPC / VPC / VNet)                                  │ │
│  │                      CIDR: 10.0.0.0/16                                  │ │
│  │                                                                          │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │  │              PRIVATE SUBNET (Multi-AZ/Multi-Zone)                │   │ │
│  │  │                    CIDR: 10.0.1.0/24, 10.0.2.0/24                │   │ │
│  │  │                                                                   │   │ │
│  │  │   ┌───────────────────────────────────────────────────────┐     │   │ │
│  │  │   │       SERVERLESS COMPUTE FUNCTION                     │     │   │ │
│  │  │   │   (Lambda / Cloud Functions / Azure Functions)        │     │   │ │
│  │  │   │                                                        │     │   │ │
│  │  │   │   Runtime: Python 3.11                                │     │   │ │
│  │  │   │   Memory: 512 MB                                      │     │   │ │
│  │  │   │   Timeout: 300 seconds                                │     │   │ │
│  │  │   │                                                        │     │   │ │
│  │  │   │   Capabilities:                                       │     │   │ │
│  │  │   │   • Connect to SFTP server                            │     │   │ │
│  │  │   │   • Download files                                    │     │   │ │
│  │  │   │   • Upload to object storage                          │     │   │ │
│  │  │   │   • Handle errors and retries                         │     │   │ │
│  │  │   │   • Log all operations                                │     │   │ │
│  │  │   │                                                        │     │   │ │
│  │  │   └───────────┬────────────────────┬──────────────────────┘     │   │ │
│  │  │               │                    │                            │   │ │
│  │  └───────────────┼────────────────────┼────────────────────────────┘   │ │
│  │                  │                    │                                │ │
│  │                  │ Port 22 (SFTP)     │ Port 443 (HTTPS)               │ │
│  │                  │ via NAT/IGW        │ Private Connection             │ │
│  │                  │                    │                                │ │
│  │  ┌───────────────▼──────────────┐     │                                │ │
│  │  │    NETWORK SECURITY          │     │                                │ │
│  │  │  (Security Group / NSG)      │     │                                │ │
│  │  │                              │     │                                │ │
│  │  │  Egress Rules:               │     │                                │ │
│  │  │  • HTTPS (443) → Storage     │     │                                │ │
│  │  │  • SSH (22) → SFTP Server    │     │                                │ │
│  │  └──────────────────────────────┘     │                                │ │
│  │                                        │                                │ │
│  │  ┌─────────────────────────────────────▼──────────────────────────┐   │ │
│  │  │              PRIVATE SERVICE ENDPOINT                          │   │ │
│  │  │  (VPC Gateway Endpoint / Private Service Connect /             │   │ │
│  │  │   Private Endpoint)                                            │   │ │
│  │  │                                                                 │   │ │
│  │  │  Purpose: Private connection to Object Storage                 │   │ │
│  │  │  Cost: FREE (AWS S3), ~$0.01/hr (GCP/Azure)                   │   │ │
│  │  │  Security: Traffic never leaves cloud backbone                │   │ │
│  │  │                                                                 │   │ │
│  │  └─────────────────────────────────────┬──────────────────────────┘   │ │
│  └────────────────────────────────────────┼──────────────────────────────┘ │
│                                            │                                │
│         ┌──────────────────────────────────▼──────────────────────────┐    │
│         │              OBJECT STORAGE SERVICE                         │    │
│         │         (S3 / Cloud Storage / Blob Storage)                 │    │
│         │                                                              │    │
│         │  Features:                                                   │    │
│         │  • Versioning enabled                                        │    │
│         │  • Server-side encryption (AES-256)                          │    │
│         │  • Public access blocked                                     │    │
│         │  • Lifecycle policies for cost optimization                  │    │
│         │  • Access logging enabled                                    │    │
│         │                                                              │    │
│         │  Storage Classes:                                            │    │
│         │  • Day 0-30: Standard (hot)                                  │    │
│         │  • Day 30-90: Infrequent Access                             │    │
│         │  • Day 90-180: Archive (cold)                               │    │
│         │  • Day 180+: Deep Archive                                    │    │
│         └──────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    SUPPORTING SERVICES                                  │ │
│  │                                                                          │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────────┐   │ │
│  │  │ Secret Manager  │  │ Identity & Access│  │  Logging Service    │   │ │
│  │  │                 │  │   Management     │  │                     │   │ │
│  │  │ Stores:         │  │                  │  │ Centralized logs    │   │ │
│  │  │ • SFTP username │  │ Grants function  │  │ from all components │   │ │
│  │  │ • SFTP password │  │ permissions to:  │  │                     │   │ │
│  │  │ • SFTP host     │  │ • Storage        │  │ Retention: 7 days   │   │ │
│  │  │ • SFTP port     │  │ • Secrets        │  │                     │   │ │
│  │  └─────────────────┘  └──────────────────┘  └─────────────────────┘   │ │
│  │                                                                          │ │
│  │  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────────┐   │ │
│  │  │ Monitoring      │  │   Scheduler      │  │  Alerting           │   │ │
│  │  │                 │  │                  │  │                     │   │ │
│  │  │ Tracks:         │  │ Triggers function│  │ Alerts on:          │   │ │
│  │  │ • Invocations   │  │ on schedule      │  │ • Errors            │   │ │
│  │  │ • Errors        │  │ (e.g., hourly)   │  │ • Timeouts          │   │ │
│  │  │ • Duration      │  │                  │  │ • Cost anomalies    │   │ │
│  │  │ • Costs         │  │ Cron: 0 * * * *  │  │                     │   │ │
│  │  └─────────────────┘  └──────────────────┘  └─────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     │ SSH (Port 22)
                                     │ Over Internet
                                     │
                          ┌──────────▼────────────┐
                          │   LEGACY SFTP SERVER   │
                          │                        │
                          │   Location: On-Premise │
                          │   Protocol: SSH/SFTP   │
                          │   Port: 22             │
                          │   Auth: Password/Key   │
                          └────────────────────────┘
```

---

## Component Breakdown

### 1. Virtual Private Network Layer
**Purpose**: Provide isolated network environment for cloud resources

**Components**:
- Virtual network with private IP address space (10.0.0.0/16)
- Multiple private subnets across availability zones/regions
- Route tables for traffic control
- Network ACLs for additional security

**Cloud Equivalents**:
- **AWS**: VPC (Virtual Private Cloud)
- **GCP**: VPC (Virtual Private Cloud)
- **Azure**: VNet (Virtual Network)

---

### 2. Serverless Compute Layer
**Purpose**: Execute file transfer logic without managing servers

**Components**:
- Event-driven function execution
- Automatic scaling (0 to N instances)
- VPC integration for network isolation
- Environment variable configuration
- IAM role/service account for permissions

**Cloud Equivalents**:
- **AWS**: Lambda
- **GCP**: Cloud Functions (2nd generation)
- **Azure**: Azure Functions

**Key Features**:
- Runtime: Python 3.11
- Memory: 512 MB
- Timeout: 300 seconds (5 minutes)
- Concurrent executions: Up to 1000
- Cold start: ~1-2 seconds

---

### 3. Private Storage Connectivity Layer
**Purpose**: Provide private, secure connection from compute to object storage

**Components**:
- Private endpoint for storage service
- Integration with VPC route tables
- Endpoint policies for least-privilege access
- No data traverses public internet

**Cloud Equivalents**:
- **AWS**: VPC Gateway Endpoint (for S3) - **FREE**
- **GCP**: Private Google Access / Private Service Connect
- **Azure**: Private Endpoint (~$7.20/month)

**Benefits**:
- Reduced security risk (no internet exposure)
- Lower latency
- No NAT Gateway costs (saves $32-48/month)
- Improved compliance posture

---

### 4. Object Storage Layer
**Purpose**: Durable, scalable storage for transferred files

**Components**:
- Bucket/container for file storage
- Versioning for data protection
- Server-side encryption (AES-256)
- Lifecycle policies for cost optimization
- Access logging and monitoring

**Cloud Equivalents**:
- **AWS**: S3 (Simple Storage Service)
- **GCP**: Cloud Storage
- **Azure**: Blob Storage

**Storage Tiers** (Universal):
1. **Hot/Standard** (0-30 days): Frequent access
2. **Cool/Infrequent Access** (30-90 days): Less frequent access
3. **Archive** (90-180 days): Rare access, lower cost
4. **Cold Archive** (180+ days): Long-term retention

---

### 5. Security Layer

#### 5.1 Network Security
**Purpose**: Control ingress and egress traffic

**Components**:
- Stateful firewall rules
- Protocol and port restrictions
- Source/destination filtering

**Cloud Equivalents**:
- **AWS**: Security Groups
- **GCP**: VPC Firewall Rules
- **Azure**: Network Security Groups (NSG)

**Rules**:
- **Egress HTTPS (443)**: Allow to object storage via private endpoint
- **Egress SSH (22)**: Allow to SFTP server
- **Ingress**: None required (private subnet)

#### 5.2 Identity & Access Management
**Purpose**: Grant minimal required permissions

**Components**:
- Service identity for function
- Policies defining allowed actions
- Resource-based access controls

**Cloud Equivalents**:
- **AWS**: IAM Roles + Policies
- **GCP**: Service Accounts + IAM Bindings
- **Azure**: Managed Identities + Role Assignments

**Permissions** (Least Privilege):
- `storage:PutObject` - Upload files to storage
- `storage:ListBucket` - List bucket contents
- `secrets:GetSecret` - Retrieve SFTP credentials
- `logs:CreateLogStream` - Write logs
- `logs:PutLogEvents` - Send log events
- `network:CreateNetworkInterface` - VPC integration

#### 5.3 Secret Management
**Purpose**: Securely store and retrieve sensitive credentials

**Components**:
- Encrypted secret storage
- Automatic rotation support
- Access auditing
- Version management

**Cloud Equivalents**:
- **AWS**: Secrets Manager ($0.40/secret/month)
- **GCP**: Secret Manager ($0.06/secret/month)
- **Azure**: Key Vault ($0.03/secret/month)

**Stored Secrets**:
```json
{
  "sftp_username": "user123",
  "sftp_password": "encrypted_password",
  "sftp_host": "sftp.example.com",
  "sftp_port": 22
}
```

---

### 6. Observability Layer

#### 6.1 Logging
**Purpose**: Centralized log collection and analysis

**Components**:
- Structured logging (JSON format)
- Log retention policies
- Search and filtering capabilities
- Export to long-term storage

**Cloud Equivalents**:
- **AWS**: CloudWatch Logs
- **GCP**: Cloud Logging (Stackdriver)
- **Azure**: Application Insights / Log Analytics

**Log Retention**: 7 days (configurable)

#### 6.2 Monitoring
**Purpose**: Track performance and resource utilization

**Components**:
- Function invocation count
- Error rate tracking
- Duration/latency metrics
- Memory and CPU utilization
- Cost tracking

**Cloud Equivalents**:
- **AWS**: CloudWatch Metrics
- **GCP**: Cloud Monitoring
- **Azure**: Azure Monitor

**Key Metrics**:
- Invocations per minute
- Error rate (%)
- Average duration (ms)
- P50, P95, P99 latency
- Concurrent executions
- Throttles

#### 6.3 Alerting
**Purpose**: Notify on issues and anomalies

**Alert Conditions**:
- Error rate > 5%
- Function duration > 4 minutes
- SFTP connection failures
- Storage write failures
- Cost exceeds threshold

---

### 7. Automation Layer

#### Scheduling
**Purpose**: Trigger file transfer on recurring schedule

**Components**:
- Cron-based scheduling
- Event-driven triggers
- Retry on failure

**Cloud Equivalents**:
- **AWS**: EventBridge (CloudWatch Events)
- **GCP**: Cloud Scheduler
- **Azure**: Logic Apps / Timer Trigger

**Example Schedules**:
- Every hour: `0 * * * *`
- Every 6 hours: `0 */6 * * *`
- Daily at 2 AM: `0 2 * * *`
- Business hours only: `0 9-17 * * 1-5`

---

## Data Flow

### Successful Transfer Flow

```
1. Scheduler triggers function
   ↓
2. Function starts in VPC private subnet
   ↓
3. Function retrieves SFTP credentials from Secret Manager
   ↓
4. Function connects to SFTP server over internet (port 22)
   ↓
5. Function downloads file(s) from SFTP server
   ↓
6. Function uploads file(s) to Object Storage via Private Endpoint
   ↓
7. Object Storage encrypts and stores file(s)
   ↓
8. Function logs success to Logging Service
   ↓
9. Function execution completes
   ↓
10. Monitoring records invocation metrics
```

### Error Handling Flow

```
1. Function encounters error (SFTP connection, storage write, etc.)
   ↓
2. Function logs detailed error to Logging Service
   ↓
3. Function implements retry logic (exponential backoff)
   ↓
4. If retry succeeds → Normal completion
   ↓
5. If retry fails → Function fails with error
   ↓
6. Monitoring detects error threshold breach
   ↓
7. Alerting sends notification to operators
   ↓
8. Operators investigate using logs and metrics
```

---

## Security Architecture

### Defense in Depth

1. **Network Layer**
   - Private subnets (no direct internet access)
   - Network ACLs
   - Security groups/firewall rules
   - Private endpoints (no data over internet for storage)

2. **Application Layer**
   - Function runs with minimal IAM permissions
   - No hardcoded credentials
   - Input validation and sanitization
   - Secure SFTP connection (SSH protocol)

3. **Data Layer**
   - Encryption in transit (TLS/HTTPS, SSH)
   - Encryption at rest (AES-256)
   - Versioning for data protection
   - Public access blocked on storage

4. **Identity Layer**
   - Service accounts/managed identities (no static credentials)
   - Least privilege access policies
   - Secret rotation support
   - Audit logging of all access

5. **Monitoring Layer**
   - All actions logged
   - Anomaly detection
   - Security alerts
   - Compliance reporting

---

## Cost Optimization

### Architecture Decisions for Cost Efficiency

1. **Serverless Compute**
   - Pay only for execution time (no idle costs)
   - Automatic scaling (no over-provisioning)
   - No server management overhead

2. **Private Endpoints vs NAT Gateway**
   - VPC Gateway Endpoint (AWS): **$0.00** vs NAT Gateway: **$32.40/month**
   - Savings: **100%** for storage traffic

3. **Storage Lifecycle**
   - Automatic tiering to cheaper storage classes
   - Day 30: Move to Infrequent Access (46% savings)
   - Day 90: Move to Archive (83% savings)
   - Day 180: Move to Deep Archive (96% savings)

4. **Logging Retention**
   - 7-day retention (vs 30+ days)
   - Export to cheaper storage for long-term retention

5. **Right-Sizing**
   - 512 MB memory (not over-provisioned)
   - 5-minute timeout (not excessive)
   - Optimized function package size

### Monthly Cost Estimate (1000 transfers, 100MB avg file)

| Component | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| Compute | $0.25 | $0.40 | $0.20 |
| Storage (100GB) | $2.30 | $2.00 | $2.05 |
| Network (Private) | $0.00 | $0.00 | $7.20 |
| Secrets | $0.40 | $0.06 | $0.03 |
| Logging | $0.50 | $0.00 | $2.30 |
| **TOTAL** | **$3.45** | **$2.46** | **$11.78** |

---

## High Availability & Disaster Recovery

### High Availability Features

1. **Multi-AZ/Multi-Zone Deployment**
   - Function deployed across multiple availability zones
   - Automatic failover between zones
   - Storage replicated across zones

2. **Automatic Scaling**
   - Functions scale from 0 to 1000+ concurrent executions
   - No single point of failure
   - Load distributed automatically

3. **Retry Logic**
   - Automatic retries on transient failures
   - Exponential backoff strategy
   - Dead letter queue for persistent failures

### Disaster Recovery

1. **Backup Strategy**
   - Storage versioning enabled (recover from accidental deletion)
   - Cross-region replication available
   - Point-in-time recovery

2. **Recovery Time Objective (RTO)**
   - Serverless: < 5 minutes (no infrastructure provisioning needed)
   - Storage: Immediate (highly available by default)

3. **Recovery Point Objective (RPO)**
   - Near-zero (files transferred immediately)
   - Versioning provides point-in-time recovery

---

## Compliance & Governance

### Compliance Features

1. **Data Encryption**
   - At rest: AES-256 encryption
   - In transit: TLS 1.2+ (HTTPS), SSH (SFTP)

2. **Access Control**
   - Principle of least privilege
   - Role-based access control (RBAC)
   - Audit logs for all access

3. **Data Residency**
   - Data stored in specified region
   - No cross-border data transfer (unless configured)

4. **Audit Trail**
   - All operations logged
   - Immutable log storage
   - Compliance reporting available

### Regulatory Alignment

- **GDPR**: Data encryption, access controls, audit logs
- **HIPAA**: Encryption, access controls, audit logs (with BAA)
- **SOC 2**: Security controls, monitoring, incident response
- **PCI DSS**: Network isolation, encryption, access controls

---

## Performance Characteristics

### Latency

- **Cold Start**: 1-2 seconds (Python runtime)
- **Warm Invocation**: 50-200ms (excluding SFTP transfer)
- **SFTP Download**: Variable (depends on file size and network)
- **Storage Upload**: 10-100ms per MB (via private endpoint)

### Throughput

- **Concurrent Executions**: 1000+ (configurable)
- **Files per Minute**: 100-1000 (depending on size)
- **Data Transfer Rate**: 100-500 Mbps (via private endpoint)

### Scalability

- **Horizontal Scaling**: Automatic (0 to 1000+ instances)
- **Storage Capacity**: Virtually unlimited
- **Request Rate**: 1000s of requests per second

---

## Operational Excellence

### Deployment

1. **Infrastructure as Code**
   - Terraform/CloudFormation/Deployment Manager
   - Version controlled
   - Automated deployments
   - Environment parity (dev/staging/prod)

2. **CI/CD Integration**
   - Automated testing
   - Automated packaging
   - Automated deployment
   - Rollback capabilities

### Monitoring & Alerting

1. **Proactive Monitoring**
   - Real-time dashboards
   - Anomaly detection
   - Trend analysis
   - Capacity planning

2. **Alert Management**
   - Multi-channel notifications (email, SMS, Slack)
   - Escalation policies
   - On-call rotation
   - Runbook automation

### Troubleshooting

1. **Log Analysis**
   - Structured logs (JSON)
   - Correlation IDs
   - Search and filtering
   - Log aggregation

2. **Distributed Tracing**
   - End-to-end request tracing
   - Performance bottleneck identification
   - Dependency mapping

---

## Future Enhancements

### Potential Additions

1. **File Processing**
   - Automatic file validation
   - Data transformation
   - Format conversion
   - Virus scanning

2. **Advanced Routing**
   - Multi-destination support
   - Content-based routing
   - File splitting/merging

3. **Enhanced Security**
   - Key-based SFTP authentication
   - Customer-managed encryption keys
   - Data loss prevention (DLP)
   - Anomaly detection

4. **Performance Optimization**
   - Parallel file transfers
   - Compression
   - Caching
   - Streaming uploads

---

## Summary

This universal architecture provides:

✅ **Security**: VPC isolation, private endpoints, encryption, least privilege
✅ **Cost Efficiency**: Serverless, private endpoints, lifecycle policies
✅ **Scalability**: Auto-scaling, unlimited storage, high throughput
✅ **Reliability**: Multi-AZ, automatic retries, versioning
✅ **Observability**: Comprehensive logging, monitoring, alerting
✅ **Compliance**: Encryption, audit trails, access controls
✅ **Portability**: Cloud-agnostic design, easy migration

The architecture is production-ready and can be deployed on AWS, GCP, or Azure with minimal modifications using the component mappings provided in this documentation.
