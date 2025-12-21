# IAM Role for Lambda Function
resource "aws_iam_role" "lambda" {
  name_prefix = "${var.project_name}-${var.environment}-lambda-"

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

  tags = {
    Name = "${var.project_name}-${var.environment}-lambda-role"
  }
}

# IAM Policy for S3 Access (Least Privilege)
resource "aws_iam_policy" "lambda_s3" {
  name_prefix = "${var.project_name}-${var.environment}-lambda-s3-"
  description = "Least privilege policy for Lambda to access S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl"
        ]
        Resource = "${aws_s3_bucket.file_transfer.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.file_transfer.arn
      }
    ]
  })
}

# IAM Policy for CloudWatch Logs
resource "aws_iam_policy" "lambda_logs" {
  name_prefix = "${var.project_name}-${var.environment}-lambda-logs-"
  description = "Policy for Lambda to write logs to CloudWatch"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "${aws_cloudwatch_log_group.lambda.arn}:*"
      }
    ]
  })
}

# IAM Policy for VPC Network Interfaces (Required for VPC Lambda)
resource "aws_iam_policy" "lambda_vpc" {
  name_prefix = "${var.project_name}-${var.environment}-lambda-vpc-"
  description = "Policy for Lambda to create/manage VPC network interfaces"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface",
          "ec2:AssignPrivateIpAddresses",
          "ec2:UnassignPrivateIpAddresses"
        ]
        Resource = "*"
      }
    ]
  })
}

# IAM Policy for Secrets Manager (for SFTP credentials)
resource "aws_iam_policy" "lambda_secrets" {
  name_prefix = "${var.project_name}-${var.environment}-lambda-secrets-"
  description = "Policy for Lambda to retrieve SFTP credentials from Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = aws_secretsmanager_secret.sftp_credentials.arn
      }
    ]
  })
}

# Attach Policies to Lambda Role
resource "aws_iam_role_policy_attachment" "lambda_s3" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_s3.arn
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_logs.arn
}

resource "aws_iam_role_policy_attachment" "lambda_vpc" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_vpc.arn
}

resource "aws_iam_role_policy_attachment" "lambda_secrets" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_secrets.arn
}
