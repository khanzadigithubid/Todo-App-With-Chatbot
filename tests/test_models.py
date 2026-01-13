import pytest
from src.todo.models import Task
from datetime import datetime


class TestTaskModel:
    """Test cases for the Task dataclass."""
    
    def test_task_creation_with_required_fields(self):
        """Test creating a task with required fields only."""
        task_id = "123e4567-e89b-12d3-a456-426614174000"
        title = "Test Task"
        
        task = Task(id=task_id, title=title)
        
        assert task.id == task_id
        assert task.title == title
        assert task.description is None
        assert task.completed is False
        assert task.created_at is not None
        assert isinstance(task.created_at, datetime)
    
    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields."""
        task_id = "123e4567-e89b-12d3-a456-426614174000"
        title = "Test Task"
        description = "Test Description"
        completed = True
        created_at = datetime.now()
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=completed,
            created_at=created_at
        )
        
        assert task.id == task_id
        assert task.title == title
        assert task.description == description
        assert task.completed == completed
        assert task.created_at == created_at
    
    def test_task_creation_sets_current_datetime_if_not_provided(self):
        """Test that created_at is set to current datetime if not provided."""
        before_creation = datetime.now()
        task = Task(id="123e4567-e89b-12d3-a456-426614174000", title="Test Task")
        after_creation = datetime.now()
        
        assert task.created_at >= before_creation
        assert task.created_at <= after_creation
    
    def test_task_str_representation_completed(self):
        """Test string representation of a completed task."""
        task = Task(
            id="123e4567-e89b-12d3-a456-426614174000",
            title="Test Task",
            completed=True
        )
        
        assert str(task) == "[✓] Test Task"
    
    def test_task_str_representation_pending(self):
        """Test string representation of a pending task."""
        task = Task(
            id="123e4567-e89b-12d3-a456-426614174000",
            title="Test Task",
            completed=False
        )
        
        assert str(task) == "[○] Test Task"
    
    def test_task_with_description(self):
        """Test task creation with description."""
        task = Task(
            id="123e4567-e89b-12d3-a456-426614174000",
            title="Test Task",
            description="Test Description"
        )
        
        assert task.description == "Test Description"