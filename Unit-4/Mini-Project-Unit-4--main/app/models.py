import os
import sqlite3
from typing import List, Dict, Any, Optional

DEFAULT_DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DEFAULT_DB_DIR, exist_ok=True)
DEFAULT_DB_PATH = os.path.join(DEFAULT_DB_DIR, 'student_records.db')

def get_db_path() -> str:
    path = os.getenv('DATABASE_PATH', DEFAULT_DB_PATH)
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    return path

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path(), timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initialize database tables for students and academic marks."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            course_code TEXT NOT NULL,
            course_name TEXT NOT NULL,
            score REAL NOT NULL,
            max_score REAL NOT NULL DEFAULT 100.0,
            grade TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
        );
    """)
    conn.commit()

    # Pre-seed sample data if table is newly created and empty
    cursor.execute("SELECT COUNT(*) FROM students;")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_sample_data(conn)
    conn.close()

def seed_sample_data(conn: sqlite3.Connection) -> None:
    sample_students = [
        ("STU101", "Alice Johnson", "alice.johnson@university.edu", "Computer Science", 4),
        ("STU102", "Bob Smith", "bob.smith@university.edu", "Information Technology", 4),
        ("STU103", "Charlie Brown", "charlie.brown@university.edu", "Data Science", 3),
    ]
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO students (student_id, name, email, department, semester)
        VALUES (?, ?, ?, ?, ?)
    """, sample_students)

    sample_marks = [
        ("STU101", "CS401", "Cloud Computing & DevOps", 92.5, 100.0, "A+"),
        ("STU101", "CS402", "Distributed Systems", 88.0, 100.0, "A"),
        ("STU102", "CS401", "Cloud Computing & DevOps", 81.0, 100.0, "B+"),
        ("STU103", "DS301", "Applied Machine Learning", 95.0, 100.0, "A+"),
    ]
    cursor.executemany("""
        INSERT INTO marks (student_id, course_code, course_name, score, max_score, grade)
        VALUES (?, ?, ?, ?, ?, ?)
    """, sample_marks)
    conn.commit()

def calculate_grade(score: float, max_score: float = 100.0) -> str:
    percentage = (score / max_score) * 100.0
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    else:
        return "F"

def get_all_students() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name, email, department, semester, created_at FROM students ORDER BY student_id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_student_by_id(student_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name, email, department, semester, created_at FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_student(student_id: str, name: str, email: str, department: str, semester: int) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (student_id, name, email, department, semester)
        VALUES (?, ?, ?, ?, ?)
    """, (student_id, name, email, department, semester))
    conn.commit()
    conn.close()
    return get_student_by_id(student_id)

def get_all_marks() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.student_id, s.name as student_name, m.course_code, m.course_name, m.score, m.max_score, m.grade, m.created_at
        FROM marks m
        LEFT JOIN students s ON m.student_id = s.student_id
        ORDER BY m.id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_marks_for_student(student_id: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, student_id, course_code, course_name, score, max_score, grade, created_at
        FROM marks
        WHERE student_id = ?
        ORDER BY id DESC
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_marks(student_id: str, course_code: str, course_name: str, score: float, max_score: float = 100.0, grade: Optional[str] = None) -> Dict[str, Any]:
    if not grade:
        grade = calculate_grade(score, max_score)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO marks (student_id, course_code, course_name, score, max_score, grade)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (student_id, course_code, course_name, score, max_score, grade))
    mark_id = cursor.lastrowid
    conn.commit()
    cursor.execute("SELECT id, student_id, course_code, course_name, score, max_score, grade, created_at FROM marks WHERE id = ?", (mark_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)
