# Mini-Project-Unit-4- : Student Record and Academic Management Platform

An enterprise cloud-native application automating student record management, course mark processing, and infrastructure deployment on AWS using Terraform and Ansible.

## 📁 Repository Structure
```
├── app/                      # Application Layer (Flask, Gunicorn, SQLite, Dockerfile)
│   ├── app.py                # REST API implementation
│   ├── models.py             # SQLite thread-safe database models
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile            # Container definition (Port 5000)
│   ├── test_endpoints.py     # Automated smoke test suite (Gate 4)
│   └── tests/                # Unit test files
├── terraform/                # Infrastructure as Code (AWS Cloud Fabric)
│   ├── main.tf               # VPC (10.1.0.0/16), Subnets, IGW, Route Tables
│   ├── ec2.tf                # Ubuntu 22.04 LTS t2.micro with 20GB gp3 EBS
│   ├── security_groups.tf    # Firewall rules (22, 80, 5000, 8080)
│   ├── s3.tf                 # S3 backup bucket (AES-256 encrypted, versioned)
│   ├── variables.tf          # Configurable variables
│   ├── outputs.tf            # IP, DNS, URLs, SSH command
│   └── terraform.tfvars.example
├── ansible/                  # Configuration Management (Server Automation)
│   ├── ansible.cfg           # OpenSSH and execution settings
│   ├── inventory.ini         # Target server inventory
│   ├── site.yml              # Master orchestration playbook
│   └── roles/                # Modular reusable roles
│       ├── common/           # System packages and firewall
│       ├── docker/           # Docker CE and containerd engine
│       ├── nginx/            # Reverse proxy (Port 80 -> Port 5000)
│       └── student_app/      # Docker container, persistent volume & validation
└── docs/                     # Architectural documentation
    └── TECHNICAL_REPORT.md   # Complete technical report and validation gates
```

## 🚀 Quick Start: Local Testing via Docker
```bash
# In Windows PowerShell or Ubuntu WSL:
cd app
docker build -t student-record-app:v1.0.0 .
docker run -d --name student-record-app -p 5000:5000 student-record-app:v1.0.0

# Run automated smoke test:
python test_endpoints.py http://localhost:5000
```

## ☁️ Cloud Infrastructure & Deployment
Follow the step-by-step guidance in [docs/TECHNICAL_REPORT.md](file:///c:/Users/darsh/OneDrive/Desktop/Mini%20Project%20Unit%204/docs/TECHNICAL_REPORT.md).
