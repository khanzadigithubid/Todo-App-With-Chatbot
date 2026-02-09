# backend/tools/delete_task.py
"""
Tool for deleting tasks from the todo list
"""

from pydantic import BaseModel
from typing import Optional
from ..database import get_session
from sqlmodel import Session
from ..models import Task

class DeleteTaskTool:
    def __init__(self):
        self.name = "delete_task"
        self.description = "Delete a task from the user's todo list"
        self.parameters = {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user"},
                "task_id": {"type": "integer", "description": "The ID of the task to delete"}
            },
            "required": ["user_id", "task_id"]
        }
    
    def execute(self, user_id: str, task_id: int) -> dict:
        """
        Execute the delete_task tool to remove a task
        """
        with get_session() as session:
            # Get the task
            task = session.get(Task, task_id)
            
            if not task:
                raise ValueError(f"Task with ID {task_id} not found")
            
            if task.user_id != user_id:
                raise ValueError(f"Task with ID {task_id} does not belong to user {user_id}")
            
            # Delete the task
            session.delete(task)
            session.commit()
            
            return {
                "id": task.id,
                "title": task.title,
                "message": "Task deleted successfully"
            }