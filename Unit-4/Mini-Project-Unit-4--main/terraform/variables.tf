variable "aws_region" {
  description = "AWS region for provisioning resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name tag prefix"
  type        = string
  default     = "student-academic-platform"
}

variable "environment" {
  description = "Deployment lifecycle environment"
  type        = string
  default     = "production"
}

variable "vpc_cidr" {
  description = "CIDR block for Student Record Platform VPC (per Unit 4 Section 9 specification)"
  type        = string
  default     = "10.1.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public compute subnet"
  type        = string
  default     = "10.1.1.0/24"
}

variable "instance_type" {
  description = "EC2 compute instance type (AWS Free Tier eligible)"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "AWS EC2 Key Pair name imported in Chapter 2"
  type        = string
  default     = "student-aws-key"
}

variable "root_volume_size" {
  description = "EBS Root volume size in GiB"
  type        = number
  default     = 20
}
