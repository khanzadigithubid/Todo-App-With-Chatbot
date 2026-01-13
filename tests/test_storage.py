import pytest
from src.todo.storage import InMemoryStorage, TodoCRUDSubagent
from src.todo.models import Task
from datetime import datetime


class TestInMemoryStorage:
    """Test cases for the InMemoryStorage class."""
    
    def setup_method(self):
        """Set up a fresh storage instance for each test."""
        self.storage = InMemoryStorage()
    
    def test_add_task(self):
        """Test adding a task to storage."""
        task = Task(id="123", title="Test Task")
        result = self.storage.add_task(task)
        
        assert result == task
        assert self.storage._tasks["123"] == task
    
    def test_get_task_found(self):
        """Test retrieving an existing task."""
        task = Task(id="123", title="Test Task")
        self.storage.add_task(task)
        
        result = self.storage.get_task("123")
        
        assert result == task
    
    def test_get_task_not_found(self):
        """Test retrieving a non-existing task."""
        result = self.storage.get_task("nonexistent")
        
        assert result is None
    
    def test_get_all_tasks_empty(self):
        """Test retrieving all tasks when storage is empty."""
        result = self.storage.get_all_tasks()
        
        assert result == []
    
    def test_get_all_tasks_with_items(self):
        """Test retrieving all tasks when storage has items."""
        task1 = Task(id="123", title="Task 1")
        task2 = Task(id="456", title="Task 2")
        
        self.storage.add_task(task1)
        self.storage.add_task(task2)
        
        result = self.storage.get_all_tasks()
        
        assert len(result) == 2
        assert task1 in result
        assert task2 in result
    
    def test_update_task_found(self):
        """Test updating an existing task."""
        task = Task(id="123", title="Original Task")
        self.storage.add_task(task)
        
        result = self.storage.update_task("123", title="Updated Task")
        
        assert result.title == "Updated Task"
        assert self.storage._tasks["123"].title == "Updated Task"
    
    def test_update_task_not_found(self):
        """Test updating a non-existing task."""
        result = self.storage.update_task("nonexistent", title="New Title")
        
        assert result is None
    
    def test_update_task_with_invalid_attribute(self):
        """Test updating a task with an invalid attribute."""
        task = Task(id="123", title="Original Task")
        self.storage.add_task(task)
        
        # Update with an attribute that doesn't exist on the Task
        result = self.storage.update_task("123", nonexistent_attr="value")
        
        # Should not change the task since the attribute doesn't exist
        assert result.title == "Original Task"
    
    def test_delete_task_found(self):
        """Test deleting an existing task."""
        task = Task(id="123", title="Test Task")
        self.storage.add_task(task)
        
        result = self.storage.delete_task("123")
        
        assert result is True
        assert "123" not in self.storage._tasks
    
    def test_delete_task_not_found(self):
        """Test deleting a non-existing task."""
        result = self.storage.delete_task("nonexistent")
        
        assert result is False


