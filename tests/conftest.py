from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.model import models, schemas
import pytest
from fastapi.testclient import TestClient
from app.main import app

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
def populate_user(session):
    """
    Add a user to the testing database
    """
    user_data = {"email": "hello123@gmail.com", "name": "nombre", "password": "password123"}
    def create_user_model(user_data: schemas.UserCreate):
        return models.User(**user_data)
    new_user = create_user_model(user_data)
    session.add(new_user)
    session.commit()