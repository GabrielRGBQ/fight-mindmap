import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base, get_db
from app.main import app
from app.model import models
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    # Here is what is run before the test has been run
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Here is what is run after the test has been run
    # Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "name": "nombre", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "gabri@gmail.com", "name": "gabriel", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def test_mindmaps(test_user, test_user2, session):
    mindmaps_data = [
        {
            "name": "Mindmap 1",
            "description": "Description of mindmap 1",
            "owner_id": test_user["id"],
        },
        {
            "name": "Mindmap 2",
            "description": "Description of mindmap 2",
            "owner_id": test_user["id"],
        },
        {
            "name": "Mindmap 3",
            "description": "Description of mindmap 3",
            "owner_id": test_user["id"],
        },
        {
            "name": "Mindmap 4",
            "description": "Description of mindmap 4",
            "owner_id": test_user2["id"],
        },
    ]

    def create_mindmap_model(mindmap):
        return models.Mindmap(**mindmap)

    mindmap_map = map(create_mindmap_model, mindmaps_data)
    mindmaps = list(mindmap_map)

    session.add_all(mindmaps)
    session.commit()

    mindmaps = session.query(models.Mindmap).all()
    return mindmaps