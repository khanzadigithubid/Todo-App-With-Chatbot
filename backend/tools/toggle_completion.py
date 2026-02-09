# backend/tools/toggle_completion.py
"""
Tool for toggling the completion status of a task
"""

from pydantic import BaseModel
from typing import Optional
from ..database import get_session
from sqlmodel import Session
from ..models import Task

class ToggleTaskCompletionTool:
    def __init__(self):
        self.name = "toggle_task_completion"
        self.description = "Toggle the completion status of a task in the user's todo list"
        self.parameters = {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user"},
                "task_id": {"type": "integer", "description": "The ID of the task to toggle"}
            },
            "required": ["user_id", "task_id"]
        }
    
    def execute(self, user_id: str, task_id: int) -> dict:
        """
        Execute the toggle_task_completion tool to toggle the completion status of a task
        """
        with get_session() as session:
            # Get the task
            task = session.get(Task, task_id)
            
            if not task:
                raise ValueError(f"Task with ID {task_id} not found")
            
            if task.user_id != user_id:
                raise ValueError(f"Task with ID {task_id} does not belong to user {user_id}")
            
            # Toggle the completion status
            task.completed = not task.completed
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "message": f"Task marked as {'completed' if task.completed else 'pending'}"
            }