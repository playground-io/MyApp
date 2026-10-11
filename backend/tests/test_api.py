"""Integration tests for the task API using a temporary SQLite database."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import main
from app.database import get_db


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch):
    """Provide an isolated in-memory database for each test."""
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    test_sessions = sessionmaker(
        bind=test_engine,
        autoflush=False,
        expire_on_commit=False,
    )

    def override_get_db():
        with test_sessions() as session:
            yield session

    monkeypatch.setattr(main, "engine", test_engine)
    main.app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(main.app) as test_client:
            yield test_client
    finally:
        main.app.dependency_overrides.clear()
        test_engine.dispose()


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_task_lifecycle_and_completion_filter(client: TestClient) -> None:
    created = client.post(
        "/api/tasks",
        json={"title": "  Write tests  ", "description": "Keep the API reliable."},
    )

    assert created.status_code == 201
    task = created.json()
    assert task["title"] == "Write tests"
    assert task["completed"] is False

    updated = client.patch(f"/api/tasks/{task['id']}", json={"completed": True})
    assert updated.status_code == 200
    assert updated.json()["completed"] is True

    completed = client.get("/api/tasks", params={"completed": True})
    incomplete = client.get("/api/tasks", params={"completed": False})
    assert [item["id"] for item in completed.json()] == [task["id"]]
    assert incomplete.json() == []

    deleted = client.delete(f"/api/tasks/{task['id']}")
    assert deleted.status_code == 204
    assert client.get("/api/tasks").json() == []


def test_task_validation_and_missing_task(client: TestClient) -> None:
    invalid = client.post("/api/tasks", json={"title": "   "})
    missing = client.patch("/api/tasks/999", json={"completed": True})

    assert invalid.status_code == 422
    assert missing.status_code == 404
    assert missing.json() == {"detail": "Task not found"}
