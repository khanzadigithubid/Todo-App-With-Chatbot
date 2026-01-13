from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.endpoints import chat # Import only the chat router
# from app.middleware import JWTAuthMiddleware # Not needed for test_app
from app.tools.task_tools import add_task # Import add_task directly
import re # Import regex module
from uuid import UUID

# Create a test app instance
test_app = FastAPI()

# For simplicity and to bypass authentication as per spec, we will
# manually include the chat router into a clean FastAPI instance.
test_app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

client = TestClient(test_app)

# Helper function to create a task and get its ID
def create_task_and_get_id(task_title: str) -> str:
    # Directly call the add_task function from the tools, bypassing the chat endpoint for setup
    task = add_task(title=task_title)
    return str(task.id) # Return the UUID as a string

def test_chat_add_task():
    task_title = "buy milk"
    response = client.post("/api/chat", json={"message": f"add a task to {task_title}"})
    assert response.status_code == 200
    assert task_title in response.json()["response"].lower() # Check for title in lower case

def test_chat_list_tasks():
    # First add a task to ensure there's something to list
    task_title = "buy groceries"
    client.post("/api/chat", json={"message": f"add a task to {task_title}"})
    response = client.post("/api/chat", json={"message": "list all tasks"})
    assert response.status_code == 200
    assert task_title in response.json()["response"].lower()

def test_chat_complete_task():
    task_title = "task to complete"
    task_id = create_task_and_get_id(task_title)
    response = client.post("/api/chat", json={"message": f"complete task {task_id}"})
    assert response.status_code == 200
    assert task_id in response.json()["response"]
    assert "completada" in response.json()["response"].lower()

def test_chat_delete_task():
    task_title = "task to delete"
    task_id = create_task_and_get_id(task_title)
    response = client.post("/api/chat", json={"message": f"delete task {task_id}"})
    assert response.status_code == 200
    assert task_id in response.json()["response"]
    assert "eliminada" in response.json()["response"].lower()

def test_chat_update_task():
    task_title = "task to update"
    task_id = create_task_and_get_id(task_title)
    new_title = "new updated title"
    response = client.post("/api/chat", json={"message": f"update task {task_id} title to {new_title}"})
    assert response.status_code == 200
    assert "actualizada" in response.json()["response"].lower()
    assert new_title in response.json()["response"].lower()
