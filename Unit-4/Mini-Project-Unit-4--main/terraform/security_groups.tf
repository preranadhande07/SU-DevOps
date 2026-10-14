# Security Group acting as virtual firewall
resource "aws_security_group" "web_sg" {
  name        = "${var.project_name}-web-sg"
  description = "Allow inbound SSH, HTTP (80), and App API traffic (5000/8080)"
  vpc_id      = aws_vpc.main.id

  # Port 22: SSH for Ansible automation & MobaXterm
  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 80: HTTP for Nginx Reverse Proxy
  ingress {
    description = "Public HTTP web traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 5000: Direct Flask/Gunicorn container access
  ingress {
    description = "Direct Flask App Port"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 8080: Alternate app port (per Unit 4 Table 9.1 specification)
  ingress {
    description = "Alternate App Port"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Unrestricted outbound egress
  egress {
    description = "Allow all outbound traffic for APT updates and Docker image pulls"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-web-sg"
  }
}
