# Development Environment - Main Configuration
# Purpose: Orchestrate all modules for development deployment

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    # Configure backend for state management
    # Uncomment and configure for production use
    # bucket         = "your-terraform-state-bucket"
    # key            = "dev/terraform.tfstate"
    # region         = "us-east-1"
    # encrypt        = true
    # dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = "dev"
      Project     = "secure-file-transfer"
      ManagedBy   = "Terraform"
    }
  }
}

# Local variables
locals {
  name_prefix = "secure-transfer-dev"
  
  common_tags = {
    Environment = "dev"
    Project     = "secure-file-transfer"
    ManagedBy   = "Terraform"
  }
}

# VPC Module
module "vpc" {
  source = "../../modules/vpc"
  
  name_prefix          = local.name_prefix
  vpc_cidr             = var.vpc_cidr
  private_subnet_cidrs = var.private_subnet_cidrs
  availability_zones   = var.availability_zones
  enable_flow_logs     = var.enable_flow_logs
  
  tags = local.common_tags
}

# Security Groups Module
module "security_groups" {
  source = "../../modules/security-groups"
  
  name_prefix         = local.name_prefix
  vpc_id              = module.vpc.vpc_id
  enable_sftp_egress  = true
  
  tags = local.common_tags
}

# Gateway Endpoint Module
module "gateway_endpoint" {
  source = "../../modules/gateway-endpoint"
  
  name_prefix     = local.name_prefix
  vpc_id          = module.vpc.vpc_id
  region          = var.aws_region
  route_table_ids = [module.vpc.private_route_table_id]
  allowed_buckets = [var.s3_bucket_name]
  
  tags = local.common_tags
}

# S3 Module
module "s3" {
  source = "../../modules/s3"
  
  bucket_name               = var.s3_bucket_name
  enable_versioning         = true
  enable_lifecycle_rules    = true
  vpc_endpoint_id           = module.gateway_endpoint.s3_endpoint_id
  allowed_principal_arns    = [module.iam.lambda_execution_role_arn]
  enable_logging            = false
  
  tags = local.common_tags
}

# IAM Module
module "iam" {
  source = "../../modules/iam"
  
  name_prefix            = local.name_prefix
  s3_bucket_arns         = [module.s3.bucket_arn]
  enable_secrets_manager = true
  secrets_arns           = [var.sftp_secret_arn]
  enable_xray            = var.enable_xray
  
  tags = local.common_tags
}

# Lambda Module
module "lambda" {
  source = "../../modules/lambda"
  
  function_name      = "${local.name_prefix}-function"
  description        = "Secure file transfer from SFTP to S3"
  execution_role_arn = module.iam.lambda_execution_role_arn
  handler            = "main.handler"
  runtime            = "python3.11"
  timeout            = 300
  memory_size        = 512
  source_code_path   = var.lambda_source_path
  
  subnet_ids         = module.vpc.private_subnet_ids
  security_group_ids = [module.security_groups.lambda_security_group_id]
  
  environment_variables = {
    S3_BUCKET         = module.s3.bucket_id
    S3_PREFIX         = var.s3_prefix
    SFTP_HOST         = var.sftp_host
    SFTP_PORT         = var.sftp_port
    SFTP_USERNAME     = var.sftp_username
    SFTP_SECRET_NAME  = var.sftp_secret_name
    MAX_FILE_SIZE_MB  = var.max_file_size_mb
  }
  
  log_level           = var.log_level
  log_retention_days  = 7
  enable_xray         = var.enable_xray
  
  enable_error_alarm    = true
  enable_throttle_alarm = true
  
  tags = local.common_tags
}
