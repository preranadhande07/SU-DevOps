# Random suffix for globally unique S3 bucket naming
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# AWS S3 Bucket for Database Backups, Logs, and Snapshots
resource "aws_s3_bucket" "backup_bucket" {
  bucket        = "${var.project_name}-backup-${random_id.bucket_suffix.hex}"
  force_destroy = false

  tags = {
    Name        = "${var.project_name}-backup"
    Description = "Nightly database dumps and audit logs backup store"
  }
}

# Enable S3 Versioning for disaster recovery
resource "aws_s3_bucket_versioning" "backup_versioning" {
  bucket = aws_s3_bucket.backup_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enforce Server-Side Encryption (AES-256)
resource "aws_s3_bucket_server_side_encryption_configuration" "backup_encryption" {
  bucket = aws_s3_bucket.backup_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Enforce Public Access Block (Private storage)
resource "aws_s3_bucket_public_access_block" "backup_public_block" {
  bucket = aws_s3_bucket.backup_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
