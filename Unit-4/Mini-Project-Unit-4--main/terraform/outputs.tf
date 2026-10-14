output "ec2_public_ip" {
  description = "Public IP address of the provisioned EC2 instance"
  value       = aws_instance.app_server.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of the EC2 instance"
  value       = aws_instance.app_server.public_dns
}

output "ec2_instance_id" {
  description = "EC2 Instance ID"
  value       = aws_instance.app_server.id
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "Public Subnet ID"
  value       = aws_subnet.public_subnet.id
}

output "s3_backup_bucket" {
  description = "Name of the S3 backup bucket"
  value       = aws_s3_bucket.backup_bucket.id
}

output "app_url_http" {
  description = "Web Application URL via Nginx (Port 80)"
  value       = "http://${aws_instance.app_server.public_ip}"
}

output "direct_api_url" {
  description = "Direct Application API URL (Port 5000)"
  value       = "http://${aws_instance.app_server.public_ip}:5000"
}

output "ssh_command" {
  description = "Convenience SSH command to connect to EC2"
  value       = "ssh -i ~/.ssh/${var.key_name} ubuntu@${aws_instance.app_server.public_ip}"
}
