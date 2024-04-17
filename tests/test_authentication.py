from app.model import schemas
from jose import jwt 
import pytest
from app.config import settings

def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    user_id = payload.get("user_id")
    assert user_id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 404),
        ("hello123@gmail.com", "wrongpassword123", 403),
        ("wrongemail@gmail.com", "wrongpassword123", 403),
        (None, "password123", 422),
        ("hello123@gmail.com", None, 422),
    ],
)
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code