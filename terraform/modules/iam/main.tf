# IAM Module - Main Configuration
# Purpose: Create IAM roles and policies for Lambda execution

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Lambda Execution Role
resource "aws_iam_role" "lambda_execution" {
  name = "${var.name_prefix}-lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-lambda-execution-role"
    }
  )
}

# VPC Execution Policy (for Lambda in VPC)
resource "aws_iam_role_policy_attachment" "lambda_vpc_execution" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

# CloudWatch Logs Policy
resource "aws_iam_role_policy" "lambda_logging" {
  name = "${var.name_prefix}-lambda-logging-policy"
  role = aws_iam_role.lambda_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# S3 Access Policy
resource "aws_iam_role_policy" "lambda_s3_access" {
  name = "${var.name_prefix}-lambda-s3-policy"
  role = aws_iam_role.lambda_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = concat(
          [for bucket in var.s3_bucket_arns : bucket],
          [for bucket in var.s3_bucket_arns : "${bucket}/*"]
        )
      }
    ]
  })
}

# Secrets Manager Access Policy (Optional)
resource "aws_iam_role_policy" "lambda_secrets_access" {
  count = var.enable_secrets_manager ? 1 : 0

  name = "${var.name_prefix}-lambda-secrets-policy"
  role = aws_iam_role.lambda_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = var.secrets_arns
      }
    ]
  })
}

# KMS Access Policy (Optional)
resource "aws_iam_role_policy" "lambda_kms_access" {
  count = var.enable_kms ? 1 : 0

  name = "${var.name_prefix}-lambda-kms-policy"
  role = aws_iam_role.lambda_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:Encrypt",
          "kms:GenerateDataKey"
        ]
        Resource = var.kms_key_arns
      }
    ]
  })
}

# X-Ray Tracing Policy (Optional)
resource "aws_iam_role_policy_attachment" "lambda_xray" {
  count = var.enable_xray ? 1 : 0

  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}
