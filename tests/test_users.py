import requests
from fastapi.testclient import TestClient
# from app.main import app

URL = 'http://localhost:8000/users/'

def test_create_user():
    data = {"name": "string",
            "email": "user@example.com"}
    response = requests.post(url=URL, json=data)
    assert response.status_code == 200

# client = TestClient(app)

# def test_create_user_testclient():
#     data = {"name": "string", "email": "user@example.com"}
#     response = client.post("/users/", json=data)
#     assert response.status_code == 200
