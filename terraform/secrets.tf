# Secrets Manager Secret for SFTP Credentials
resource "aws_secretsmanager_secret" "sftp_credentials" {
  name_prefix             = "${var.project_name}-${var.environment}-sftp-"
  description             = "SFTP credentials for file transfer"
  recovery_window_in_days = 7

  tags = {
    Name = "${var.project_name}-${var.environment}-sftp-credentials"
  }
}

# Secret version (template - must be updated with actual values)
resource "aws_secretsmanager_secret_version" "sftp_credentials" {
  secret_id = aws_secretsmanager_secret.sftp_credentials.id

  secret_string = jsonencode({
    username    = var.sftp_username
    private_key = ""
    host        = var.sftp_host
    port        = var.sftp_port
  })

  lifecycle {
    ignore_changes = [secret_string]
  }
}
