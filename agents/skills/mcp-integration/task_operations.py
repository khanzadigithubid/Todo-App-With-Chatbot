"""
Task Operations Skill for MCP Integration
This module provides reusable functions for task management operations
that can be used by the chatbot agent through MCP tools.
"""

from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime
from backend.app import crud, schemas
from backend.app.database import SessionLocal
from backend.app.models import Task


class TaskOperations:
    """
    A skill class that provides methods for task management operations.
    These methods can be used by MCP tools to interact with the database.
    """
    
    @staticmethod
    def create_task(title: str, description: Optional[str] = None, 
                   user_id: str = None, priority: str = "medium",
                   due_date: Optional[str] = None) -> Dict:
        """
        Create a new task in the database.
        
        Args:
            title: Title of the task (required)
            description: Description of the task (optional)
            user_id: UUID of the user for whom the task is being added (required)
            priority: Priority level of the task (default: "medium")
            due_date: Deadline for the task in ISO 8601 format (optional)
            
        Returns:
            Dict containing the created task information
        """
        task_create_schema = schemas.TaskCreate(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )
        
        with SessionLocal() as db:
            task = crud.create_task(db, task_create_schema, UUID(user_id))
            return {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "due_date": task.due_date.isoformat() if task.due_date else None
            }
    
    @staticmethod
    def get_tasks(user_id: str, status_filter: Optional[str] = "all", 
                  priority_filter: Optional[str] = "all") -> List[Dict]:
        """
        Retrieve all tasks for a specific user.
        
        Args:
            user_id: UUID of the user whose tasks are being retrieved
            status_filter: Filter tasks by status (pending, completed, all)
            priority_filter: Filter tasks by priority (low, medium, high, all)
            
        Returns:
            List of task dictionaries
        """
        with SessionLocal() as db:
            tasks = crud.get_tasks(db, UUID(user_id))
            
            # Apply filters if specified
            if status_filter and status_filter != "all":
                tasks = [task for task in tasks if task.status == status_filter]
                
            if priority_filter and priority_filter != "all":
                tasks = [task for task in tasks if task.priority == priority_filter]
                
            return [
                {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "due_date": task.due_date.isoformat() if task.due_date else None
                }
                for task in tasks
            ]
    
    @staticmethod
    def update_task(task_id: str, user_id: str, title: Optional[str] = None,
                    description: Optional[str] = None, status: Optional[str] = None,
                    priority: Optional[str] = None, due_date: Optional[str] = None) -> Optional[Dict]:
        """
        Update an existing task.
        
        Args:
            task_id: UUID of the task to be updated
            user_id: UUID of the user who owns the task
            title: New title of the task (optional)
            description: New description of the task (optional)
            status: New status of the task (optional)
            priority: New priority level of the task (optional)
            due_date: New deadline for the task (optional)
            
        Returns:
            Dict containing the updated task information or None if not found
        """
        task_update_schema = schemas.TaskUpdate(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date
        )
        
        with SessionLocal() as db:
            task = crud.update_task(db, UUID(task_id), task_update_schema, UUID(user_id))
            if task:
                return {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                    "due_date": task.due_date.isoformat() if task.due_date else None
                }
            return None
    
    @staticmethod
    def delete_task(task_id: str, user_id: str) -> Dict[str, bool]:
        """
        Delete an existing task.
        
        Args:
            task_id: UUID of the task to be deleted
            user_id: UUID of the user who owns the task
            
        Returns:
            Dict with success status and message
        """
        with SessionLocal() as db:
            task = crud.delete_task(db, UUID(task_id), UUID(user_id))
            if task:
                return {"success": True, "message": "Task deleted successfully"}
            return {"success": False, "message": "Task not found"}
    
    @staticmethod
    def toggle_task_completion(task_id: str, user_id: str) -> Optional[Dict]:
        """
        Toggle the completion status of a task.
        
        Args:
            task_id: UUID of the task to toggle
            user_id: UUID of the user who owns the task
            
        Returns:
            Dict containing the toggled task information or None if not found
        """
        with SessionLocal() as db:
            task = crud.get_task(db, UUID(task_id), UUID(user_id))
            if not task:
                return None
            
            # Toggle the status
            new_status = "completed" if task.status == "pending" else "pending"
            
            task_update_schema = schemas.TaskUpdate(status=new_status)
            updated_task = crud.update_task(db, UUID(task_id), task_update_schema, UUID(user_id))
            
            if updated_task:
                return {
                    "id": str(updated_task.id),
                    "status": updated_task.status,
                    "title": updated_task.title
                }
            return None