import datetime
import os
import sqlite3
from flask import Flask, jsonify, request
from models import (
    init_db,
    get_all_students,
    get_student_by_id,
    create_student,
    get_all_marks,
    get_marks_for_student,
    add_marks,
    get_db_path,
)

app = Flask(__name__)

# Ensure tables are initialized on startup
with app.app_context():
    init_db()

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Enterprise Student Record and Academic Management Platform",
        "status": "UP",
        "version": "1.0.0",
        "documentation": {
            "health_check": "GET /api/health",
            "list_students": "GET /api/students",
            "create_student": "POST /api/students",
            "student_profile": "GET /api/students/<student_id>",
            "list_marks": "GET /api/marks",
            "submit_marks": "POST /api/marks",
            "student_marks": "GET /api/marks/student/<student_id>"
        }
    }), 200

@app.route("/api/health", methods=["GET"])
def health_check():
    db_status = "UP"
    try:
        conn = sqlite3.connect(get_db_path(), timeout=2.0)
        conn.execute("SELECT 1;").fetchone()
        conn.close()
    except Exception as e:
        db_status = f"DOWN: {str(e)}"

    return jsonify({
        "status": "UP" if db_status == "UP" else "DEGRADED",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "database": db_status,
        "service": "student-academic-platform",
        "version": "1.0.0"
    }), 200 if db_status == "UP" else 500

@app.route("/api/students", methods=["GET"])
def list_students():
    try:
        students = get_all_students()
        return jsonify({
            "status": "success",
            "count": len(students),
            "data": students
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/students", methods=["POST"])
def register_student():
    data = request.get_json(force=True, silent=True) or {}
    required_fields = ["student_id", "name", "email", "department"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "status": "error",
                "message": f"Field '{field}' is required."
            }), 400

    student_id = str(data["student_id"]).strip().upper()
    name = str(data["name"]).strip()
    email = str(data["email"]).strip().lower()
    department = str(data["department"]).strip()
    semester = int(data.get("semester", 1))

    existing = get_student_by_id(student_id)
    if existing:
        return jsonify({
            "status": "error",
            "message": f"Student with ID '{student_id}' already exists."
        }), 409

    try:
        new_student = create_student(student_id, name, email, department, semester)
        return jsonify({
            "status": "success",
            "message": "Student created successfully.",
            "data": new_student
        }), 201
    except sqlite3.IntegrityError as e:
        return jsonify({"status": "error", "message": f"Integrity error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/students/<student_id>", methods=["GET"])
def get_student(student_id):
    student = get_student_by_id(student_id.upper())
    if not student:
        return jsonify({"status": "error", "message": "Student not found."}), 404

    marks = get_marks_for_student(student_id.upper())
    return jsonify({
        "status": "success",
        "student": student,
        "marks": marks
    }), 200

@app.route("/api/marks", methods=["GET"])
def list_marks():
    try:
        marks = get_all_marks()
        return jsonify({
            "status": "success",
            "count": len(marks),
            "data": marks
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/marks", methods=["POST"])
def submit_marks():
    data = request.get_json(force=True, silent=True) or {}
    required_fields = ["student_id", "course_code", "course_name", "score"]
    for field in required_fields:
        if data.get(field) is None:
            return jsonify({
                "status": "error",
                "message": f"Field '{field}' is required."
            }), 400

    student_id = str(data["student_id"]).strip().upper()
    student = get_student_by_id(student_id)
    if not student:
        return jsonify({
            "status": "error",
            "message": f"Cannot submit marks: Student ID '{student_id}' not found."
        }), 404

    try:
        score = float(data["score"])
        max_score = float(data.get("max_score", 100.0))
        if score < 0 or score > max_score:
            return jsonify({
                "status": "error",
                "message": f"Score must be between 0 and {max_score}."
            }), 400
    except ValueError:
        return jsonify({"status": "error", "message": "Score must be a valid numeric value."}), 400

    course_code = str(data["course_code"]).strip().upper()
    course_name = str(data["course_name"]).strip()
    grade = data.get("grade")

    try:
        new_mark = add_marks(student_id, course_code, course_name, score, max_score, grade)
        return jsonify({
            "status": "success",
            "message": "Marks recorded successfully.",
            "data": new_mark
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/marks/student/<student_id>", methods=["GET"])
def student_marks_endpoint(student_id):
    student = get_student_by_id(student_id.upper())
    if not student:
        return jsonify({"status": "error", "message": "Student not found."}), 404
    marks = get_marks_for_student(student_id.upper())
    return jsonify({
        "status": "success",
        "student_id": student_id.upper(),
        "count": len(marks),
        "data": marks
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
