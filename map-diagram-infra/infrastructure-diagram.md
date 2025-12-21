# Universal Infrastructure Diagram

## High-Level Architecture (Cloud-Agnostic)

```mermaid
graph TB
    subgraph "External Systems"
        SFTP[Legacy SFTP Server<br/>Port 22/SSH]
    end

    subgraph "Cloud Provider Platform"
        subgraph "Virtual Private Network"
            subgraph "Private Subnet Zone 1"
                COMPUTE1[Serverless Function<br/>Instance 1]
            end
            
            subgraph "Private Subnet Zone 2"
                COMPUTE2[Serverless Function<br/>Instance 2]
            end
            
            SG[Security Group/<br/>Firewall Rules]
            
            ENDPOINT[Private Service Endpoint<br/>Gateway to Object Storage<br/>Zero-Cost]
        end
        
        STORAGE[Object Storage Bucket<br/>Encrypted at Rest<br/>Versioning Enabled]
        
        SECRETS[Secrets Manager<br/>Encrypted Credentials]
        
        IAM[Identity & Access Management<br/>Service Principal/Roles]
        
        LOGS[Centralized Logging<br/>Service]
        
        METRICS[Monitoring & Metrics<br/>Service]
        
        SCHEDULER[Event Scheduler<br/>Cron-based Triggers]
    end

    SFTP -->|SSH/SFTP Protocol<br/>Port 22| SG
    SG -->|Allow Egress| COMPUTE1
    SG -->|Allow Egress| COMPUTE2
    
    COMPUTE1 -->|Private Connection| ENDPOINT
    COMPUTE2 -->|Private Connection| ENDPOINT
    
    ENDPOINT -->|No Internet<br/>No NAT Required| STORAGE
    
    COMPUTE1 -.->|Read Credentials| SECRETS
    COMPUTE2 -.->|Read Credentials| SECRETS
    
    IAM -->|Authorize| COMPUTE1
    IAM -->|Authorize| COMPUTE2
    IAM -->|Authorize| STORAGE
    IAM -->|Authorize| SECRETS
    
    COMPUTE1 -->|Write Logs| LOGS
    COMPUTE2 -->|Write Logs| LOGS
    
    COMPUTE1 -->|Emit Metrics| METRICS
    COMPUTE2 -->|Emit Metrics| METRICS
    
    SCHEDULER -->|Trigger| COMPUTE1
    SCHEDULER -->|Trigger| COMPUTE2
    
    style COMPUTE1 fill:#4CAF50
    style COMPUTE2 fill:#4CAF50
    style ENDPOINT fill:#FF9800
    style STORAGE fill:#2196F3
    style SECRETS fill:#F44336
    style IAM fill:#9C27B0
```

## Detailed Component Diagram

