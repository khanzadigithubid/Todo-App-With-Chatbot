# backend/tools/update_task.py

"""
Tool for updating tasks in the todo list
"""

from pydantic import BaseModel
from typing import Optional
from ..database import get_session
from sqlmodel import Session
from ..models import Task
from uuid import UUID

class UpdateTaskTool:
    def __init__(self):
        self.name = "update_task"
        self.description = "Update an existing task in the user's todo list"
        self.parameters = {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user"},
                "task_id": {"type": "string", "description": "The ID of the task to update"},
                "title": {"type": "string", "description": "The new title of the task"},
                "description": {"type": "string", "description": "The new description of the task"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "The new priority of the task"},
                "category": {"type": "string", "description": "The new category of the task"},
                "due_date": {"type": "string", "description": "The new due date of the task in YYYY-MM-DD format"}
            },
            "required": ["user_id", "task_id"]
        }
    
    def execute(self, user_id: str, task_id: str, title: Optional[str] = None, 
                description: Optional[str] = None, priority: Optional[str] = None, 
                category: Optional[str] = None, due_date: Optional[str] = None) -> dict:
        """
        Execute the update_task tool to update an existing task
        """
        with get_session() as session:
            # Get the task
            task = session.get(Task, UUID(task_id))
            
            if not task:
                raise ValueError(f"Task with ID {task_id} not found")
            
            if str(task.user_id) != user_id:
                raise ValueError(f"Task with ID {task_id} does not belong to user {user_id}")
            
            # Update the task with provided fields
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if priority is not None:
                task.priority = priority
            if category is not None:
                # For simplicity, we'll just add the category to the list
                if task.categories is None:
                    task.categories = [category]
                else:
                    task.categories.append(category)
            if due_date is not None:
                from datetime import datetime
                task.due_date = datetime.fromisoformat(due_date)
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.status == "completed",
                "priority": task.priority,
                "categories": task.categories,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }