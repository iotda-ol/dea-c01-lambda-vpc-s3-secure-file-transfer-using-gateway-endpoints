# S3 Module - Main Configuration
# Purpose: Create secure S3 bucket for file storage

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# S3 Bucket
resource "aws_s3_bucket" "main" {
  bucket = var.bucket_name

  tags = merge(
    var.tags,
    {
      Name = var.bucket_name
    }
  )
}

# Block Public Access
resource "aws_s3_bucket_public_access_block" "main" {
  bucket = aws_s3_bucket.main.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Versioning
resource "aws_s3_bucket_versioning" "main" {
  bucket = aws_s3_bucket.main.id

  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Disabled"
  }
}

# Server-Side Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = var.kms_key_id != null ? "aws:kms" : "AES256"
      kms_master_key_id = var.kms_key_id
    }
    bucket_key_enabled = var.kms_key_id != null ? true : false
  }
}

# Lifecycle Rules
resource "aws_s3_bucket_lifecycle_configuration" "main" {
  count = var.enable_lifecycle_rules ? 1 : 0

  bucket = aws_s3_bucket.main.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    transition {
      days          = var.transition_to_ia_days
      storage_class = "STANDARD_IA"
    }
  }

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    transition {
      days          = var.transition_to_glacier_days
      storage_class = "GLACIER"
    }
  }

  rule {
    id     = "expire-old-versions"
    status = var.enable_versioning ? "Enabled" : "Disabled"

    noncurrent_version_expiration {
      noncurrent_days = var.noncurrent_version_expiration_days
    }
  }

  rule {
    id     = "delete-incomplete-uploads"
    status = "Enabled"

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

# Bucket Policy for VPC Endpoint Access
resource "aws_s3_bucket_policy" "main" {
  count = var.vpc_endpoint_id != null ? 1 : 0

  bucket = aws_s3_bucket.main.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowVPCEndpointAccess"
        Effect = "Allow"
        Principal = {
          AWS = var.allowed_principal_arns
        }
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.main.arn,
          "${aws_s3_bucket.main.arn}/*"
        ]
        Condition = {
          StringEquals = {
            "aws:SourceVpce" = var.vpc_endpoint_id
          }
        }
      },
      {
        Sid    = "DenyUnencryptedObjectUploads"
        Effect = "Deny"
        Principal = "*"
        Action = "s3:PutObject"
        Resource = "${aws_s3_bucket.main.arn}/*"
        Condition = {
          StringNotEquals = {
            "s3:x-amz-server-side-encryption" = var.kms_key_id != null ? "aws:kms" : "AES256"
          }
        }
      }
    ]
  })
}

# Logging Bucket (Optional)
resource "aws_s3_bucket" "logs" {
  count = var.enable_logging ? 1 : 0

  bucket = "${var.bucket_name}-logs"

  tags = merge(
    var.tags,
    {
      Name = "${var.bucket_name}-logs"
    }
  )
}

# Block Public Access for Logging Bucket
resource "aws_s3_bucket_public_access_block" "logs" {
  count = var.enable_logging ? 1 : 0

  bucket = aws_s3_bucket.logs[0].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable Logging
resource "aws_s3_bucket_logging" "main" {
  count = var.enable_logging ? 1 : 0

  bucket = aws_s3_bucket.main.id

  target_bucket = aws_s3_bucket.logs[0].id
  target_prefix = "access-logs/"
}
