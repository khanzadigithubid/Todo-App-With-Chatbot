"""
Tool Registry for MCP Tools
This module provides a registry for MCP tools to manage and access them programmatically.
"""

from typing import Dict, Type, List
from .base import BaseMCPTool
from .task_tools import (
    AddTaskTool, ListTasksTool, UpdateTaskTool, 
    DeleteTaskTool, ToggleTaskCompletionTool
)


class ToolRegistry:
    """
    A registry to manage MCP tools, allowing for dynamic registration 
    and retrieval of tools by name.
    """
    
    def __init__(self):
        self._tools: Dict[str, Type[BaseMCPTool]] = {}
        self._instances: Dict[str, BaseMCPTool] = {}
        
        # Register default tools
        self.register_tool(AddTaskTool)
        self.register_tool(ListTasksTool)
        self.register_tool(UpdateTaskTool)
        self.register_tool(DeleteTaskTool)
        self.register_tool(ToggleTaskCompletionTool)
    
    def register_tool(self, tool_class: Type[BaseMCPTool]):
        """
        Register a tool class in the registry.
        
        Args:
            tool_class: A subclass of BaseMCPTool to register
        """
        tool_name = tool_class().name
        self._tools[tool_name] = tool_class
        # Create an instance for quick access
        self._instances[tool_name] = tool_class()
    
    def get_tool_class(self, name: str) -> Type[BaseMCPTool]:
        """
        Get a tool class by its name.
        
        Args:
            name: The name of the tool to retrieve
            
        Returns:
            The tool class
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry")
        return self._tools[name]
    
    def get_tool_instance(self, name: str) -> BaseMCPTool:
        """
        Get a tool instance by its name.
        
        Args:
            name: The name of the tool to retrieve
            
        Returns:
            An instance of the tool
        """
        if name not in self._instances:
            raise KeyError(f"Tool '{name}' not found in registry")
        return self._instances[name]
    
    def get_all_tool_names(self) -> List[str]:
        """
        Get a list of all registered tool names.
        
        Returns:
            List of tool names
        """
        return list(self._tools.keys())
    
    def execute_tool(self, name: str, **kwargs) -> dict:
        """
        Execute a tool by name with the provided arguments.

        Args:
            name: The name of the tool to execute
            **kwargs: Arguments to pass to the tool

        Returns:
            The result of the tool execution
        """
        tool_instance = self.get_tool_instance(name)
        # Execute the sync run method
        return tool_instance.run_sync(**kwargs)


# Global registry instance
tool_registry = ToolRegistry()


def get_tool_registry() -> ToolRegistry:
    """
    Get the global tool registry instance.
    
    Returns:
        The global ToolRegistry instance
    """
    return tool_registry