import requests

URL = 'http://localhost:8000/users/'

def test_create_user():
    data = {"name": "string",
            "email": "user@example.com"}
    response = requests.post(url=URL, json=data)
    assert response.status_code == 200
