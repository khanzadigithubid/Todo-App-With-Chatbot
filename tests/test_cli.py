import pytest
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch, MagicMock
from src.todo.cli import app
from typer.testing import CliRunner
from src.todo.storage import TodoCRUDSubagent
from src.todo.service import TodoService


class TestCLICommands:
    """Test cases for the CLI commands."""
    
    def setup_method(self):
        """Set up a fresh service instance for each test."""
        self.subagent = TodoCRUDSubagent()
        self.service = TodoService(self.subagent)
        self.runner = CliRunner()
    
    @patch('src.todo.cli.service')
    def test_add_command_success(self, mock_service):
        """Test the add command with valid parameters."""
        from src.todo.cli import app
        from src.todo.models import Task
        from datetime import datetime
        
        # Mock the service.add_task method
        mock_task = Task(
            id="123e4567-e89b-12d3-a456-426614174000",
            title="Test Task",
            description="Test Description"
        )
        mock_service.add_task.return_value = mock_task
        
        # Run the command
        result = self.runner.invoke(app, ["add", "Test Task", "--description", "Test Description"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Task ban gaya!" in result.stdout
    
    @patch('src.todo.cli.service')
    def test_add_command_without_description(self, mock_service):
        """Test the add command with only a title."""
        from src.todo.cli import app
        from src.todo.models import Task
        
        # Mock the service.add_task method
        mock_task = Task(
            id="123e4567-e89b-12d3-a456-426614174000",
            title="Test Task"
        )
        mock_service.add_task.return_value = mock_task
        
        # Run the command
        result = self.runner.invoke(app, ["add", "Test Task"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Task ban gaya!" in result.stdout
    
    @patch('src.todo.cli.service')
    def test_list_command_with_tasks(self, mock_service):
        """Test the list command when there are tasks."""
        from src.todo.cli import app
        from src.todo.models import Task
        
        # Create mock tasks
        task1 = Task(id="1", title="Task 1", completed=False)
        task2 = Task(id="2", title="Task 2", completed=True)
        mock_service.get_all_tasks.return_value = [task1, task2]
        
        # Run the command
        result = self.runner.invoke(app, ["list"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Task List" in result.stdout
        assert "Task 1" in result.stdout
        assert "Task 2" in result.stdout
    
    @patch('src.todo.cli.service')
    def test_list_command_no_tasks(self, mock_service):
        """Test the list command when there are no tasks."""
        from src.todo.cli import app
        
        # Mock empty task list
        mock_service.get_all_tasks.return_value = []
        
        # Run the command
        result = self.runner.invoke(app, ["list"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Koi tasks nahi hain" in result.stdout
    
    @patch('src.todo.cli.service')
    def test_update_command_success(self, mock_service):
        """Test the update command successfully."""
        from src.todo.cli import app
        from src.todo.models import Task
        
        # Mock the service.update_task method
        updated_task = Task(
            id="123e4567-e89b-12d3-a456-426614174000",
            title="Updated Task",
            description="Updated Description"
        )
        mock_service.update_task.return_value = updated_task
        
        # Run the command
        result = self.runner.invoke(app, [
            "update", 
            "123e4567-e89b-12d3-a456-426614174000", 
            "--title", "Updated Task", 
            "--description", "Updated Description"
        ])
        
        # Assertions
        assert result.exit_code == 0
        assert "Task update ho gaya!" in result.stdout
    
    @patch('src.todo.cli.service')
    def test_delete_command_success(self, mock_service):
        """Test the delete command successfully."""
        from src.todo.cli import app
        
        # Mock the service.delete_task method to return True (success)
        mock_service.delete_task.return_value = True
        
        # Run the command
        result = self.runner.invoke(app, ["delete", "123e4567-e89b-12d3-a456-426614174000"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Task delete ho gaya!" in result.stdout
    
    @patch('src.todo.cli.service')
    def test_complete_command_success(self, mock_service):
        """Test the complete command successfully."""
        from src.todo.cli import app
        from src.todo.models import Task
        
        # Mock the service.toggle_task_status method
        completed_task = Task(
            id="123e4567-e89b-12d3-a456-426614174000",
            title="Test Task",
            completed=True
        )
        mock_service.toggle_task_status.return_value = completed_task
        
        # Run the command
        result = self.runner.invoke(app, ["complete", "123e4567-e89b-12d3-a456-426614174000"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Task complete ho gaya!" in result.stdout
    
    @patch('src.todo.cli.service')
    def test_incomplete_command_success(self, mock_service):
        """Test the incomplete command successfully."""
        from src.todo.cli import app
        from src.todo.models import Task
        
        # Mock the service.toggle_task_status method
        incomplete_task = Task(
            id="123e4567-e89b-12d3-a456-426614174000",
            title="Test Task",
            completed=False
        )
        mock_service.toggle_task_status.return_value = incomplete_task
        
        # Run the command
        result = self.runner.invoke(app, ["incomplete", "123e4567-e89b-12d3-a456-426614174000"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Task incomplete ho gaya!" in result.stdout


# Note: Since the CLI is now replaced by the interactive menu system in main.py,
# we also need to test the interactive functionality.
# However, testing the interactive menu system requires different approach.
# Let's create a separate test for the interactive components.