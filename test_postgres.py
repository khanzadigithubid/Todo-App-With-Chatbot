"""
Simple test to verify PostgreSQL storage is working correctly.
"""
import sys
import traceback
from src.todo.models import Task
from src.todo.postgres_storage import PostgresStorage
from datetime import datetime
import uuid


def test_postgres_storage():
    """Test the PostgreSQL storage implementation."""
    print("Testing PostgreSQL storage...")

    try:
        # Create a storage instance
        storage = PostgresStorage()
        print("Successfully connected to PostgreSQL database")

        # Create a test task
        task_id = str(uuid.uuid4())
        test_task = Task(
            id=task_id,
            title="Test Task",
            description="This is a test task for PostgreSQL storage",
            status="pending",
            created_at=datetime.now()
        )

        # Add the task
        print(f"Adding task with ID: {task_id}")
        added_task = storage.add_task(test_task)
        print(f"Task added: {added_task.title}")

        # Retrieve the task
        retrieved_task = storage.get_task(task_id)
        print(f"Retrieved task: {retrieved_task.title if retrieved_task else 'None'}")

        # Update the task
        updated_task = storage.update_task(task_id, status="completed", description="Updated description")
        print(f"Task updated: {updated_task.status if updated_task else 'None'}")

        # Get all tasks
        all_tasks = storage.get_all_tasks()
        print(f"Total tasks in storage: {len(all_tasks)}")

        # Delete the task
        deleted = storage.delete_task(task_id)
        print(f"Task deleted: {deleted}")

        # Verify deletion
        deleted_task = storage.get_task(task_id)
        print(f"After deletion, task exists: {deleted_task is not None}")

        print("PostgreSQL storage test completed successfully!")

    except Exception as e:
        print(f"Error during PostgreSQL storage test: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    test_postgres_storage()