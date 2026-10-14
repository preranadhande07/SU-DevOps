# System Architecture Concept

## Components
- UI: Login, Catalog Search, Checkout Dashboard, Admin Reports.
- API/business modules: Authentication, Books, Circulation, Fines, Notifications, Reports.
- Database: Users, Roles, Books, Copies, Loans, Fines, Audit Events.
- Background jobs: Due-date reminders and overdue fine processing.
- Delivery/operations: CI/CD, Docker, Kubernetes, Terraform, Ansible, Prometheus, Grafana.

Keep book titles separate from physical copies; use foreign keys and transactions for issue/return consistency. Enforce authorization on the server. This is a concept, not a claim that all components are implemented.
