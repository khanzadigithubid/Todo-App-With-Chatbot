import pytest
from src.todo.service import TodoService
from src.todo.storage import TodoCRUDSubagent
from src.todo.models import Task


class TestTodoService:
    """Test cases for the TodoService class."""
    
    def setup_method(self):
        """Set up a fresh service instance for each test."""
        self.subagent = TodoCRUDSubagent()
        self.service = TodoService(self.subagent)
    
    def test_add_task_success(self):
        """Test successfully adding a task."""
        title = "Test Task"
        description = "Test Description"
        
        task = self.service.add_task(title, description)
        
        assert task.title == title
        assert task.description == description
        assert task.completed is False
        assert task.id is not None
        assert task.created_at is not None
    
    def test_add_task_without_description(self):
        """Test adding a task without description."""
        title = "Test Task"
        
        task = self.service.add_task(title)
        
        assert task.title == title
        assert task.description is None
    
    def test_add_task_empty_title_validation(self):
        """Test validation for empty title during task creation."""
        with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
            self.service.add_task("")
    
    def test_add_task_short_title_validation(self):
        """Test validation for title that's too short."""
        with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
            self.service.add_task("")  # This is 0 chars, which should fail
    
    def test_add_task_long_title_validation(self):
        """Test validation for title that's too long."""
        long_title = "a" * 201  # 201 characters, which should fail
        
        with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
            self.service.add_task(long_title)
    
    def test_get_task(self):
        """Test retrieving a task."""
        created_task = self.service.add_task("Test Task")
        task_id = created_task.id
        
        retrieved_task = self.service.get_task(task_id)
        
        assert retrieved_task.id == task_id
        assert retrieved_task.title == "Test Task"
    
    def test_get_all_tasks(self):
        """Test retrieving all tasks."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        
        all_tasks = self.service.get_all_tasks()
        
        assert len(all_tasks) == 2
        task_ids = [task.id for task in all_tasks]
        assert task1.id in task_ids
        assert task2.id in task_ids
    
    def test_update_task_success(self):
        """Test successfully updating a task."""
        original_task = self.service.add_task("Original Task", "Original Description")
        task_id = original_task.id
        
        updated_task = self.service.update_task(
            task_id, 
            title="Updated Task", 
            description="Updated Description"
        )
        
        assert updated_task.id == task_id
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated Description"
    
    def test_update_task_title_only(self):
        """Test updating only the title of a task."""
        original_task = self.service.add_task("Original Task", "Original Description")
        task_id = original_task.id
        
        updated_task = self.service.update_task(task_id, title="Updated Task")
        
        assert updated_task.id == task_id
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Original Description"  # Should remain unchanged
    
    def test_update_task_description_only(self):
        """Test updating only the description of a task."""
        original_task = self.service.add_task("Original Task", "Original Description")
        task_id = original_task.id
        
        updated_task = self.service.update_task(task_id, description="Updated Description")
        
        assert updated_task.id == task_id
        assert updated_task.title == "Original Task"  # Should remain unchanged
        assert updated_task.description == "Updated Description"
    
    def test_update_task_title_validation(self):
        """Test validation for title length during update."""
        original_task = self.service.add_task("Original Task")
        task_id = original_task.id
        
        long_title = "a" * 201  # 201 characters, which should fail
        
        with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
            self.service.update_task(task_id, title=long_title)
    
    def test_update_task_empty_title_validation(self):
        """Test validation for empty title during update."""
        original_task = self.service.add_task("Original Task")
        task_id = original_task.id
        
        with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
            self.service.update_task(task_id, title="")
    
    def test_update_nonexistent_task(self):
        """Test updating a non-existent task."""
        with pytest.raises(ValueError, match="Task with ID nonexistent does not exist"):
            self.service.update_task("nonexistent", title="New Title")
    
    def test_delete_task_success(self):
        """Test successfully deleting a task."""
        task = self.service.add_task("Test Task")
        task_id = task.id
        
        # Verify task exists before deletion
        assert self.service.get_task(task_id) is not None
        
        result = self.service.delete_task(task_id)
        
        assert result is True
        assert self.service.get_task(task_id) is None
    
    def test_delete_nonexistent_task(self):
        """Test deleting a non-existent task."""
        with pytest.raises(ValueError, match="Task with ID nonexistent does not exist"):
            self.service.delete_task("nonexistent")
    
    def test_toggle_task_status_success(self):
        """Test successfully toggling a task's status."""
        task = self.service.add_task("Test Task")
        task_id = task.id
        
        # Verify initial state (should be False)
        initial_task = self.service.get_task(task_id)
        assert initial_task.completed is False
        
        # Toggle status
        toggled_task = self.service.toggle_task_status(task_id)
        
        assert toggled_task.completed is True
    
    def test_toggle_task_status_from_true_to_false(self):
        """Test toggling a task's status from True to False."""
        task = self.service.add_task("Test Task")
        task_id = task.id
        
        # First, set the task as completed
        self.subagent.update_task(task_id, completed=True)
        
        # Verify initial state (should be True)
        initial_task = self.service.get_task(task_id)
        assert initial_task.completed is True
        
        # Toggle status
        toggled_task = self.service.toggle_task_status(task_id)
        
        assert toggled_task.completed is False
    
    def test_toggle_nonexistent_task(self):
        """Test toggling status of a non-existent task."""
        with pytest.raises(ValueError, match="Task with ID nonexistent does not exist"):
            self.service.toggle_task_status("nonexistent")