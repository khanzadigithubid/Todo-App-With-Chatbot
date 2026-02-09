# backend/tools/registry.py

"""
Registry for tools used by the AI assistant
"""

class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register_tool(self, name, tool_class):
        """Register a tool with the registry"""
        self.tools[name] = tool_class
    
    def get_tool_instance(self, name):
        """Get an instance of a registered tool"""
        if name in self.tools:
            return self.tools[name]()
        else:
            raise ValueError(f"Tool '{name}' not found in registry")
    
    def execute_tool(self, name, **kwargs):
        """Execute a tool with the given arguments"""
        tool = self.get_tool_instance(name)
        return tool.execute(**kwargs)

# Global instance of the tool registry
tool_registry = ToolRegistry()