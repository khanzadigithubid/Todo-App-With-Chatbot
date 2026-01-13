"""
MCP Tools for Task Management
This module implements the MCP tools for task management operations.
Each tool follows the MCP protocol specification and interacts with the database.
"""

from typing import Any, Dict
from uuid import UUID
import asyncio

from .base import BaseMCPTool, MCPToolError
from .. import crud, schemas
from ..database import engine
from sqlmodel import Session
from contextlib import contextmanager
from sqlalchemy.exc import OperationalError


class AddTaskTool(BaseMCPTool):
    """MCP Tool for adding a new task"""

    @property
    def name(self) -> str:
        return "add_task"

    @property
    def description(self) -> str:
        return "Adds a new task to the user's task list."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the task (1-200 characters)",
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the task",
                },
                "user_id": {
                    "type": "string",
                    "description": "UUID of the user for whom the task is being added",
                },
                "priority": {
                    "type": "string",
                    "description": "Priority level of the task",
                    "enum": ["low", "medium", "high"],
                    "default": "medium",
                },
                "due_date": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Deadline for the task in ISO 8601 format",
                }
            },
            "required": ["title", "user_id"]
        }

    async def run(self, **kwargs) -> Dict[str, Any]:
        """Execute the add_task operation"""
        title = kwargs.get("title")
        description = kwargs.get("description")
        user_id = kwargs.get("user_id")
        priority = kwargs.get("priority", "medium")
        due_date = kwargs.get("due_date")

        # Validate inputs
        if not title or len(title) < 1 or len(title) > 200:
            raise MCPToolError("Title must be between 1 and 200 characters")

        if not user_id:
            raise MCPToolError("user_id is required")

        try:
            # Create the task schema
            task_create = schemas.TaskCreate(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )

            # Create the task in the database using a session from the dependency
            with Session(engine) as db:
                task = crud.create_task(db, task_create, UUID(user_id))

                # Return the created task
                return {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "due_date": task.due_date.isoformat() if task.due_date else None
                }
        except OperationalError as e:
            raise MCPToolError(f"Database connection error: {str(e)}")
        except Exception as e:
            raise MCPToolError(f"Failed to create task: {str(e)}")


class ListTasksTool(BaseMCPTool):
    """MCP Tool for listing tasks"""

    @property
    def name(self) -> str:
        return "list_tasks"

    @property
    def description(self) -> str:
        return "Retrieves all tasks for a specific user."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "UUID of the user whose tasks are being retrieved",
                },
                "status_filter": {
                    "type": "string",
                    "description": "Filter tasks by status",
                    "enum": ["pending", "completed", "all"],
                    "default": "all",
                },
                "priority_filter": {
                    "type": "string",
                    "description": "Filter tasks by priority",
                    "enum": ["low", "medium", "high", "all"],
                    "default": "all",
                }
            },
            "required": ["user_id"]
        }

    async def run(self, **kwargs) -> Dict[str, Any]:
        """Execute the list_tasks operation"""
        user_id = kwargs.get("user_id")
        status_filter = kwargs.get("status_filter", "all")
        priority_filter = kwargs.get("priority_filter", "all")

        if not user_id:
            raise MCPToolError("user_id is required")

        try:
            with Session(engine) as db:
                tasks = crud.get_tasks(db, UUID(user_id))

                # Apply filters if specified
                if status_filter != "all":
                    tasks = [task for task in tasks if task.status == status_filter]

                if priority_filter != "all":
                    tasks = [task for task in tasks if task.priority == priority_filter]

                # Format the tasks for return
                result = []
                for task in tasks:
                    result.append({
                        "id": str(task.id),
                        "title": task.title,
                        "description": task.description,
                        "status": task.status,
                        "priority": task.priority,
                        "created_at": task.created_at.isoformat() if task.created_at else None,
                        "due_date": task.due_date.isoformat() if task.due_date else None
                    })

                return result
        except OperationalError as e:
            raise MCPToolError(f"Database connection error: {str(e)}")
        except Exception as e:
            raise MCPToolError(f"Failed to retrieve tasks: {str(e)}")


