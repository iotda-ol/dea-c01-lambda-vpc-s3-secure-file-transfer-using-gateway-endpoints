# S3 Bucket for File Transfer
resource "aws_s3_bucket" "file_transfer" {
  bucket_prefix = "${var.project_name}-${var.environment}-files-"

  tags = {
    Name        = "${var.project_name}-${var.environment}-file-transfer-bucket"
    Environment = var.environment
  }
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "file_transfer" {
  bucket = aws_s3_bucket.file_transfer.id

  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket Server-Side Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "file_transfer" {
  bucket = aws_s3_bucket.file_transfer.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

# S3 Bucket Public Access Block
resource "aws_s3_bucket_public_access_block" "file_transfer" {
  bucket = aws_s3_bucket.file_transfer.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# S3 Bucket Lifecycle Policy for Cost Optimization
resource "aws_s3_bucket_lifecycle_configuration" "file_transfer" {
  bucket = aws_s3_bucket.file_transfer.id

  rule {
    id     = "transition-to-ia"
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

  rule {
    id     = "delete-old-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

# S3 VPC Gateway Endpoint
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.${var.aws_region}.s3"
  vpc_endpoint_type = "Gateway"

  route_table_ids = [aws_route_table.private.id]

  tags = {
    Name = "${var.project_name}-${var.environment}-s3-gateway-endpoint"
  }
}

# S3 VPC Endpoint Policy (Least Privilege)
resource "aws_vpc_endpoint_policy" "s3" {
  vpc_endpoint_id = aws_vpc_endpoint.s3.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.lambda.arn
        }
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl",
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.file_transfer.arn,
          "${aws_s3_bucket.file_transfer.arn}/*"
        ]
      }
    ]
  })
}
