# Functional Requirements Specification

- **FR-01 Authentication:** Support Admin, Librarian, Student, and Faculty roles with role-based access control.
- **FR-02 Catalog:** Create, view, update, and delete book records, including ISBN, author, category, and shelf location.
- **FR-03 Circulation:** Process checkouts and returns, calculate due dates, and update inventory.
- **FR-04 Fines:** Calculate overdue penalties using configured library rules and membership tier.
- **FR-05 Notifications:** Trigger due-date and overdue email alerts through a configured provider.
- **FR-06 Search:** Search catalog records using supported fields.
- **FR-07 Reports:** Allow authorized staff to view inventory and circulation summaries.

Acceptance checks include required-field validation, preventing issue of unavailable copies, correct availability updates on return, and server-side permission checks.
