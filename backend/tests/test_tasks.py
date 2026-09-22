import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from database import Base, get_db
import main

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


main.app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(main.app)


def create_sample_task():
    return client.post("/api/tasks", json={"title": "sample"})


def test_create_task_title_only():
    response = create_sample_task()
    assert response.status_code == 201


def test_list_tasks_excludes_description():
    create_sample_task()
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert "description" not in response.json()[0]


def test_get_task_includes_description():
    created = create_sample_task().json()
    response = client.get(f"/api/tasks/{created['id']}")
    assert response.status_code == 200
    assert "description" in response.json()


def test_update_task_all_fields():
    created = create_sample_task().json()
    response = client.put(
        f"/api/tasks/{created['id']}",
        json={"title": "updated", "description": "d", "status": "done", "due_at": None},
    )
    assert response.status_code == 200


def test_delete_task():
    created = create_sample_task().json()
    response = client.delete(f"/api/tasks/{created['id']}")
    assert response.status_code == 204


def test_create_missing_title():
    response = client.post("/api/tasks", json={})
    assert response.status_code == 400


def test_create_invalid_status():
    response = client.post("/api/tasks", json={"title": "t", "status": "bogus"})
    assert response.status_code == 400


def test_create_invalid_due_at_format():
    response = client.post("/api/tasks", json={"title": "t", "due_at": "not-a-date"})
    assert response.status_code == 400


def test_get_nonexistent_task():
    response = client.get("/api/tasks/999999")
    assert response.status_code == 404


def test_create_with_unknown_field():
    response = client.post("/api/tasks", json={"title": "t", "extra_field": "x"})
    assert response.status_code == 422
