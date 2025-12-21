# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-${var.environment}-vpc"
  }
}

# Private Subnets
resource "aws_subnet" "private" {
  count                   = length(var.private_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.private_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = false

  tags = {
    Name = "${var.project_name}-${var.environment}-private-subnet-${count.index + 1}"
    Tier = "Private"
  }
}

# Route Table for Private Subnets
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-${var.environment}-private-rt"
  }
}

# Associate Route Table with Private Subnets
resource "aws_route_table_association" "private" {
  count          = length(var.private_subnet_cidrs)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

# Security Group for Lambda
resource "aws_security_group" "lambda" {
  name        = "${var.project_name}-${var.environment}-lambda-sg"
  description = "Security group for Lambda function with VPC access"
  vpc_id      = aws_vpc.main.id

  # Egress rule for HTTPS to S3 (via Gateway Endpoint)
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS to S3 via Gateway Endpoint"
  }

  # Egress rule for SFTP
  egress {
    from_port   = var.sftp_port
    to_port     = var.sftp_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SFTP access to legacy system"
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-lambda-sg"
  }
}
