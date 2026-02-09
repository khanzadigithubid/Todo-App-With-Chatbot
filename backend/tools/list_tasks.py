# backend/tools/list_tasks.py
"""
Tool for listing tasks from the todo list
"""

from pydantic import BaseModel
from typing import Optional, List
from ..database import get_session
from sqlmodel import Session, select
from ..models import Task

class ListTasksTool:
    def __init__(self):
        self.name = "list_tasks"
        self.description = "Retrieve tasks from the user's todo list"
        self.parameters = {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user"},
                "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter tasks by status"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Filter tasks by priority"},
                "category": {"type": "string", "description": "Filter tasks by category"}
            },
            "required": ["user_id"]
        }
    
    def execute(self, user_id: str, status: Optional[str] = "all", 
                priority: Optional[str] = None, category: Optional[str] = None) -> List[dict]:
        """
        Execute the list_tasks tool to retrieve tasks
        """
        with get_session() as session:
            # Build query based on filters
            query = select(Task).where(Task.user_id == user_id)
            
            if status and status != "all":
                if status == "pending":
                    query = query.where(Task.completed == False)
                elif status == "completed":
                    query = query.where(Task.completed == True)
            
            if priority:
                query = query.where(Task.priority == priority)
                
            if category:
                query = query.where(Task.category == category)
            
            tasks = session.exec(query).all()
            
            # Convert tasks to dictionaries
            task_list = []
            for task in tasks:
                task_dict = {
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
                task_list.append(task_dict)
            
            return task_list