```mermaid
graph TB
    subgraph "Internet/External Network"
        EXT[External SFTP Server<br/>Legacy System]
    end

    subgraph "Cloud Virtual Network - 10.0.0.0/16"
        subgraph "Availability Zone 1"
            SUBNET1[Private Subnet 1<br/>10.0.1.0/24<br/>No Internet Gateway]
            LAMBDA1[Function Instance 1<br/>Runtime: Python 3.11<br/>Memory: 512 MB<br/>Timeout: 300s]
        end
        
        subgraph "Availability Zone 2"
            SUBNET2[Private Subnet 2<br/>10.0.2.0/24<br/>No Internet Gateway]
            LAMBDA2[Function Instance 2<br/>Runtime: Python 3.11<br/>Memory: 512 MB<br/>Timeout: 300s]
        end
        
        RT[Route Table<br/>Private Routes Only]
        
        NACL[Network ACL<br/>Stateless Firewall]
        
        SG_LAMBDA[Security Group<br/>Egress: 443 HTTPS<br/>Egress: 22 SSH]
        
        VPC_ENDPOINT[VPC Gateway Endpoint<br/>Service: Object Storage<br/>Type: Gateway<br/>Cost: FREE]
        
        ENI1[Elastic Network Interface 1<br/>Private IP: 10.0.1.x]
        ENI2[Elastic Network Interface 2<br/>Private IP: 10.0.2.x]
    end
    
    subgraph "Managed Services - Control Plane"
        S3[Object Storage Service<br/>Bucket: Encrypted<br/>SSE-AES256/SSE-KMS<br/>Versioning: Enabled<br/>Public Access: Blocked]
        
        SM[Secrets Management Service<br/>Encryption: KMS<br/>Rotation: Optional<br/>Recovery: 7 days]
        
        CW_LOGS[Centralized Logging<br/>Retention: 7 days<br/>Encryption: Enabled]
        
        CW_METRICS[Monitoring Service<br/>Metrics: Invocations, Duration, Errors<br/>Alarms: Configurable]
        
        EB[Event Scheduler<br/>Schedule: Configurable<br/>Cron Expression Support]
        
        KMS[Key Management Service<br/>Customer Managed Keys<br/>Automatic Rotation]
    end
    
    subgraph "Identity & Access"
        ROLE[Service Role<br/>Type: Execution Role]
        
        POLICY1[Policy: Object Storage Access<br/>Actions: PutObject, GetObject<br/>Principle: Least Privilege]
        
        POLICY2[Policy: Logging Access<br/>Actions: CreateLogStream, PutLogEvents]
        
        POLICY3[Policy: VPC Access<br/>Actions: ENI Management]
        
        POLICY4[Policy: Secrets Access<br/>Actions: GetSecretValue]
    end
    
    subgraph "Storage Lifecycle"
        STANDARD[Standard Storage<br/>Day 0-29<br/>High Availability]
        
        IA[Infrequent Access<br/>Day 30-89<br/>46% Cost Savings]
        
        GLACIER[Archive Storage<br/>Day 90-179<br/>83% Cost Savings]
        
        DEEP[Deep Archive<br/>Day 180+<br/>96% Cost Savings]
    end

    EXT -->|SSH/SFTP| SG_LAMBDA
    
    SUBNET1 --> RT
    SUBNET2 --> RT
    RT --> VPC_ENDPOINT
    
    LAMBDA1 --> ENI1
    LAMBDA2 --> ENI2
    
    ENI1 --> SUBNET1
    ENI2 --> SUBNET2
    
    SG_LAMBDA --> LAMBDA1
    SG_LAMBDA --> LAMBDA2
    
    LAMBDA1 -->|HTTPS via Endpoint| VPC_ENDPOINT
    LAMBDA2 -->|HTTPS via Endpoint| VPC_ENDPOINT
    
    VPC_ENDPOINT -->|Private Connection| S3
    
    LAMBDA1 -.->|Retrieve Credentials| SM
    LAMBDA2 -.->|Retrieve Credentials| SM
    
    LAMBDA1 -->|Write Logs| CW_LOGS
    LAMBDA2 -->|Write Logs| CW_LOGS
    
    LAMBDA1 -->|Metrics| CW_METRICS
    LAMBDA2 -->|Metrics| CW_METRICS
    
    EB -->|Invoke| LAMBDA1
    EB -->|Invoke| LAMBDA2
    
    ROLE --> POLICY1
    ROLE --> POLICY2
    ROLE --> POLICY3
    ROLE --> POLICY4
    
    ROLE -.->|Assume| LAMBDA1
    ROLE -.->|Assume| LAMBDA2
    
    SM --> KMS
    S3 --> KMS
    CW_LOGS --> KMS
    
    S3 --> STANDARD
    STANDARD -->|After 30 days| IA
    IA -->|After 90 days| GLACIER
    GLACIER -->|After 180 days| DEEP
    
    style LAMBDA1 fill:#4CAF50
    style LAMBDA2 fill:#4CAF50
    style VPC_ENDPOINT fill:#FF9800
    style S3 fill:#2196F3
    style SM fill:#F44336
    style ROLE fill:#9C27B0
    style KMS fill:#E91E63
```

