# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.project_name}-${var.environment}-file-transfer"
  retention_in_days = 7

  tags = {
    Name = "${var.project_name}-${var.environment}-lambda-logs"
  }
}

# Lambda Function
resource "aws_lambda_function" "file_transfer" {
  filename         = "${path.module}/../lambda_function.zip"
  function_name    = "${var.project_name}-${var.environment}-file-transfer"
  role             = aws_iam_role.lambda.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("${path.module}/../lambda_function.zip")
  runtime          = "python3.11"
  timeout          = 300
  memory_size      = 512

  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.lambda.id]
  }

  environment {
    variables = {
      S3_BUCKET_NAME       = aws_s3_bucket.file_transfer.id
      SFTP_SECRET_ARN      = aws_secretsmanager_secret.sftp_credentials.arn
      SFTP_REMOTE_PATH     = var.sftp_remote_path
      LOG_LEVEL            = "INFO"
    }
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-file-transfer"
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda,
    aws_iam_role_policy_attachment.lambda_s3,
    aws_iam_role_policy_attachment.lambda_logs,
    aws_iam_role_policy_attachment.lambda_vpc,
    aws_iam_role_policy_attachment.lambda_secrets
  ]
}

# EventBridge Rule for Scheduled Execution (Optional)
resource "aws_cloudwatch_event_rule" "file_transfer_schedule" {
  name                = "${var.project_name}-${var.environment}-file-transfer-schedule"
  description         = "Trigger file transfer Lambda function on schedule"
  schedule_expression = "rate(1 hour)"
  is_enabled          = false

  tags = {
    Name = "${var.project_name}-${var.environment}-schedule-rule"
  }
}

# EventBridge Target
resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.file_transfer_schedule.name
  target_id = "lambda"
  arn       = aws_lambda_function.file_transfer.arn
}

# Lambda Permission for EventBridge
resource "aws_lambda_permission" "eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.file_transfer.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.file_transfer_schedule.arn
}
