# backend/tools/add_task.py
"""
Tool for adding tasks to the todo list
"""

from pydantic import BaseModel
from typing import Optional
from ..database import get_session
from sqlmodel import Session
from ..models import Task
import uuid

class AddTaskTool:
    def __init__(self):
        self.name = "add_task"
        self.description = "Create a new task in the user's todo list"
        self.parameters = {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user"},
                "title": {"type": "string", "description": "The title of the task"},
                "description": {"type": "string", "description": "The description of the task"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "The priority of the task"},
                "category": {"type": "string", "description": "The category of the task"},
                "due_date": {"type": "string", "description": "The due date of the task in YYYY-MM-DD format"}
            },
            "required": ["user_id", "title"]
        }
    
    def execute(self, user_id: str, title: str, description: Optional[str] = None, 
                priority: Optional[str] = "medium", category: Optional[str] = None, 
                due_date: Optional[str] = None) -> dict:
        """
        Execute the add_task tool to create a new task
        """
        with get_session() as session:
            # Create a new task
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                priority=priority,
                category=category,
                due_date=due_date,
                completed=False
            )
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority,
                "category": task.category,
                "due_date": task.due_date,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }