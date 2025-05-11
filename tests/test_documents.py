import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base
from app import models
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Test db connection (memory = temp)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Create the table before each test
Base.metadata.create_all(bind=engine)

# FastAPI dependency override


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_document():
    response = client.post(
        "/documents/",
        json={"title": "Test Doc", "content": "Testing content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Doc"
    assert data["content"] == "Testing content"
    assert data["approved"] is False
    assert "id" in data


def test_read_documents():
    response = client.get("/documents/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_update_document():
    # Add first document
    response = client.put(
        "/documents/1",
        json={"title": "Updated", "content": "Updated content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["content"] == "Updated content"


def test_delete_document():
    response = client.delete("/documents/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

    # Is it deleted
    response = client.get("/documents/1")
    assert response.status_code == 404
