# Cloud Provider Component Mapping Table

## Comprehensive Resource Equivalency Matrix

This document provides a detailed mapping of every infrastructure component across AWS, Google Cloud Platform (GCP), and Microsoft Azure.

---

## Core Infrastructure Components

### Compute Services

| **Service Category** | **AWS** | **GCP** | **Azure** | **Open Source Alternative** |
|---------------------|---------|---------|-----------|---------------------------|
| **Serverless Functions** | AWS Lambda | Cloud Functions (1st/2nd Gen) | Azure Functions | OpenFaaS, Knative, Fn Project |
| **Container Orchestration** | Amazon ECS | Google Kubernetes Engine (GKE) | Azure Kubernetes Service (AKS) | Kubernetes, Docker Swarm |
| **Virtual Machines** | Amazon EC2 | Compute Engine | Azure Virtual Machines | KVM, Proxmox, OpenStack |
| **Batch Processing** | AWS Batch | Cloud Tasks, Dataflow | Azure Batch | Apache Airflow, Luigi |
| **Managed Kubernetes** | Amazon EKS | Google Kubernetes Engine (GKE) | Azure Kubernetes Service (AKS) | Kubernetes, K3s, MicroK8s |

---

### Storage Services

| **Service Category** | **AWS** | **GCP** | **Azure** | **Open Source Alternative** |
|---------------------|---------|---------|-----------|---------------------------|
| **Object Storage** | Amazon S3 | Cloud Storage | Azure Blob Storage | MinIO, Ceph, OpenStack Swift |
| **File Storage** | Amazon EFS | Filestore | Azure Files | NFS, GlusterFS, CephFS |
| **Block Storage** | Amazon EBS | Persistent Disk | Azure Managed Disks | Ceph RBD, LVM, ZFS |
| **Archive Storage** | S3 Glacier / Glacier Deep Archive | Cloud Storage Archive | Azure Archive Storage | Tarsnap, Duplicati |
| **Data Transfer** | AWS DataSync, Transfer Family | Storage Transfer Service | Azure Data Box, AzCopy | rsync, rclone, Syncthing |

---

### Networking Services

| **Service Category** | **AWS** | **GCP** | **Azure** | **Open Source Alternative** |
|---------------------|---------|---------|-----------|---------------------------|
| **Virtual Network** | Amazon VPC | Virtual Private Cloud (VPC) | Azure Virtual Network (VNet) | OpenStack Neutron, Calico |
| **Subnet** | VPC Subnet | VPC Subnet | VNet Subnet | VLAN, Network Namespaces |
| **Load Balancer** | Elastic Load Balancing (ALB/NLB) | Cloud Load Balancing | Azure Load Balancer / Application Gateway | HAProxy, NGINX, Traefik |
| **CDN** | Amazon CloudFront | Cloud CDN | Azure CDN | Varnish, NGINX, Cloudflare (free tier) |
| **DNS** | Amazon Route 53 | Cloud DNS | Azure DNS | BIND, PowerDNS, CoreDNS |
| **VPN** | AWS VPN | Cloud VPN | Azure VPN Gateway | OpenVPN, WireGuard, StrongSwan |
| **Direct Connection** | AWS Direct Connect | Cloud Interconnect | Azure ExpressRoute | Dedicated fiber, MPLS |
| **NAT Gateway** | NAT Gateway | Cloud NAT | NAT Gateway | iptables, nftables |
| **Private Link** | AWS PrivateLink | Private Service Connect | Azure Private Link | VPN, SSH Tunneling |

---

### Security Services

