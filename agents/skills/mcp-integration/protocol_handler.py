"""
Protocol Handler Skill for MCP Integration
This module provides functions to handle MCP protocol communication
and coordinate with the task operations skills.
"""

import asyncio
from typing import Any, Dict, Optional
from .task_operations import TaskOperations


class ProtocolHandler:
    """
    A skill class that handles MCP protocol communication and
    coordinates with task operations skills.
    """
    
    @staticmethod
    async def handle_add_task_request(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an add_task request via MCP protocol.
        
        Args:
            params: Parameters for the add_task operation
            
        Returns:
            Result of the add_task operation
        """
        try:
            result = TaskOperations.create_task(
                title=params["title"],
                description=params.get("description"),
                user_id=params["user_id"],
                priority=params.get("priority", "medium"),
                due_date=params.get("due_date")
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def handle_list_tasks_request(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a list_tasks request via MCP protocol.
        
        Args:
            params: Parameters for the list_tasks operation
            
        Returns:
            Result of the list_tasks operation
        """
        try:
            result = TaskOperations.get_tasks(
                user_id=params["user_id"],
                status_filter=params.get("status_filter", "all"),
                priority_filter=params.get("priority_filter", "all")
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def handle_update_task_request(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an update_task request via MCP protocol.
        
        Args:
            params: Parameters for the update_task operation
            
        Returns:
            Result of the update_task operation
        """
        try:
            result = TaskOperations.update_task(
                task_id=params["task_id"],
                user_id=params["user_id"],
                title=params.get("title"),
                description=params.get("description"),
                status=params.get("status"),
                priority=params.get("priority"),
                due_date=params.get("due_date")
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def handle_delete_task_request(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a delete_task request via MCP protocol.
        
        Args:
            params: Parameters for the delete_task operation
            
        Returns:
            Result of the delete_task operation
        """
        try:
            result = TaskOperations.delete_task(
                task_id=params["task_id"],
                user_id=params["user_id"]
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def handle_toggle_task_completion_request(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a toggle_task_completion request via MCP protocol.
        
        Args:
            params: Parameters for the toggle_task_completion operation
            
        Returns:
            Result of the toggle_task_completion operation
        """
        try:
            result = TaskOperations.toggle_task_completion(
                task_id=params["task_id"],
                user_id=params["user_id"]
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def validate_request_params(operation: str, params: Dict[str, Any]) -> Optional[str]:
        """
        Validate the parameters for a given operation.
        
        Args:
            operation: The operation name
            params: Parameters to validate
            
        Returns:
            Error message if validation fails, None otherwise
        """
        required_params = {
            "add_task": ["title", "user_id"],
            "list_tasks": ["user_id"],
            "update_task": ["task_id", "user_id"],
            "delete_task": ["task_id", "user_id"],
            "toggle_task_completion": ["task_id", "user_id"]
        }
        
        if operation not in required_params:
            return f"Unknown operation: {operation}"
        
        for param in required_params[operation]:
            if param not in params:
                return f"Missing required parameter: {param}"
        
        return None