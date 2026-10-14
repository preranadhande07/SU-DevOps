#!/usr/bin/env python3
"""
Automated smoke test script for Student Record & Academic Management Platform.
Can be executed against localhost or a remote EC2 public IP.
Usage:
    python test_endpoints.py http://localhost:5000
    python test_endpoints.py http://<EC2_PUBLIC_IP>
"""

import sys
import json
import urllib.request
import urllib.error

def send_request(url, method="GET", data=None):
    headers = {"Content-Type": "application/json"}
    encoded_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"error": body}
    except Exception as e:
        return 0, {"error": str(e)}

def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    base_url = base_url.rstrip("/")
    print(f"==================================================")
    print(f"RUNNING API SMOKE TESTS AGAINST: {base_url}")
    print(f"==================================================")

    # 1. Health check
    print("\n[1] Testing GET /api/health ...")
    status, res = send_request(f"{base_url}/api/health")
    print(f"Status Code: {status}")
    print(f"Response: {json.dumps(res, indent=2)}")
    assert status == 200, f"Expected 200, got {status}"
    assert res.get("status") == "UP", f"Expected UP, got {res.get('status')}"

    # 2. List students
    print("\n[2] Testing GET /api/students ...")
    status, res = send_request(f"{base_url}/api/students")
    print(f"Status Code: {status}")
    print(f"Response Count: {res.get('count')}")
    assert status == 200, f"Expected 200, got {status}"

    # 3. Register student
    test_student_id = "STU888"
    print(f"\n[3] Testing POST /api/students (Creating {test_student_id}) ...")
    payload = {
        "student_id": test_student_id,
        "name": "Sarah Connor",
        "email": "sarah.connor@university.edu",
        "department": "Cybernetics",
        "semester": 4
    }
    status, res = send_request(f"{base_url}/api/students", method="POST", data=payload)
    print(f"Status Code: {status}")
    print(f"Response: {json.dumps(res, indent=2)}")
    assert status in (201, 409), f"Unexpected status: {status}"

    # 4. Submit marks
    print(f"\n[4] Testing POST /api/marks (Submitting marks for {test_student_id}) ...")
    mark_payload = {
        "student_id": test_student_id,
        "course_code": "CS401",
        "course_name": "Cloud Computing & DevOps",
        "score": 98.0,
        "max_score": 100.0
    }
    status, res = send_request(f"{base_url}/api/marks", method="POST", data=mark_payload)
    print(f"Status Code: {status}")
    print(f"Response: {json.dumps(res, indent=2)}")
    assert status == 201, f"Expected 201, got {status}"

    # 5. List all marks
    print("\n[5] Testing GET /api/marks ...")
    status, res = send_request(f"{base_url}/api/marks")
    print(f"Status Code: {status}")
    print(f"Total Marks Records: {res.get('count')}")
    assert status == 200, f"Expected 200, got {status}"

    # 6. Get single student profile
    print(f"\n[6] Testing GET /api/students/{test_student_id} ...")
    status, res = send_request(f"{base_url}/api/students/{test_student_id}")
    print(f"Status Code: {status}")
    print(f"Response: {json.dumps(res, indent=2)}")
    assert status == 200, f"Expected 200, got {status}"

    print("\n==================================================")
    print("ALL API SMOKE TESTS PASSED SUCCESSFULLY! (GATE 4)")
    print("==================================================")

if __name__ == "__main__":
    main()
