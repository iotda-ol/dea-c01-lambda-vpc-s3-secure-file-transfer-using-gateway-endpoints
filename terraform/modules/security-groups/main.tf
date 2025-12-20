# Security Groups Module - Main Configuration
# Purpose: Create security groups for Lambda functions

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Lambda Security Group
resource "aws_security_group" "lambda" {
  name        = "${var.name_prefix}-lambda-sg"
  description = "Security group for Lambda function"
  vpc_id      = var.vpc_id

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-lambda-sg"
    }
  )
}

# Egress rule for HTTPS (S3 access via gateway endpoint)
resource "aws_vpc_security_group_egress_rule" "lambda_https" {
  security_group_id = aws_security_group.lambda.id
  description       = "Allow HTTPS outbound for S3 access"
  
  ip_protocol = "tcp"
  from_port   = 443
  to_port     = 443
  cidr_ipv4   = "0.0.0.0/0"
}

# Egress rule for SFTP (if enabled)
resource "aws_vpc_security_group_egress_rule" "lambda_sftp" {
  count = var.enable_sftp_egress ? 1 : 0

  security_group_id = aws_security_group.lambda.id
  description       = "Allow SFTP outbound"
  
  ip_protocol = "tcp"
  from_port   = 22
  to_port     = 22
  cidr_ipv4   = "0.0.0.0/0"
}

# Egress rule for custom ports
resource "aws_vpc_security_group_egress_rule" "lambda_custom" {
  for_each = var.custom_egress_rules

  security_group_id = aws_security_group.lambda.id
  description       = each.value.description
  
  ip_protocol = each.value.protocol
  from_port   = each.value.from_port
  to_port     = each.value.to_port
  cidr_ipv4   = each.value.cidr_ipv4
}
