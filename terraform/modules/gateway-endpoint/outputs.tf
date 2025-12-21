# Gateway Endpoint Module - Outputs
# Purpose: Export endpoint information

output "s3_endpoint_id" {
  description = "ID of the S3 VPC endpoint"
  value       = aws_vpc_endpoint.s3.id
}

output "s3_endpoint_state" {
  description = "State of the S3 VPC endpoint"
  value       = aws_vpc_endpoint.s3.state
}

output "dynamodb_endpoint_id" {
  description = "ID of the DynamoDB VPC endpoint (if enabled)"
  value       = var.enable_dynamodb_endpoint ? aws_vpc_endpoint.dynamodb[0].id : null
}

output "dynamodb_endpoint_state" {
  description = "State of the DynamoDB VPC endpoint (if enabled)"
  value       = var.enable_dynamodb_endpoint ? aws_vpc_endpoint.dynamodb[0].state : null
}
