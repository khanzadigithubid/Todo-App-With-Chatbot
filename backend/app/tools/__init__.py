"""
MCP Tools Interface
This module provides the interface for MCP (Model Context Protocol) tools
used in the chatbot system for task management operations.
"""

from .base import BaseMCPTool
from .task_tools import AddTaskTool, ListTasksTool, UpdateTaskTool, DeleteTaskTool, ToggleTaskCompletionTool

# Register all tools for the MCP system
MCP_TOOLS = [
    AddTaskTool,
    ListTasksTool,
    UpdateTaskTool,
    DeleteTaskTool,
    ToggleTaskCompletionTool
]

__all__ = [
    "BaseMCPTool",
    "MCP_TOOLS",
    "AddTaskTool",
    "ListTasksTool", 
    "UpdateTaskTool",
    "DeleteTaskTool",
    "ToggleTaskCompletionTool"
]