## Network Flow Diagram

```mermaid
sequenceDiagram
    participant SFTP as SFTP Server
    participant Lambda as Serverless Function
    participant Secrets as Secrets Manager
    participant VPC_EP as VPC Gateway Endpoint
    participant S3 as Object Storage
    participant Logs as Logging Service
    
    Note over Lambda: Function Triggered by Event
    
    Lambda->>Secrets: Retrieve SFTP Credentials
    Secrets-->>Lambda: Return Encrypted Credentials
    
    Lambda->>SFTP: Connect via SSH (Port 22)
    SFTP-->>Lambda: Establish Connection
    
    Lambda->>SFTP: List Files in Remote Directory
    SFTP-->>Lambda: Return File List
    
    loop For Each File
        Lambda->>SFTP: Download File
        SFTP-->>Lambda: Stream File Data
        
        Lambda->>VPC_EP: Upload to Storage (HTTPS)
        VPC_EP->>S3: Forward Request (Private)
        S3-->>VPC_EP: Acknowledge Upload
        VPC_EP-->>Lambda: Success Response
        
        Lambda->>Logs: Write Transfer Log
    end
    
    Lambda->>SFTP: Close Connection
    Lambda->>Logs: Write Completion Status
    
    Note over Lambda: Function Execution Complete
```

## Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        subgraph "Network Security"
            VPC[Private Virtual Network<br/>Isolated Network Space]
            SG[Security Groups<br/>Stateful Firewall<br/>Least Privilege Rules]
            NACL[Network ACLs<br/>Stateless Firewall]
            NO_IGW[No Internet Gateway<br/>No Public IPs]
            NO_NAT[No NAT Gateway<br/>Cost Optimization]
        end
        
        subgraph "Access Control"
            IAM_ROLE[Service Roles<br/>Principle of Least Privilege]
            IAM_POLICY[Fine-Grained Policies<br/>Resource-Level Permissions]
            ENDPOINT_POLICY[Endpoint Policy<br/>Restrict Service Access]
        end
        
        subgraph "Data Encryption"
            TRANSIT[Encryption in Transit<br/>TLS/HTTPS for Storage<br/>SSH for SFTP]
            REST[Encryption at Rest<br/>Storage: AES-256<br/>Secrets: KMS]
            KEY_MGMT[Key Management<br/>Customer Managed Keys<br/>Automatic Rotation]
        end
        
        subgraph "Compliance & Monitoring"
            LOGGING[Comprehensive Logging<br/>All API Calls Logged]
            MONITORING[Real-time Monitoring<br/>Anomaly Detection]
            VERSIONING[Object Versioning<br/>Audit Trail]
            PUBLIC_BLOCK[Public Access Blocked<br/>All Public Access Denied]
        end
    end
    
    style VPC fill:#4CAF50
    style IAM_ROLE fill:#9C27B0
    style TRANSIT fill:#2196F3
    style LOGGING fill:#FF9800
```

## Cost Optimization Architecture

```mermaid
graph LR
    subgraph "Cost Optimization Strategy"
        subgraph "Compute Costs"
            SERVERLESS[Serverless Model<br/>Pay Per Execution<br/>No Idle Costs<br/>Automatic Scaling]
        end
        
        subgraph "Network Costs"
            GATEWAY_EP[Gateway Endpoint<br/>FREE Service<br/>No Hourly Charges<br/>No Data Transfer Fees]
            NO_NAT_COST[No NAT Gateway<br/>Save $32+/month per AZ]
        end
        
        subgraph "Storage Costs"
            LIFECYCLE[Lifecycle Policies<br/>Automatic Tiering]
            TIER1[Standard: Day 0-29]
            TIER2[IA: Day 30-89<br/>46% Savings]
            TIER3[Archive: Day 90-179<br/>83% Savings]
            TIER4[Deep Archive: Day 180+<br/>96% Savings]
        end
        
        subgraph "Operational Costs"
            LOG_RETENTION[Log Retention: 7 days<br/>Minimize Storage Costs]
            BUCKET_KEYS[Bucket Keys Enabled<br/>99% KMS Cost Reduction]
        end
    end
    
    LIFECYCLE --> TIER1
    TIER1 --> TIER2
    TIER2 --> TIER3
    TIER3 --> TIER4
    
    style GATEWAY_EP fill:#4CAF50
    style NO_NAT_COST fill:#4CAF50
    style LIFECYCLE fill:#2196F3
