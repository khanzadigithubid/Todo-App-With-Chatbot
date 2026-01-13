"""
Base class for MCP (Model Context Protocol) tools
Provides common functionality and interface for all MCP tools
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from uuid import UUID


class BaseMCPTool(ABC):
    """
    Abstract base class for all MCP tools in the task management system.
    Each tool should inherit from this class and implement the required methods.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name of the tool"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the tool does"""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """JSON schema defining the parameters the tool accepts"""
        pass
    
    @abstractmethod
    async def run(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with the provided parameters.

        Args:
            **kwargs: Parameters for the tool execution

        Returns:
            Dict containing the result of the tool execution
        """
        pass

    def run_sync(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool synchronously with the provided parameters.
        Default implementation runs the async method in a new event loop.

        Args:
            **kwargs: Parameters for the tool execution

        Returns:
            Dict containing the result of the tool execution
        """
        import asyncio
        import concurrent.futures

        # Run the async function in a new event loop using a thread pool
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self._run_async, **kwargs)
            return future.result()

    def _run_async(self, **kwargs):
        """
        Helper method to run the async function in a new event loop.
        """
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.run(**kwargs))
        finally:
            loop.close()


class MCPToolError(Exception):
    """Custom exception for MCP tool errors"""
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)