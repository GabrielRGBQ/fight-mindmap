from app.model import schemas
from fastapi import status

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "name": "nombre", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_create_user_duplicate(client, populate_user):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "name": "nombre", "password": "password123"}
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST