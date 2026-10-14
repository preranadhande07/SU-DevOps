-- Conceptual schema; adapt to the selected database before implementation.
CREATE TABLE users (user_id INTEGER PRIMARY KEY, name VARCHAR(120) NOT NULL, email VARCHAR(255) NOT NULL UNIQUE, role VARCHAR(30) NOT NULL, status VARCHAR(20) NOT NULL DEFAULT 'active');
CREATE TABLE books (book_id INTEGER PRIMARY KEY, isbn VARCHAR(20) UNIQUE, title VARCHAR(255) NOT NULL, author VARCHAR(255) NOT NULL, category VARCHAR(120));
CREATE TABLE book_copies (copy_id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL REFERENCES books(book_id), shelf_location VARCHAR(120), status VARCHAR(20) NOT NULL DEFAULT 'available');
CREATE TABLE loans (loan_id INTEGER PRIMARY KEY, copy_id INTEGER NOT NULL REFERENCES book_copies(copy_id), user_id INTEGER NOT NULL REFERENCES users(user_id), issue_date DATE NOT NULL, due_date DATE NOT NULL, return_date DATE);
CREATE TABLE fines (fine_id INTEGER PRIMARY KEY, loan_id INTEGER NOT NULL REFERENCES loans(loan_id), amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0), status VARCHAR(20) NOT NULL DEFAULT 'unpaid');
