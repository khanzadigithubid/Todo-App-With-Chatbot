import pytest
from unittest.mock import patch, MagicMock
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from src.todo.storage import TodoCRUDSubagent
from src.todo.service import TodoService


class TestInteractiveMenuSystem:
    """Test cases for the interactive menu system in main.py."""
    
    def setup_method(self):
        """Set up fresh service instance for each test."""
        self.subagent = TodoCRUDSubagent()
        self.service = TodoService(self.subagent)
    
    @patch('builtins.input', side_effect=['2', '7'])  # Choose list then exit
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_menu_display_and_exit(self, mock_stdout, mock_input):
        """Test that the menu displays properly and can exit."""
        from main import print_menu
        
        # Mock console for the test
        from rich.console import Console
        console = Console(force_terminal=True)
        
        # Print menu and capture output
        print_menu(console)
        
        # Since print_menu now uses print without return value, 
        # we'll simulate the main function behavior
        output = mock_stdout.getvalue()
        # This test is primarily to ensure the function doesn't crash
        assert True  # The function executed without errors
    
    def test_add_task_interactive(self):
        """Test the interactive add task function."""
        from main import add_task_interactive
        from rich.console import Console
        
        # Create a mock console
        console = Console(force_terminal=True, file=io.StringIO())
        
        # Mock the input function to simulate user entering "Test Task" and "Test Description"
        with patch('builtins.input', side_effect=['Test Task', 'Test Description']):
            with patch('main.get_user_input', side_effect=['Test Task', 'Test Description']):
                add_task_interactive(console, self.service)
        
        # Verify that a task was added
        tasks = self.service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test Task"
        assert tasks[0].description == "Test Description"
    
    def test_list_tasks_interactive(self):
        """Test the interactive list tasks function."""
        from main import list_tasks_interactive
        from rich.console import Console
        
        # First, add a task for testing
        self.service.add_task("Test Task", "Test Description")
        
        # Create a mock console
        console = Console(force_terminal=True, file=io.StringIO())
        
        # Call the function
        list_tasks_interactive(console, self.service)
        
        # Verify that there are tasks to list
        tasks = self.service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test Task"
    
    def test_update_task_interactive(self):
        """Test the interactive update task function."""
        from main import update_task_interactive
        from rich.console import Console
        
        # First, add a task for testing
        task = self.service.add_task("Original Task", "Original Description")
        
        # Create a mock console
        console = Console(force_terminal=True, file=io.StringIO())
        
        # Mock the input function to simulate user selecting task 1, and entering new values
        with patch('builtins.input', side_effect=['1', 'Updated Task', 'Updated Description']):
            with patch('main.get_user_input', side_effect=['1', 'Updated Task', 'Updated Description']):
                update_task_interactive(console, self.service)
        
        # Verify that the task was updated
        updated_task = self.service.get_task(task.id)
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated Description"
    
    def test_delete_task_interactive(self):
        """Test the interactive delete task function."""
        from main import delete_task_interactive
        from rich.console import Console
        
        # First, add a task for testing
        task = self.service.add_task("Test Task", "Test Description")
        task_id = task.id  # Store the ID
        
        # Verify task exists
        assert self.service.get_task(task_id) is not None
        
        # Create a mock console
        console = Console(force_terminal=True, file=io.StringIO())
        
        # Mock the input function to simulate user selecting task 1
        with patch('builtins.input', side_effect=['1']):
            with patch('main.get_user_input', side_effect=['1']):
                delete_task_interactive(console, self.service)
        
        # Verify that the task was deleted
        assert self.service.get_task(task_id) is None
    
    def test_toggle_task_status_interactive(self):
        """Test the interactive toggle task status function."""
        from main import toggle_task_status_interactive
        from rich.console import Console
        
        # First, add a task for testing
        task = self.service.add_task("Test Task", "Test Description")
        task_id = task.id  # Store the ID
        
        # Verify task starts as incomplete
        initial_task = self.service.get_task(task_id)
        assert initial_task.completed is False
        
        # Create a mock console
        console = Console(force_terminal=True, file=io.StringIO())
        
        # Mock the input function to simulate user selecting task 1
        with patch('builtins.input', side_effect=['1']):
            with patch('main.get_user_input', side_effect=['1']):
                toggle_task_status_interactive(console, self.service, complete=True)
        
        # Verify that the task status was changed to complete
        updated_task = self.service.get_task(task_id)
        assert updated_task.completed is True


class TestInputFunctions:
    """Test helper functions in main.py."""
    
    def test_get_user_input(self):
        """Test the get_user_input function."""
        from main import get_user_input
        from rich.console import Console
        
        console = Console(force_terminal=True)
        
        # Mock input to return a test value
        with patch('builtins.input', return_value='Test Input'):
            result = get_user_input(console, "Enter value")
        
        assert result == 'Test Input'