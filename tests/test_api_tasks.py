import sys
sys.path.append(".") # Add project root to sys.path

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from backend.app.main import app
from backend.app.database import get_session
import pytest

# Setup in-memory SQLite for testing
engine = create_engine("sqlite:///./test.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="session")
def session_fixture():
    create_db_and_tables()
    with Session(engine) as session:
        yield session
    drop_db_and_tables()

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_user(client: TestClient):
    response = client.post(
        "/api/users/",
        json={"email": "test@example.com", "name": "Test User"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data
    assert "created_at" in data

def test_create_and_get_tasks_for_user(client: TestClient):
    # Create user 1
    response = client.post(
        "/api/users/",
        json={"email": "user1@example.com", "name": "User One"},
    )
    user1_id = response.json()["id"]

    # Create task for user 1
    response = client.post(
        f"/api/{user1_id}/tasks/",
        json={"title": "User1 Task 1", "description": "Description for User1 Task 1"},
    )
    assert response.status_code == 200
    task1_user1 = response.json()
    assert task1_user1["title"] == "User1 Task 1"
    assert task1_user1["user_id"] == user1_id

    # Get tasks for user 1
    response = client.get(f"/api/{user1_id}/tasks/")
    assert response.status_code == 200
    tasks_user1 = response.json()
    assert len(tasks_user1) == 1
    assert tasks_user1[0]["title"] == "User1 Task 1"

    # Create user 2
    response = client.post(
        "/api/users/",
        json={"email": "user2@example.com", "name": "User Two"},
    )
    user2_id = response.json()["id"]

    # Create task for user 2
    response = client.post(
        f"/api/{user2_id}/tasks/",
        json={"title": "User2 Task 1", "description": "Description for User2 Task 1"},
    )
    assert response.status_code == 200
    task1_user2 = response.json()
    assert task1_user2["title"] == "User2 Task 1"
    assert task1_user2["user_id"] == user2_id

    # Get tasks for user 2
    response = client.get(f"/api/{user2_id}/tasks/")
    assert response.status_code == 200
    tasks_user2 = response.json()
    assert len(tasks_user2) == 1
    assert tasks_user2[0]["title"] == "User2 Task 1"

    # Verify user 1 cannot see user 2's tasks
    response = client.get(f"/api/{user1_id}/tasks/")
    assert response.status_code == 200
    tasks_user1_again = response.json()
    assert len(tasks_user1_again) == 1
    assert tasks_user1_again[0]["title"] == "User1 Task 1"
    assert tasks_user1_again[0]["user_id"] == user1_id
    assert tasks_user1_again[0]["title"] != "User2 Task 1"

def test_update_task_for_user(client: TestClient):
    # Create user
    response = client.post(
        "/api/users/",
        json={"email": "updateuser@example.com", "name": "Update User"},
    )
    user_id = response.json()["id"]

    # Create task
    response = client.post(
        f"/api/{user_id}/tasks/",
        json={"title": "Original Title", "description": "Original Description"},
    )
    task_id = response.json()["id"]

    # Update task
    response = client.put(
        f"/api/{user_id}/tasks/{task_id}",
        json={"title": "Updated Title", "description": "Updated Description", "completed": True},
    )
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Updated Title"
    assert updated_task["description"] == "Updated Description"
    assert updated_task["completed"] is True
    assert updated_task["id"] == task_id
    assert updated_task["user_id"] == user_id

    # Try to update a task with a wrong user ID
    response = client.put(
        f"/api/some_other_id/tasks/{task_id}",
        json={"title": "Malicious Update", "description": "Malicious Description", "completed": True},
    )
    assert response.status_code == 422

def test_delete_task_for_user(client: TestClient):
    # Create user
    response = client.post(
        "/api/users/",
        json={"email": "deleteuser@example.com", "name": "Delete User"},
    )
    user_id = response.json()["id"]

    # Create task
    response = client.post(
        f"/api/{user_id}/tasks/",
        json={"title": "Task to Delete", "description": "Description to Delete"},
    )
    task_id = response.json()["id"]

    # Delete task
    response = client.delete(f"/api/{user_id}/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

    # Verify task is deleted
    response = client.get(f"/api/{user_id}/tasks/{task_id}")
    assert response.status_code == 404 # Not Found

    # Try to delete task with a wrong user ID
    response = client.delete(f"/api/some_other_id/tasks/{task_id}")
    assert response.status_code == 422
