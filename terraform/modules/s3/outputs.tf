# S3 Module - Outputs
# Purpose: Export S3 bucket information

output "bucket_id" {
  description = "ID of the S3 bucket"
  value       = aws_s3_bucket.main.id
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.main.arn
}

output "bucket_regional_domain_name" {
  description = "Regional domain name of the bucket"
  value       = aws_s3_bucket.main.bucket_regional_domain_name
}

output "logging_bucket_id" {
  description = "ID of the logging bucket (if enabled)"
  value       = var.enable_logging ? aws_s3_bucket.logs[0].id : null
}