| **Service Category** | **AWS** | **GCP** | **Azure** | **Open Source Alternative** |
|---------------------|---------|---------|-----------|---------------------------|
| **Firewall** | Security Groups, Network ACLs | Firewall Rules | Network Security Groups (NSG) | iptables, nftables, ufw |
| **Web Application Firewall** | AWS WAF | Cloud Armor | Azure WAF | ModSecurity, NAXSI |
| **DDoS Protection** | AWS Shield | Cloud Armor | Azure DDoS Protection | Fail2ban, rate limiting |
| **Identity & Access Management** | AWS IAM | Cloud IAM | Azure Active Directory / RBAC | Keycloak, FreeIPA, OpenLDAP |
| **Secrets Management** | AWS Secrets Manager | Secret Manager | Azure Key Vault | HashiCorp Vault, Bitwarden |
| **Certificate Management** | AWS Certificate Manager (ACM) | Certificate Manager | Azure Key Vault Certificates | Let's Encrypt, OpenSSL |
| **Encryption Key Management** | AWS KMS | Cloud KMS | Azure Key Vault | HashiCorp Vault, OpenSSL |
| **Security Monitoring** | Amazon GuardDuty | Security Command Center | Microsoft Defender for Cloud | OSSEC, Wazuh, Falco |
| **Compliance** | AWS Audit Manager | Security Command Center | Azure Policy / Compliance | Open Policy Agent (OPA) |

---

### Database Services

| **Service Category** | **AWS** | **GCP** | **Azure** | **Open Source Alternative** |
|---------------------|---------|---------|-----------|---------------------------|
| **Relational Database** | Amazon RDS | Cloud SQL | Azure SQL Database | PostgreSQL, MySQL, MariaDB |
| **NoSQL Database** | DynamoDB | Firestore, Bigtable | Cosmos DB | MongoDB, Cassandra, CouchDB |
| **In-Memory Cache** | Amazon ElastiCache | Memorystore | Azure Cache for Redis | Redis, Memcached |
| **Data Warehouse** | Amazon Redshift | BigQuery | Azure Synapse Analytics | Apache Druid, ClickHouse |
| **Graph Database** | Amazon Neptune | N/A (use Datastore) | Cosmos DB (Gremlin API) | Neo4j, ArangoDB, JanusGraph |
| **Time Series Database** | Amazon Timestream | N/A (use Bigtable) | Azure Data Explorer | InfluxDB, TimescaleDB, Prometheus |

---

### Monitoring & Logging

| **Service Category** | **AWS** | **GCP** | **Azure** | **Open Source Alternative** |
|---------------------|---------|---------|-----------|---------------------------|
| **Logging** | CloudWatch Logs | Cloud Logging | Azure Monitor Logs | ELK Stack (Elasticsearch, Logstash, Kibana), Loki |
| **Metrics** | CloudWatch Metrics | Cloud Monitoring | Azure Monitor Metrics | Prometheus, Grafana, Graphite |
| **Tracing** | AWS X-Ray | Cloud Trace | Application Insights | Jaeger, Zipkin, OpenTelemetry |
| **Application Performance** | CloudWatch Application Insights | Cloud Profiler | Application Insights | New Relic (open source agent), AppDynamics |
| **Log Analysis** | CloudWatch Logs Insights | Logs Explorer | Log Analytics (KQL) | ELK, Graylog, Splunk (free tier) |
| **Dashboards** | CloudWatch Dashboards | Cloud Monitoring Dashboards | Azure Dashboards / Workbooks | Grafana, Kibana, Chronograf |

---

### Messaging & Event Services

| **Service Category** | **AWS** | **GCP** | **Azure** | **Open Source Alternative** |
|---------------------|---------|---------|-----------|---------------------------|
| **Message Queue** | Amazon SQS | Cloud Tasks | Azure Queue Storage | RabbitMQ, Apache Kafka, ActiveMQ |
| **Pub/Sub Messaging** | Amazon SNS | Cloud Pub/Sub | Azure Service Bus | NATS, Apache Kafka, RabbitMQ |
| **Event Bus** | Amazon EventBridge | Eventarc | Azure Event Grid | Apache Kafka, NATS |
| **Streaming** | Amazon Kinesis | Cloud Pub/Sub, Dataflow | Azure Event Hubs | Apache Kafka, Apache Pulsar, Redpanda |
| **Workflow Orchestration** | AWS Step Functions | Cloud Workflows | Azure Logic Apps | Apache Airflow, Temporal, Prefect |

---

### DevOps & CI/CD