class TestTodoCRUDSubagent:
    """Test cases for the TodoCRUDSubagent class."""
    
    def setup_method(self):
        """Set up a fresh subagent instance for each test."""
        self.subagent = TodoCRUDSubagent()
    
    def test_create_task(self):
        """Test creating a new task."""
        title = "Test Task"
        description = "Test Description"
        
        task = self.subagent.create_task(title, description)
        
        assert task.title == title
        assert task.description == description
        assert task.completed is False  # Default value
        assert task.id is not None
        assert task.created_at is not None
        assert isinstance(task.created_at, datetime)
    
    def test_create_task_without_description(self):
        """Test creating a task without description."""
        title = "Test Task"
        
        task = self.subagent.create_task(title)
        
        assert task.title == title
        assert task.description is None
        assert task.completed is False
    
    def test_get_task_found(self):
        """Test retrieving an existing task."""
        created_task = self.subagent.create_task("Test Task")
        task_id = created_task.id
        
        retrieved_task = self.subagent.get_task(task_id)
        
        assert retrieved_task.id == task_id
        assert retrieved_task.title == "Test Task"
    
    def test_get_task_not_found(self):
        """Test retrieving a non-existing task."""
        result = self.subagent.get_task("nonexistent")
        
        assert result is None
    
    def test_get_all_tasks_empty(self):
        """Test getting all tasks when none exist."""
        result = self.subagent.get_all_tasks()
        
        assert result == []
    
    def test_get_all_tasks_with_items(self):
        """Test getting all tasks when some exist."""
        task1 = self.subagent.create_task("Task 1")
        task2 = self.subagent.create_task("Task 2")
        
        result = self.subagent.get_all_tasks()
        
        assert len(result) == 2
        task_ids = [task.id for task in result]
        assert task1.id in task_ids
        assert task2.id in task_ids
    
    def test_update_task_title(self):
        """Test updating a task's title."""
        original_task = self.subagent.create_task("Original Task")
        task_id = original_task.id
        
        updated_task = self.subagent.update_task(task_id, title="Updated Task")
        
        assert updated_task.id == task_id
        assert updated_task.title == "Updated Task"
    
    def test_update_task_description(self):
        """Test updating a task's description."""
        original_task = self.subagent.create_task("Test Task", "Original Description")
        task_id = original_task.id
        
        updated_task = self.subagent.update_task(task_id, description="Updated Description")
        
        assert updated_task.id == task_id
        assert updated_task.description == "Updated Description"
    
    def test_update_task_both_fields(self):
        """Test updating both title and description."""
        original_task = self.subagent.create_task("Original Task", "Original Description")
        task_id = original_task.id
        
        updated_task = self.subagent.update_task(
            task_id, 
            title="Updated Task", 
            description="Updated Description"
        )
        
        assert updated_task.id == task_id
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated Description"
    
    def test_update_task_title_length_validation(self):
        """Test validation for title length during update."""
        original_task = self.subagent.create_task("Test Task")
        task_id = original_task.id
        
        # Try to update with a title that's too long
        long_title = "a" * 201
        with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
            self.subagent.update_task(task_id, title=long_title)
    
    def test_update_task_nonexistent(self):
        """Test updating a non-existing task."""
        result = self.subagent.update_task("nonexistent", title="New Title")
        
        assert result is None
    
    def test_delete_task_existing(self):
        """Test deleting an existing task."""
        task = self.subagent.create_task("Test Task")
        task_id = task.id
        
        result = self.subagent.delete_task(task_id)
        
        assert result is True
        assert self.subagent.get_task(task_id) is None
    
    def test_delete_task_nonexistent(self):
        """Test deleting a non-existing task."""
        result = self.subagent.delete_task("nonexistent")
        
        assert result is False
    
    def test_toggle_task_status_from_false_to_true(self):
        """Test toggling a task's status from False to True."""
        task = self.subagent.create_task("Test Task")
        task_id = task.id
        
        # Verify initial state
        initial_task = self.subagent.get_task(task_id)
        assert initial_task.completed is False
        
        # Toggle status
        toggled_task = self.subagent.toggle_task_status(task_id)
        
        assert toggled_task.completed is True
    
    def test_toggle_task_status_from_true_to_false(self):
        """Test toggling a task's status from True to False."""
        task = self.subagent.create_task("Test Task")
        task_id = task.id
        
        # First, set the task as completed
        self.subagent.update_task(task_id, completed=True)
        
        # Verify initial state is completed
        initial_task = self.subagent.get_task(task_id)
        assert initial_task.completed is True
        
        # Toggle status
        toggled_task = self.subagent.toggle_task_status(task_id)
        
        assert toggled_task.completed is False
    
    def test_toggle_task_status_nonexistent(self):
        """Test toggling status of a non-existing task."""
        result = self.subagent.toggle_task_status("nonexistent")
        
        assert result is None