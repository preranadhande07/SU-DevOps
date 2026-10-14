# Non-Functional Requirements Specification

- **Security:** Hash passwords with bcrypt/Argon2, enforce authorization, use HTTPS in deployment, and store secrets safely.
- **Performance:** Assignment target: catalog search API under 500 ms under concurrent load; verify with load tests.
- **Availability/scalability:** Assignment target: 99.9% uptime; containerization and horizontal scaling may support this but do not guarantee it.
- **Maintainability:** Modular code, documented interfaces, automated tests, and separated configuration.
- **Privacy/recovery/observability:** Limit access to personal borrowing data, plan backups, and monitor service health.