| **Service Category** | **AWS** | **GCP** | **Azure** | **Open Source Alternative** |
|---------------------|---------|---------|-----------|---------------------------|
| **Source Control** | AWS CodeCommit | Cloud Source Repositories | Azure Repos | GitLab, Gitea, Gogs |
| **Build Service** | AWS CodeBuild | Cloud Build | Azure Pipelines | Jenkins, GitLab CI, Drone |
| **Deployment** | AWS CodeDeploy | Cloud Deploy | Azure Pipelines | Spinnaker, Argo CD, Flux |
| **Pipeline** | AWS CodePipeline | Cloud Build Triggers | Azure Pipelines | Jenkins, GitLab CI, Tekton |
| **Container Registry** | Amazon ECR | Artifact Registry, Container Registry | Azure Container Registry | Docker Registry, Harbor, Quay |
| **Infrastructure as Code** | AWS CloudFormation | Deployment Manager | Azure Resource Manager (ARM) | Terraform, Pulumi, Ansible |

---

### AI/ML Services

| **Service Category** | **AWS** | **GCP** | **Azure** | **Open Source Alternative** |
|---------------------|---------|---------|-----------|---------------------------|
| **Machine Learning Platform** | Amazon SageMaker | Vertex AI | Azure Machine Learning | Kubeflow, MLflow, H2O.ai |
| **Managed Notebooks** | SageMaker Notebooks | Vertex AI Workbench | Azure ML Notebooks | JupyterHub, Zeppelin |
| **Model Training** | SageMaker Training | Vertex AI Training | Azure ML Training | TensorFlow, PyTorch, scikit-learn |
| **Model Deployment** | SageMaker Endpoints | Vertex AI Predictions | Azure ML Endpoints | TensorFlow Serving, TorchServe, Seldon |
| **AutoML** | SageMaker Autopilot | AutoML Tables | Azure AutoML | Auto-sklearn, TPOT, H2O AutoML |
| **Pre-trained Models** | AWS AI Services | Cloud AI APIs | Azure Cognitive Services | Hugging Face, OpenAI (API) |

---

### Analytics & Big Data

| **Service Category** | **AWS** | **GCP** | **Azure** | **Open Source Alternative** |
|---------------------|---------|---------|-----------|---------------------------|
| **Data Warehouse** | Amazon Redshift | BigQuery | Azure Synapse Analytics | Apache Hive, Presto, ClickHouse |
| **ETL/Data Pipeline** | AWS Glue | Cloud Dataflow, Dataprep | Azure Data Factory | Apache Airflow, Apache NiFi, Talend |
| **Stream Processing** | Amazon Kinesis Data Analytics | Dataflow | Azure Stream Analytics | Apache Flink, Apache Storm, Apache Spark Streaming |
| **Data Catalog** | AWS Glue Data Catalog | Data Catalog | Azure Purview | Apache Atlas, Amundsen |
| **BI & Visualization** | Amazon QuickSight | Looker, Data Studio | Power BI | Apache Superset, Metabase, Redash |
| **Search & Analytics** | Amazon OpenSearch | N/A (use Dataflow) | Azure Cognitive Search | Elasticsearch, Apache Solr, Meilisearch |

---

## Serverless File Transfer Solution - Detailed Component Mapping

### Architecture Component Matrix

