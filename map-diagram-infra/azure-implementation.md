# Azure Implementation Guide

## Overview

This guide provides step-by-step instructions for deploying the secure file transfer architecture on Microsoft Azure.

---

## Prerequisites

- Azure Subscription with appropriate permissions
- Azure CLI installed and configured
- Terraform >= 1.0
- Python >= 3.11
- Git

---

## Architecture Components (Azure-Specific)

| Component | Azure Service | Notes |
|-----------|---------------|-------|
| Virtual Network | Virtual Network (VNet) | Address space: 10.0.0.0/16 |
| Serverless Compute | Azure Functions | Python 3.11 (Linux) |
| Object Storage | Blob Storage | With versioning & lifecycle |
| Private Endpoint | Private Link | $0.01/hour + data charges |
| Secrets Vault | Key Vault | $0.03/secret/month |
| IAM | Azure AD + RBAC | Managed Identity |
| Logging | Azure Monitor Logs | Log Analytics Workspace |
| Monitoring | Azure Monitor | Metrics and alerts |
| Scheduler | Logic Apps / Timer Trigger | Built into Azure Functions |
| Network Security | Network Security Groups | NSG rules |

---

## Deployment Steps

### Step 1: Set Up Azure CLI

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "Your Subscription Name"

# Verify
az account show
```

### Step 2: Create Resource Group

```bash
# Create resource group
az group create \
  --name secure-transfer-dev-rg \
  --location eastus

# Set as default (optional)
az configure --defaults group=secure-transfer-dev-rg location=eastus
```

### Step 3: Create Terraform Configuration

**main.tf**:
```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

