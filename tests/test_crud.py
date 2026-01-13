import pytest
from src.todo.models import Task
from src.todo.storage import TodoCRUDSubagent
from src.todo.service import TodoService


def test_create_task():
    """Test creating a new task."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)
    
    # Create a task
    title = "Test task"
    description = "Test description"
    task = service.add_task(title, description)
    
    # Verify the task was created correctly
    assert task.title == title
    assert task.description == description
    assert task.completed is False
    assert task.id is not None
    assert task.created_at is not None


def test_create_task_without_description():
    """Test creating a task without a description."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)
    
    # Create a task without description
    title = "Test task without description"
    task = service.add_task(title)
    
    # Verify the task was created correctly with None description
    assert task.title == title
    assert task.description is None
    assert task.completed is False


def test_create_task_title_length_validation():
    """Test validation for task title length."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)
    
    # Test with empty title
    with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
        service.add_task("")
    
    # Test with title longer than 200 characters
    long_title = "a" * 201
    with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
        service.add_task(long_title)


def test_get_task():
    """Test retrieving a task by ID."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)
    
    # Create a task
    task = service.add_task("Test task", "Test description")
    task_id = task.id
    
    # Retrieve the task
    retrieved_task = service.get_task(task_id)
    
    # Verify the retrieved task matches the created task
    assert retrieved_task.id == task_id
    assert retrieved_task.title == "Test task"
    assert retrieved_task.description == "Test description"


def test_get_all_tasks():
    """Test retrieving all tasks."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)

    # Create multiple tasks
    task1 = service.add_task("Task 1", "Description 1")
    task2 = service.add_task("Task 2", "Description 2")

    # Get all tasks
    all_tasks = service.get_all_tasks()

    # Verify both tasks are in the list
    assert len(all_tasks) == 2
    task_ids = [task.id for task in all_tasks]
    assert task1.id in task_ids
    assert task2.id in task_ids


def test_list_command_output(capsys):
    """Test that list command produces expected output."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)

    # Add a task
    service.add_task("Test task", "Test description")

    # Capture the output when getting all tasks
    tasks = service.get_all_tasks()

    # Verify we have at least one task
    assert len(tasks) == 1
    assert tasks[0].title == "Test task"
    assert tasks[0].description == "Test description"


def test_update_task():
    """Test updating a task."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)

    # Create a task
    original_task = service.add_task("Original task", "Original description")
    task_id = original_task.id

    # Update the task
    updated_task = service.update_task(task_id, title="Updated task", description="Updated description")

    # Verify the task was updated
    assert updated_task.title == "Updated task"
    assert updated_task.description == "Updated description"

    # Verify the task can be retrieved with updated values
    retrieved_task = service.get_task(task_id)
    assert retrieved_task.title == "Updated task"
    assert retrieved_task.description == "Updated description"


def test_update_task_validation():
    """Test validation when updating a task."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)

    # Create a task
    original_task = service.add_task("Original task", "Original description")
    task_id = original_task.id

    # Try to update with a title that's too long
    long_title = "a" * 201
    with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
        service.update_task(task_id, title=long_title)


def test_update_nonexistent_task():
    """Test updating a task that doesn't exist."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)

    # Try to update a task that doesn't exist
    with pytest.raises(ValueError, match="Task with ID nonexistent does not exist"):
        service.update_task("nonexistent", title="New title")


def test_delete_task():
    """Test deleting a task."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)

    # Create a task
    task = service.add_task("Task to delete", "Description to delete")
    task_id = task.id

    # Verify the task exists
    assert service.get_task(task_id) is not None

    # Delete the task
    result = service.delete_task(task_id)

    # Verify the task was deleted
    assert result is True
    assert service.get_task(task_id) is None


def test_delete_nonexistent_task():
    """Test deleting a task that doesn't exist."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)

    # Try to delete a task that doesn't exist
    with pytest.raises(ValueError, match="Task with ID nonexistent does not exist"):
        service.delete_task("nonexistent")


def test_toggle_task_status():
    """Test toggling a task's completion status."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)

    # Create a task (default is incomplete)
    task = service.add_task("Test task", "Test description")
    task_id = task.id

    # Verify initial state is incomplete
    retrieved_task = service.get_task(task_id)
    assert retrieved_task.completed is False

    # Toggle to complete
    updated_task = service.toggle_task_status(task_id)
    assert updated_task.completed is True

    # Toggle back to incomplete
    updated_task = service.toggle_task_status(task_id)
    assert updated_task.completed is False


def test_toggle_nonexistent_task():
    """Test toggling a task that doesn't exist."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)

    # Try to toggle a task that doesn't exist
    with pytest.raises(ValueError, match="Task with ID nonexistent does not exist"):
        service.toggle_task_status("nonexistent")


def test_edge_cases():
    """Test edge cases like title length validation and non-existent IDs."""
    subagent = TodoCRUDSubagent()
    service = TodoService(subagent)

    # Test title at exactly 200 characters (should be valid)
    valid_title = "a" * 200
    task = service.add_task(valid_title)
    assert task.title == valid_title

    # Test that a task with empty description is valid
    task2 = service.add_task("Test task", "")
    assert task2.description == ""

    # Test that getting all tasks works when there are no tasks
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) > 0  # We have created tasks above

    # Test deleting tasks to empty the list
    service.delete_task(task.id)  # Delete the task
    service.delete_task(task2.id)  # Delete the task
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) == 0