| **Component** | **AWS Implementation** | **GCP Implementation** | **Azure Implementation** |
|--------------|----------------------|----------------------|------------------------|
| **Serverless Compute** | AWS Lambda (Python 3.11, 512 MB, 300s timeout, VPC-enabled) | Cloud Functions 2nd Gen (Python 3.11, 512 MiB, 300s timeout, VPC connector) | Azure Functions (Python 3.11, Consumption/Premium Plan, VNet integration) |
| **Object Storage** | Amazon S3 (Versioning, SSE-S3/KMS, lifecycle policies) | Cloud Storage (Versioning, Google-managed/CMEK, lifecycle rules) | Azure Blob Storage (Versioning, Microsoft-managed/CMK, lifecycle management) |
| **Virtual Network** | Amazon VPC (10.0.0.0/16, DNS enabled) | Google VPC (Custom mode, Private Google Access) | Azure Virtual Network (10.0.0.0/16, Azure-provided DNS) |
| **Private Subnet** | VPC Subnet (10.0.1.0/24, 10.0.2.0/24, multi-AZ) | VPC Subnet (10.0.1.0/24, 10.0.2.0/24, regional) | VNet Subnet (10.0.1.0/24, 10.0.2.0/24) |
| **Security Rules** | Security Group (Egress: 443 HTTPS, 22 SSH) | Firewall Rules (Egress: googleapis.com:443, SFTP:22) | Network Security Group (Outbound: Storage:443, SFTP:22) |
| **Private Endpoint** | VPC Gateway Endpoint (S3, Gateway type, FREE) | Private Google Access (Subnet-level, FREE) | Service Endpoint (Microsoft.Storage, FREE) or Private Endpoint ($7.30/mo) |
| **IAM/RBAC** | IAM Role (Lambda execution role, least privilege policies) | Service Account (Custom, least privilege roles) | Managed Identity (System-assigned, RBAC role assignments) |
| **Secrets Storage** | AWS Secrets Manager (JSON secret, KMS encrypted) | Secret Manager (Versioned, Google-managed/CMEK) | Azure Key Vault (Secrets, soft delete, purge protection) |
| **Logging** | CloudWatch Logs (Log group, 7-day retention) | Cloud Logging (Log name, 30-day default retention) | Azure Monitor Logs (Log Analytics workspace, 30-day retention) |
| **Metrics** | CloudWatch Metrics (AWS/Lambda namespace, custom metrics) | Cloud Monitoring (cloud.googleapis.com/function/*, custom metrics) | Azure Monitor Metrics (Platform metrics, custom metrics) |
| **Alerting** | CloudWatch Alarms (Metric-based, SNS notifications) | Cloud Monitoring Alerts (Policies, Pub/Sub/Email) | Azure Monitor Alerts (Metric/log alerts, Action Groups) |
| **Scheduler** | EventBridge Rule (Cron expression, Lambda target) | Cloud Scheduler (Cron, HTTP target to Cloud Functions) | Timer Trigger (NCRONTAB expression, direct function trigger) |
| **Notifications** | Amazon SNS / EventBridge | Cloud Pub/Sub | Azure Event Grid |
| **Audit Logging** | AWS CloudTrail | Cloud Audit Logs | Azure Activity Log |
| **Encryption (Transit)** | TLS 1.2+ (S3 enforced) | TLS 1.2+ (GCS enforced) | TLS 1.2+ (enforced) |
| **Encryption (Rest)** | S3 SSE-S3 (AES-256) or SSE-KMS | Google-managed or CMEK (AES-256) | Storage Service Encryption (AES-256) |

---

## Networking Deep Dive

### Private Connectivity Models

#### AWS: VPC Gateway Endpoint

**Characteristics:**
- **Type:** Gateway endpoint (not interface endpoint)
- **Target Service:** S3 (and DynamoDB)
- **Cost:** FREE (no hourly charge, no data processing charge)
- **Integration:** Automatic route table updates
- **DNS:** Uses public S3 DNS (e.g., bucket-name.s3.amazonaws.com)
- **Security:** Endpoint policy for additional access control
- **Traffic Path:** Lambda → Route Table → Gateway Endpoint → S3 (private AWS network)

**Terraform Example:**
```hcl
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private.id]
}
```

**Limitations:**
- Only available for S3 and DynamoDB
- Must be in same region as VPC
- Cannot be used from on-premises via VPN/Direct Connect

---

#### GCP: Private Google Access

**Characteristics:**
- **Type:** Subnet-level configuration
- **Target Service:** All Google APIs (including Cloud Storage)
- **Cost:** FREE
- **Integration:** Enable on subnet, configure firewall rules
- **DNS:** Uses restricted.googleapis.com or private.googleapis.com
- **Security:** VPC Service Controls for perimeter security
- **Traffic Path:** Cloud Functions → Serverless VPC Connector → Private Google Access → Cloud Storage

**Terraform Example:**
```hcl
resource "google_compute_subnetwork" "private" {
  name                     = "private-subnet"
  ip_cidr_range            = "10.0.1.0/24"
  region                   = var.region
  network                  = google_compute_network.vpc.id
  private_ip_google_access = true
}

resource "google_vpc_access_connector" "connector" {
  name          = "vpc-connector"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.8.0.0/28"
}
```

**Limitations:**
- Serverless VPC Connector has costs ($0.07/hour)
- Connector has throughput limits (200-300 Mbps for e2-micro)
- Must configure DNS to use restricted or private googleapis endpoints

---

#### Azure: Service Endpoint / Private Endpoint

**Characteristics (Service Endpoint):**
- **Type:** Subnet-level configuration
- **Target Service:** Multiple Azure services (Storage, SQL, etc.)
- **Cost:** FREE
- **Integration:** Enable on subnet, configure NSG rules
- **Security:** Storage firewall rules for additional control
- **Traffic Path:** Azure Functions → VNet Integration → Service Endpoint → Blob Storage

**Terraform Example (Service Endpoint):**
```hcl
resource "azurerm_subnet" "function" {
  name                 = "function-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
  
  service_endpoints = ["Microsoft.Storage"]
}

resource "azurerm_storage_account_network_rules" "rules" {
  storage_account_id = azurerm_storage_account.files.id
  default_action     = "Deny"
  virtual_network_subnet_ids = [azurerm_subnet.function.id]
}
```

**Characteristics (Private Endpoint):**
- **Type:** Dedicated network interface with private IP
- **Cost:** $7.30/month + $0.01/GB data processed
- **Security:** Higher isolation, private DNS zone
- **Traffic Path:** Azure Functions → VNet → Private Endpoint → Blob Storage (never leaves Microsoft network)

**Terraform Example (Private Endpoint):**
```hcl
resource "azurerm_private_endpoint" "storage" {
  name                = "storage-private-endpoint"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.function.id
  
  private_service_connection {
    name                           = "storage-connection"
    private_connection_resource_id = azurerm_storage_account.files.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }
}
```

**Decision Matrix:**
- Use **Service Endpoint** for cost-sensitive scenarios, adequate security
- Use **Private Endpoint** for maximum isolation, compliance requirements

---

## Cost Optimization Comparison

### Storage Lifecycle Policies

#### AWS S3 Lifecycle Tiers

| **Tier** | **Cost (per GB/month)** | **Retrieval Cost** | **Transition After** | **Use Case** |
|---------|------------------------|-------------------|-------------------|-------------|
| S3 Standard | $0.023 | None | - | Frequently accessed |
| S3 Standard-IA | $0.0125 (46% savings) | $0.01/GB | 30 days | Infrequent access |
| S3 Glacier Instant Retrieval | $0.004 (83% savings) | $0.03/GB | 90 days | Quarterly access |
| S3 Glacier Flexible Retrieval | $0.0036 (84% savings) | $0.03/GB (3-5 hours) | 180 days | Rarely accessed |
| S3 Glacier Deep Archive | $0.00099 (96% savings) | $0.02/GB (12 hours) | 365 days | Long-term archive |

**Terraform Example:**
```hcl
resource "aws_s3_bucket_lifecycle_configuration" "lifecycle" {
  bucket = aws_s3_bucket.files.id
  
  rule {
    id     = "transition-rule"
    status = "Enabled"
    
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    
    transition {
      days          = 90
      storage_class = "GLACIER_IR"
    }
    
    transition {
      days          = 180
      storage_class = "DEEP_ARCHIVE"
    }
  }
}
```

---

#### GCP Cloud Storage Lifecycle Tiers

| **Tier** | **Cost (per GB/month)** | **Retrieval Cost** | **Transition After** | **Use Case** |
|---------|------------------------|-------------------|-------------------|-------------|
| Standard | $0.020 | None | - | Frequently accessed |
| Nearline | $0.010 (50% savings) | $0.01/GB | 30 days | Monthly access |
| Coldline | $0.004 (80% savings) | $0.02/GB | 90 days | Quarterly access |
| Archive | $0.0012 (94% savings) | $0.05/GB | 365 days | Long-term archive |

**Terraform Example:**
```hcl
resource "google_storage_bucket" "files" {
  name     = "file-transfer-bucket"
  location = "US"
  
  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
    condition {
      age = 30
    }
  }
  
  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
    condition {
      age = 90
    }
  }
  
  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
    condition {
      age = 365
    }
  }
}
```

---

#### Azure Blob Storage Lifecycle Tiers

| **Tier** | **Cost (per GB/month)** | **Retrieval Cost** | **Transition After** | **Use Case** |
|---------|------------------------|-------------------|-------------------|-------------|
| Hot | $0.018 | None | - | Frequently accessed |
| Cool | $0.010 (44% savings) | $0.01/GB | 30 days | Infrequent access |
| Archive | $0.00099 (95% savings) | $0.02/GB + priority | 90 days | Long-term archive |

**Terraform Example:**
```hcl
resource "azurerm_storage_management_policy" "lifecycle" {
  storage_account_id = azurerm_storage_account.files.id
  
  rule {
    name    = "lifecycle-rule"
    enabled = true
    
    filters {
      blob_types = ["blockBlob"]
    }
    
    actions {
      base_blob {
        tier_to_cool_after_days_since_modification_greater_than    = 30
        tier_to_archive_after_days_since_modification_greater_than = 90
      }
    }
  }
}
```

---

## Security Best Practices - Universal

### Defense in Depth Checklist

#### Network Security
- [ ] Deploy serverless functions in private subnets/networks
- [ ] Use restrictive security groups/firewall rules (egress only)
- [ ] Enable private connectivity to object storage (no internet routing)
- [ ] Disable public access to object storage buckets
- [ ] Implement network flow logs for audit trail
- [ ] Use VPN/Direct Connect for on-premises connectivity (if needed)

#### Identity & Access Control
- [ ] Use least privilege IAM/RBAC policies
- [ ] Avoid long-lived credentials (use temporary tokens/managed identities)
- [ ] Implement service-specific roles (not shared roles)
- [ ] Enable multi-factor authentication (MFA) for human access
- [ ] Regularly rotate credentials
- [ ] Use resource-based policies for additional access control

#### Data Protection
- [ ] Enable encryption in transit (TLS 1.2+)
- [ ] Enable encryption at rest (AES-256)
- [ ] Use managed encryption keys or bring your own key (BYOK)
- [ ] Enable versioning on object storage
- [ ] Implement data classification and tagging
- [ ] Use Object Lock (AWS) / Retention Policies (GCP/Azure) for immutability

#### Secrets Management
- [ ] Store credentials in dedicated secrets service (Secrets Manager/Key Vault)
- [ ] Encrypt secrets with KMS/CMK
- [ ] Implement automatic rotation where possible
- [ ] Audit all secret access
- [ ] Use short-lived credentials when possible

#### Monitoring & Audit
- [ ] Enable comprehensive logging (all API calls)
- [ ] Set up real-time alerts for anomalies
- [ ] Implement centralized log aggregation
- [ ] Enable audit logs (CloudTrail/Cloud Audit Logs/Activity Log)
- [ ] Create dashboards for visibility
- [ ] Conduct regular security reviews

#### Compliance
- [ ] Document security controls for compliance frameworks
- [ ] Implement data retention policies
- [ ] Enable compliance monitoring tools
- [ ] Conduct regular vulnerability assessments
- [ ] Maintain incident response plans
- [ ] Perform regular compliance audits

---

## Summary

This component mapping table provides a comprehensive cross-cloud reference for implementing secure file transfer infrastructure across AWS, GCP, and Azure. Key insights:

1. **Core Services Align Well:** All three providers offer equivalent services for compute, storage, networking, and security
2. **Pricing Differences:** AWS offers free VPC Gateway Endpoint; GCP has VPC Connector costs; Azure offers free Service Endpoints
3. **Security Models:** Similar defense-in-depth approaches, with provider-specific implementations
4. **Portability:** Application code is highly portable; infrastructure requires cloud-specific configurations

Use this table as a reference when:
- Planning multi-cloud deployments
- Migrating between cloud providers
- Evaluating cost-benefit of different providers
- Implementing disaster recovery across clouds
- Standardizing security practices

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-21  
**Companion Document:** INFRASTRUCTURE-COMPOSER.md
