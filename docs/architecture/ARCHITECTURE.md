# Architecture Documentation

## System Architecture

### Overview
This solution implements a secure file transfer system that moves files from a legacy SFTP server to Amazon S3 using AWS Lambda in a VPC. The design eliminates the need for internet gateways or NAT gateways by using VPC Gateway Endpoints for S3 access.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS Cloud                                │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                VPC (10.0.0.0/16)                          │  │
│  │                                                            │  │
│  │  ┌──────────────────┐      ┌──────────────────┐         │  │
│  │  │ Private Subnet 1 │      │ Private Subnet 2 │         │  │
│  │  │  10.0.1.0/24     │      │  10.0.2.0/24     │         │  │
│  │  │                  │      │                  │         │  │
│  │  │  ┌────────────┐ │      │                  │         │  │
│  │  │  │   Lambda   │ │      │                  │         │  │
│  │  │  │  Function  │ │      │                  │         │  │
│  │  │  └────┬───────┘ │      │                  │         │  │
│  │  │       │         │      │                  │         │  │
│  │  └───────┼─────────┘      └──────────────────┘         │  │
│  │          │                                               │  │
│  │          │                                               │  │
│  │  ┌───────▼──────────────────────────────────────────┐  │  │
│  │  │         Private Route Table                      │  │  │
│  │  │                                                   │  │  │
│  │  │  Routes:                                          │  │  │
│  │  │  - 10.0.0.0/16 → local                           │  │  │
│  │  │  - S3 prefix → vpce-xxxxx (Gateway Endpoint)    │  │  │
│  │  └───────────────────┬───────────────────────────────┘  │  │
│  │                      │                                   │  │
│  │              ┌───────▼──────────┐                       │  │
│  │              │  S3 Gateway      │                       │  │
│  │              │   Endpoint       │                       │  │
│  │              │  (vpce-xxxxx)    │                       │  │
│  │              └───────┬──────────┘                       │  │
│  └──────────────────────┼───────────────────────────────────┘  │
│                         │                                       │
│                 ┌───────▼──────────┐                           │
│                 │                   │                           │
│                 │    Amazon S3      │                           │
│                 │     Bucket        │                           │
│                 │  (Encrypted)      │                           │
│                 │                   │                           │
│                 └───────────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

         │
         │ Internet (SFTP)
         │
┌────────▼──────────┐
│                   │
│  Legacy SFTP      │
│    Server         │
│                   │
└───────────────────┘
```

### Components

#### 1. VPC (Virtual Private Cloud)
- **CIDR**: 10.0.0.0/16
- **Subnets**: Two private subnets in different availability zones
- **Purpose**: Provides network isolation for Lambda function

#### 2. Private Subnets
- **Subnet 1**: 10.0.1.0/24 (AZ-a)
- **Subnet 2**: 10.0.2.0/24 (AZ-b)
- **Purpose**: Host Lambda ENIs with no direct internet access

#### 3. Lambda Function
- **Runtime**: Python 3.11
- **Memory**: 512 MB (configurable)
- **Timeout**: 300 seconds (5 minutes)
- **Purpose**: Execute file transfer logic

#### 4. S3 Gateway Endpoint
- **Type**: Gateway Endpoint
- **Cost**: Free (no data processing charges)
- **Purpose**: Enable private S3 access without NAT/IGW

#### 5. S3 Bucket
- **Encryption**: AES-256 (SSE-S3) or KMS
- **Versioning**: Enabled
- **Purpose**: Store transferred files securely

#### 6. Security Groups
- **Lambda SG**: Allows outbound HTTPS (443) and SFTP (22)
- **Purpose**: Control Lambda network traffic

#### 7. IAM Roles
- **Lambda Execution Role**: Permissions for S3, VPC, CloudWatch, Secrets Manager
- **Purpose**: Grant least-privilege access

### Data Flow

1. **Event Trigger**: Lambda function is invoked (manually, scheduled, or event-driven)
2. **Credential Retrieval**: Lambda retrieves SFTP credentials from Secrets Manager
3. **SFTP Connection**: Lambda connects to legacy SFTP server via internet
4. **File Download**: File is downloaded to Lambda's /tmp directory
5. **File Validation**: File size and integrity are validated
6. **S3 Upload**: File is uploaded to S3 via Gateway Endpoint (private network)
7. **Cleanup**: Temporary files are deleted
8. **Response**: Success/failure status is returned

### Security Features

1. **No Internet Gateway**: Lambda in private subnet, no direct internet access for S3
2. **VPC Gateway Endpoint**: Private connection to S3
3. **Encryption in Transit**: HTTPS/TLS for all communications
4. **Encryption at Rest**: S3 server-side encryption
5. **IAM Least Privilege**: Minimal required permissions
6. **Secrets Manager**: Secure credential storage
7. **VPC Flow Logs**: Network traffic monitoring (optional)
8. **CloudWatch Logs**: Audit trail of all operations

### High Availability

- **Multi-AZ Deployment**: Lambda can use subnets in multiple AZs
- **S3 Durability**: 99.999999999% (11 nines)
- **Automatic Failover**: Lambda automatically handles failures
- **Retry Logic**: Built-in retry with exponential backoff

### Cost Optimization

1. **No NAT Gateway**: Save ~$32/month per AZ
2. **No Data Processing Charges**: Gateway endpoints are free
3. **S3 Lifecycle Policies**: Automatically tier old data to cheaper storage
4. **Lambda Ephemeral Storage**: Use /tmp instead of EFS
5. **CloudWatch Log Retention**: Short retention for dev (7 days)

### Scalability

- **Lambda Concurrency**: Up to 1000 concurrent executions (default)
- **S3 Performance**: 3,500 PUT/POST/DELETE and 5,500 GET requests per second per prefix
- **No VPC Limits**: Gateway endpoints scale automatically
- **Stateless Design**: Each invocation is independent

### Monitoring & Observability

1. **CloudWatch Metrics**
   - Lambda: Duration, Errors, Throttles, Invocations
   - S3: Requests, Bytes uploaded
   
2. **CloudWatch Logs**
   - Lambda execution logs
   - VPC Flow Logs (optional)
   - S3 access logs (optional)

3. **CloudWatch Alarms**
   - Lambda errors > 0
   - Lambda throttles > 0
   - Lambda duration > threshold

4. **AWS X-Ray** (optional)
   - Distributed tracing
   - Performance analysis
   - Bottleneck identification

### Compliance & Governance

- **DEA-C01 Alignment**: Follows AWS Data Engineer Associate best practices
- **Well-Architected Framework**: Implements all five pillars
- **Tagging Strategy**: Environment, Project, ManagedBy tags
- **State Management**: Terraform state in S3 with DynamoDB locking

### Disaster Recovery

- **RTO**: < 1 hour (redeploy with Terraform)
- **RPO**: < 1 minute (S3 versioning enabled)
- **Backup Strategy**: S3 versioning + optional cross-region replication
- **Recovery Procedure**: Documented in runbooks

### Future Enhancements

1. **Dead Letter Queue**: Capture failed events
2. **Step Functions**: Orchestrate complex workflows
3. **EventBridge**: Event-driven invocation
4. **S3 Event Notifications**: Trigger downstream processing
5. **AWS Transfer Family**: Replace legacy SFTP server
6. **Container Support**: Migrate to Lambda containers for larger packages