class UpdateTaskTool(BaseMCPTool):
    """MCP Tool for updating a task"""

    @property
    def name(self) -> str:
        return "update_task"

    @property
    def description(self) -> str:
        return "Updates an existing task."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "UUID of the task to be updated",
                },
                "user_id": {
                    "type": "string",
                    "description": "UUID of the user who owns the task",
                },
                "title": {
                    "type": "string",
                    "description": "New title of the task (1-200 characters)",
                },
                "description": {
                    "type": "string",
                    "description": "New description of the task",
                },
                "status": {
                    "type": "string",
                    "description": "New status of the task",
                    "enum": ["pending", "completed"],
                },
                "priority": {
                    "type": "string",
                    "description": "New priority level of the task",
                    "enum": ["low", "medium", "high"],
                },
                "due_date": {
                    "type": "string",
                    "format": "date-time",
                    "description": "New deadline for the task in ISO 8601 format",
                }
            },
            "required": ["task_id", "user_id"]
        }

    async def run(self, **kwargs) -> Dict[str, Any]:
        """Execute the update_task operation"""
        task_id = kwargs.get("task_id")
        user_id = kwargs.get("user_id")
        title = kwargs.get("title")
        description = kwargs.get("description")
        status = kwargs.get("status")
        priority = kwargs.get("priority")
        due_date = kwargs.get("due_date")

        if not task_id or not user_id:
            raise MCPToolError("task_id and user_id are required")

        try:
            # Create the task update schema
            task_update = schemas.TaskUpdate(
                title=title,
                description=description,
                status=status,
                priority=priority,
                due_date=due_date
            )

            with Session(engine) as db:
                task = crud.update_task(db, UUID(task_id), task_update, UUID(user_id))

                if not task:
                    raise MCPToolError("Task not found or user doesn't have permission to update it")

                # Return the updated task
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
        except OperationalError as e:
            raise MCPToolError(f"Database connection error: {str(e)}")
        except Exception as e:
            raise MCPToolError(f"Failed to update task: {str(e)}")


class DeleteTaskTool(BaseMCPTool):
    """MCP Tool for deleting a task"""

    @property
    def name(self) -> str:
        return "delete_task"

    @property
    def description(self) -> str:
        return "Deletes an existing task."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "UUID of the task to be deleted",
                },
                "user_id": {
                    "type": "string",
                    "description": "UUID of the user who owns the task",
                }
            },
            "required": ["task_id", "user_id"]
        }

    async def run(self, **kwargs) -> Dict[str, Any]:
        """Execute the delete_task operation"""
        task_id = kwargs.get("task_id")
        user_id = kwargs.get("user_id")

        if not task_id or not user_id:
            raise MCPToolError("task_id and user_id are required")

        try:
            with Session(engine) as db:
                task = crud.delete_task(db, UUID(task_id), UUID(user_id))

                if task:
                    return {
                        "success": True,
                        "message": "Task deleted successfully"
                    }
                else:
                    raise MCPToolError("Task not found or user doesn't have permission to delete it")
        except OperationalError as e:
            raise MCPToolError(f"Database connection error: {str(e)}")
        except Exception as e:
            raise MCPToolError(f"Failed to delete task: {str(e)}")


class ToggleTaskCompletionTool(BaseMCPTool):
    """MCP Tool for toggling task completion status"""

    @property
    def name(self) -> str:
        return "toggle_task_completion"

    @property
    def description(self) -> str:
        return "Toggles the completion status of a task."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "UUID of the task to toggle",
                },
                "user_id": {
                    "type": "string",
                    "description": "UUID of the user who owns the task",
                }
            },
            "required": ["task_id", "user_id"]
        }

    async def run(self, **kwargs) -> Dict[str, Any]:
        """Execute the toggle_task_completion operation"""
        task_id = kwargs.get("task_id")
        user_id = kwargs.get("user_id")

        if not task_id or not user_id:
            raise MCPToolError("task_id and user_id are required")

        try:
            with Session(engine) as db:
                # Get the current task
                task = crud.get_task(db, UUID(task_id), UUID(user_id))

                if not task:
                    raise MCPToolError("Task not found or user doesn't have permission to access it")

                # Toggle the status
                new_status = "completed" if task.status == "pending" else "pending"

                # Update the task with the new status
                task_update = schemas.TaskUpdate(status=new_status)
                updated_task = crud.update_task(db, UUID(task_id), task_update, UUID(user_id))

                if updated_task:
                    return {
                        "id": str(updated_task.id),
                        "status": updated_task.status,
                        "title": updated_task.title
                    }
                else:
                    raise MCPToolError("Failed to update task status")
        except OperationalError as e:
            raise MCPToolError(f"Database connection error: {str(e)}")
        except Exception as e:
            raise MCPToolError(f"Failed to toggle task completion: {str(e)}")