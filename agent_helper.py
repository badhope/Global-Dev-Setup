# Global-Dev-Setup - Agent Query Helper
# Simple helper for external agents to query the tool registry

import json
import subprocess
import sys

class AgentHelper:
    """Simple helper for external agents to interact with the registry"""
    
    def __init__(self):
        pass
    
    def run_query(self, command: str, *args):
        """Run a query on the registry"""
        cmd = ["python", "registry.py"]
        cmd.append(f"--{command}")
        cmd.extend(args)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr.strip()}"
        except Exception as e:
            return f"Exception: {str(e)}"
    
    def list_tools(self):
        """Get list of all tools"""
        return self.run_query("list-tools")
    
    def list_categories(self):
        """Get list of all categories"""
        return self.run_query("list-categories")
    
    def list_templates(self):
        """Get list of all templates"""
        return self.run_query("list-templates")
    
    def get_tool_info(self, tool_name):
        """Get detailed tool information as JSON"""
        return self.run_query("tool", tool_name)
    
    def get_template_info(self, template_name):
        """Get detailed template information as JSON"""
        return self.run_query("template", template_name)
    
    def search_tools(self, keyword):
        """Search tools by keyword"""
        return self.run_query("search", keyword)
    
    def get_tools_by_category(self, category):
        """Get tools by category"""
        return self.run_query("category", category)
    
    def get_recommendations(self, category):
        """Get recommendations for a category"""
        return self.run_query("recommend", category)
    
    def get_install_command(self, tool_name):
        """Get installation command for a tool"""
        return self.run_query("install-command", tool_name)
    
    def export_registry(self):
        """Export registry to JSON"""
        self.run_query("export")
        with open("tool_registry.json", "r") as f:
            return f.read()


# Example usage for external agents
if __name__ == "__main__":
    helper = AgentHelper()
    
    # Example: Agent wants to set up a web development environment
    print("=== Agent Query Example ===")
    print()
    
    # 1. Agent asks: What templates are available?
    print("1. Available templates:")
    print(helper.list_templates())
    print()
    
    # 2. Agent asks: Get details for web developer template
    print("2. Web developer template details:")
    print(helper.get_template_info("fullstack-developer"))
    print()
    
    # 3. Agent asks: What tools are recommended for web development?
    print("3. Recommended tools for web development:")
    print(helper.get_recommendations("web"))
    print()
    
    # 4. Agent asks: Get installation command for a specific tool
    print("4. Installation command for docker:")
    print(helper.get_install_command("docker"))
    print()
    
    # 5. Agent can export the entire registry for offline use
    print("5. Exporting registry to JSON...")
    registry_json = helper.export_registry()
    print("Registry exported successfully!")