# Data sources
data "azurerm_client_config" "current" {}
```

**variables.tf**:
```hcl
variable "resource_group_name" {
  description = "Resource group name"
  type        = string
  default     = "secure-transfer-dev-rg"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "securetransfer"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vnet_address_space" {
  description = "VNet address space"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "sftp_host" {
  description = "SFTP server hostname"
  type        = string
}

variable "sftp_port" {
  description = "SFTP server port"
  type        = number
  default     = 22
}

variable "sftp_username" {
  description = "SFTP username"
  type        = string
}

variable "schedule" {
  description = "NCRONTAB schedule for function"
  type        = string
  default     = "0 0 2 * * *"  # Daily at 2 AM
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default = {
    Project     = "SecureFileTransfer"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}
```

### Step 4: Create Virtual Network

**network.tf**:
```hcl
# Virtual Network
resource "azurerm_virtual_network" "vnet" {
  name                = "${var.project_name}-${var.environment}-vnet"
  resource_group_name = var.resource_group_name
  location            = var.location
  address_space       = var.vnet_address_space
  
  tags = var.tags
}

# Private Subnet 1
resource "azurerm_subnet" "private_subnet_1" {
  name                 = "${var.project_name}-${var.environment}-private-subnet-1"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
  
  delegation {
    name = "function-delegation"
    
    service_delegation {
      name = "Microsoft.Web/serverFarms"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/action"
      ]
    }
  }
  
  service_endpoints = ["Microsoft.Storage", "Microsoft.KeyVault"]
}

# Private Subnet 2 (for high availability)
resource "azurerm_subnet" "private_subnet_2" {
  name                 = "${var.project_name}-${var.environment}-private-subnet-2"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.2.0/24"]
  
  service_endpoints = ["Microsoft.Storage", "Microsoft.KeyVault"]
}

# Network Security Group
resource "azurerm_network_security_group" "function_nsg" {
  name                = "${var.project_name}-${var.environment}-function-nsg"
  resource_group_name = var.resource_group_name
  location            = var.location
  
  # Allow HTTPS outbound
  security_rule {
    name                       = "AllowHTTPSOutbound"
    priority                   = 100
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  
  # Allow SFTP outbound
  security_rule {
    name                       = "AllowSFTPOutbound"
    priority                   = 110
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"  # Replace with SFTP server IP
  }
  
  tags = var.tags
}

# Associate NSG with subnet
resource "azurerm_subnet_network_security_group_association" "subnet1_nsg" {
  subnet_id                 = azurerm_subnet.private_subnet_1.id
  network_security_group_id = azurerm_network_security_group.function_nsg.id
}
```

### Step 5: Create Storage Account

**storage.tf**:
```hcl
# Random suffix for globally unique storage account name
resource "random_string" "storage_suffix" {
  length  = 8
  special = false
  upper   = false
}

# Storage Account
resource "azurerm_storage_account" "storage" {
  name                     = "${var.project_name}${var.environment}${random_string.storage_suffix.result}"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  
  blob_properties {
    versioning_enabled = true
    
    delete_retention_policy {
      days = 7
    }
  }
  
  network_rules {
    default_action             = "Deny"
    bypass                     = ["AzureServices"]
    virtual_network_subnet_ids = [azurerm_subnet.private_subnet_1.id]
  }
  
  tags = var.tags
}

# Blob Container
resource "azurerm_storage_container" "files" {
  name                  = "uploaded-files"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

# Lifecycle Management Policy
resource "azurerm_storage_management_policy" "lifecycle" {
  storage_account_id = azurerm_storage_account.storage.id
  
  rule {
    name    = "transition-to-cool"
    enabled = true
    
    filters {
      blob_types = ["blockBlob"]
    }
    
    actions {
      base_blob {
        tier_to_cool_after_days_since_modification_greater_than = 30
        tier_to_archive_after_days_since_modification_greater_than = 90
        delete_after_days_since_modification_greater_than = 365
      }
      
      version {
        delete_after_days_since_creation = 90
      }
    }
  }
}

# Private Endpoint for Blob Storage
resource "azurerm_private_endpoint" "blob_private_endpoint" {
  name                = "${var.project_name}-${var.environment}-blob-pe"
  resource_group_name = var.resource_group_name
  location            = var.location
  subnet_id           = azurerm_subnet.private_subnet_2.id
  
  private_service_connection {
    name                           = "${var.project_name}-${var.environment}-blob-psc"
    private_connection_resource_id = azurerm_storage_account.storage.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }
  
  tags = var.tags
}
```

### Step 6: Create Key Vault

**keyvault.tf**:
```hcl
# Key Vault
resource "azurerm_key_vault" "keyvault" {
  name                       = "${var.project_name}-${var.environment}-kv-${random_string.storage_suffix.result}"
  resource_group_name        = var.resource_group_name
  location                   = var.location
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  
  network_acls {
    default_action             = "Deny"
    bypass                     = "AzureServices"
    virtual_network_subnet_ids = [azurerm_subnet.private_subnet_1.id]
  }
  
  tags = var.tags
}

# Access policy for current user (for initial setup)
resource "azurerm_key_vault_access_policy" "current_user" {
  key_vault_id = azurerm_key_vault.keyvault.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id
  
  secret_permissions = [
    "Get", "List", "Set", "Delete", "Purge", "Recover"
  ]
}

# SFTP Credentials Secret (placeholder)
resource "azurerm_key_vault_secret" "sftp_credentials" {
  name         = "sftp-credentials"
  value        = jsonencode({
    username    = var.sftp_username
    password    = ""  # Update manually
    private_key = ""  # Update manually
    host        = var.sftp_host
    port        = var.sftp_port
  })
  key_vault_id = azurerm_key_vault.keyvault.id
  
  depends_on = [azurerm_key_vault_access_policy.current_user]
  
  lifecycle {
    ignore_changes = [value]
  }
}
```

### Step 7: Create Azure Function

**function.tf**:
```hcl
# App Service Plan (Consumption)
resource "azurerm_service_plan" "function_plan" {
  name                = "${var.project_name}-${var.environment}-plan"
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "Y1"  # Consumption plan
  
  tags = var.tags
}

# Application Insights
resource "azurerm_application_insights" "insights" {
  name                = "${var.project_name}-${var.environment}-insights"
  resource_group_name = var.resource_group_name
  location            = var.location
  application_type    = "other"
  
  tags = var.tags
}

# Storage Account for Function App (required)
resource "azurerm_storage_account" "function_storage" {
  name                     = "${var.project_name}${var.environment}fn${random_string.storage_suffix.result}"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  tags = var.tags
}

# Managed Identity
resource "azurerm_user_assigned_identity" "function_identity" {
  name                = "${var.project_name}-${var.environment}-function-identity"
  resource_group_name = var.resource_group_name
  location            = var.location
  
  tags = var.tags
}

# Azure Function App
resource "azurerm_linux_function_app" "function" {
  name                       = "${var.project_name}-${var.environment}-function"
  resource_group_name        = var.resource_group_name
  location                   = var.location
  service_plan_id            = azurerm_service_plan.function_plan.id
  storage_account_name       = azurerm_storage_account.function_storage.name
  storage_account_access_key = azurerm_storage_account.function_storage.primary_access_key
  
  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.function_identity.id]
  }
  
  site_config {
    application_stack {
      python_version = "3.11"
    }
    
    vnet_route_all_enabled = true
  }
  
  virtual_network_subnet_id = azurerm_subnet.private_subnet_1.id
  
  app_settings = {
    "APPINSIGHTS_INSTRUMENTATIONKEY"        = azurerm_application_insights.insights.instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.insights.connection_string
    "STORAGE_ACCOUNT_NAME"                  = azurerm_storage_account.storage.name
    "STORAGE_CONTAINER_NAME"                = azurerm_storage_container.files.name
    "KEY_VAULT_NAME"                        = azurerm_key_vault.keyvault.name
    "SECRET_NAME"                           = azurerm_key_vault_secret.sftp_credentials.name
    "FUNCTIONS_WORKER_RUNTIME"              = "python"
    "AzureWebJobsFeatureFlags"              = "EnableWorkerIndexing"
    "SCHEDULE"                              = var.schedule
  }
  
  tags = var.tags
}
```

### Step 8: Configure IAM/RBAC

**iam.tf**:
```hcl
# Grant Storage Blob Data Contributor to Managed Identity
resource "azurerm_role_assignment" "function_storage_contributor" {
  scope                = azurerm_storage_account.storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.function_identity.principal_id
}

# Grant Key Vault Secrets User to Managed Identity
resource "azurerm_key_vault_access_policy" "function_secrets_access" {
  key_vault_id = azurerm_key_vault.keyvault.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_user_assigned_identity.function_identity.principal_id
  
  secret_permissions = ["Get", "List"]
}
```

### Step 9: Deploy Infrastructure

```bash
# Initialize Terraform
terraform init

# Plan deployment
terraform plan -out=tfplan

# Apply deployment
terraform apply tfplan
```

### Step 10: Deploy Function Code

```bash
# Package function
cd lambda
zip -r function.zip .

# Deploy to Azure Function
az functionapp deployment source config-zip \
  --resource-group secure-transfer-dev-rg \
  --name securetransfer-dev-function \
  --src function.zip
```

### Step 11: Update SFTP Credentials

```bash
# Update Key Vault secret
az keyvault secret set \
  --vault-name <keyvault-name> \
  --name sftp-credentials \
  --value '{
    "username": "your-username",
    "password": "your-password",
    "host": "sftp.example.com",
    "port": 22
  }'