```

## Multi-Region Architecture (Optional)

```mermaid
graph TB
    subgraph "Region 1 - Primary"
        VPC1[Virtual Network 1]
        COMPUTE1[Serverless Functions]
        STORAGE1[Object Storage]
        ENDPOINT1[Gateway Endpoint]
    end
    
    subgraph "Region 2 - Secondary/DR"
        VPC2[Virtual Network 2]
        COMPUTE2[Serverless Functions]
        STORAGE2[Object Storage<br/>Replication Target]
        ENDPOINT2[Gateway Endpoint]
    end
    
    STORAGE1 -.->|Cross-Region Replication| STORAGE2
    
    subgraph "Global Services"
        DNS[DNS Service<br/>Health Checks<br/>Failover Routing]
        MONITOR[Global Monitoring<br/>Multi-Region Dashboard]
    end
    
    DNS --> COMPUTE1
    DNS -.->|Failover| COMPUTE2
    
    MONITOR --> COMPUTE1
    MONITOR --> COMPUTE2
    
    style STORAGE1 fill:#2196F3
    style STORAGE2 fill:#2196F3
```

## Deployment Architecture Pattern

```mermaid
graph TB
    subgraph "Development"
        DEV_VPC[Dev VPC<br/>10.0.0.0/16]
        DEV_FUNC[Dev Functions<br/>Lower Memory/Timeout]
        DEV_STORAGE[Dev Storage<br/>No Lifecycle]
    end
    
    subgraph "Staging"
        STG_VPC[Staging VPC<br/>10.1.0.0/16]
        STG_FUNC[Staging Functions<br/>Prod-like Config]
        STG_STORAGE[Staging Storage<br/>Simplified Lifecycle]
    end
    
    subgraph "Production"
        PROD_VPC[Prod VPC<br/>10.2.0.0/16]
        PROD_FUNC[Prod Functions<br/>Optimized Config<br/>Multi-AZ]
        PROD_STORAGE[Prod Storage<br/>Full Lifecycle<br/>Replication]
    end
    
    DEV_VPC --> STG_VPC
    STG_VPC --> PROD_VPC
    
    style PROD_VPC fill:#4CAF50
    style PROD_FUNC fill:#4CAF50
    style PROD_STORAGE fill:#2196F3
```

## Legend

### Colors
- 🟢 **Green**: Compute/Function Components
- 🟠 **Orange**: Network Endpoints
- 🔵 **Blue**: Storage Services
- 🔴 **Red**: Secrets/Sensitive Data
- 🟣 **Purple**: Identity & Access Management
- 🟤 **Pink**: Encryption Services

### Line Types
- **Solid Line** (→): Direct data flow or connection
- **Dashed Line** (-.->): Authentication/Authorization flow
- **Bold Line**: Primary data path

### Component Types
- **Rectangle**: Standard component
- **Rounded Rectangle**: Managed service
- **Cylinder**: Storage service
- **Diamond**: Decision point

## Notes

1. **All diagrams use cloud-agnostic terminology** that maps to specific services in AWS, GCP, or Azure
2. **Security is implemented at every layer** from network to application
3. **Cost optimization is a first-class concern** with multiple strategies employed
4. **High availability** is achieved through multi-AZ deployment
5. **Scalability** is inherent in the serverless architecture
6. **Monitoring and observability** are built-in from day one

For service-specific mappings to AWS, GCP, and Azure, see `cloud-service-mapping.md`.
