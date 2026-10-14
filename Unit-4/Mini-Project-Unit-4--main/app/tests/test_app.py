import os
import tempfile
import pytest

# Configure a temporary database path before importing app/models
@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.environ["DATABASE_PATH"] = db_path

    # Reload/import app after setting env var
    from app import app
    from models import init_db

    with app.app_context():
        init_db()

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

    os.close(db_fd)
    if os.path.exists(db_path):
        os.remove(db_path)

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "UP"
    assert data["database"] == "UP"
    assert "timestamp" in data

def test_list_students(client):
    response = client.get("/api/students")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)
    # At least sample data exists
    assert data["count"] >= 3

def test_create_and_get_student(client):
    new_student = {
        "student_id": "STU999",
        "name": "David Miller",
        "email": "david.miller@university.edu",
        "department": "Cybersecurity",
        "semester": 5
    }
    # Create student
    res = client.post("/api/students", json=new_student)
    assert res.status_code == 201
    created = res.get_json()
    assert created["status"] == "success"
    assert created["data"]["student_id"] == "STU999"

    # Fetch created student
    fetch_res = client.get("/api/students/STU999")
    assert fetch_res.status_code == 200
    fetch_data = fetch_res.get_json()
    assert fetch_data["student"]["name"] == "David Miller"

def test_create_student_duplicate(client):
    duplicate = {
        "student_id": "STU101",  # already in seed
        "name": "Duplicate User",
        "email": "dup@university.edu",
        "department": "CS"
    }
    res = client.post("/api/students", json=duplicate)
    assert res.status_code == 409

def test_submit_and_list_marks(client):
    mark_payload = {
        "student_id": "STU101",
        "course_code": "CS403",
        "course_name": "DevOps & SRE",
        "score": 96.0,
        "max_score": 100.0
    }
    res = client.post("/api/marks", json=mark_payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["status"] == "success"
    assert data["data"]["grade"] == "A+"

    # List marks
    list_res = client.get("/api/marks")
    assert list_res.status_code == 200
    list_data = list_res.get_json()
    assert list_data["count"] >= 1

def test_submit_marks_invalid_student(client):
    mark_payload = {
        "student_id": "NONEXISTENT",
        "course_code": "CS101",
        "course_name": "Intro to CS",
        "score": 85.0
    }
    res = client.post("/api/marks", json=mark_payload)
    assert res.status_code == 404