```

### Step 12: Test Function

```bash
# Get function key
FUNCTION_KEY=$(az functionapp keys list \
  --resource-group secure-transfer-dev-rg \
  --name securetransfer-dev-function \
  --query "functionKeys.default" -o tsv)

# Invoke function
curl -X POST "https://securetransfer-dev-function.azurewebsites.net/api/file-transfer?code=$FUNCTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{"test": true}'

# View logs
az monitor app-insights query \
  --app <insights-id> \
  --analytics-query "traces | order by timestamp desc | take 50"
```

---

## Monitoring & Operations

### View Logs

```bash
# Stream logs
az webapp log tail \
  --resource-group secure-transfer-dev-rg \
  --name securetransfer-dev-function

# Query Application Insights
az monitor app-insights query \
  --app <insights-name> \
  --analytics-query "traces | where severityLevel >= 3"
```

---

## Estimated Monthly Costs (Azure)

| Resource | Cost |
|----------|------|
| Azure Functions (1,000 invocations) | $0.20 |
| Blob Storage (100 GB) | $1.80 |
| Private Endpoint | $7.20 |
| Key Vault | $0.03 |
| Application Insights | $0.50 |
| **Total** | **~$9.73/month** |

**Note**: Private Link costs make Azure the most expensive option for this architecture.

---

## Cleanup

```bash
terraform destroy
```

---

## Cost Optimization Tips

1. **Consider Public Endpoint**: If security allows, remove Private Link to save $7.20/month
2. **Use Service Endpoints**: Free alternative to Private Link for Azure services
3. **Storage Lifecycle**: Aggressive tiering to Archive can save 80%+
4. **App Insights Sampling**: Reduce data ingestion costs

---

## Additional Resources

- [Azure Functions VNet Integration](https://docs.microsoft.com/en-us/azure/azure-functions/functions-networking-options)
- [Azure Private Link](https://docs.microsoft.com/en-us/azure/private-link/)
- [Azure Key Vault Best Practices](https://docs.microsoft.com/en-us/azure/key-vault/general/best-practices)
