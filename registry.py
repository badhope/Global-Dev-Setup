# Global-Dev-Setup - Tool Registry API
# Provides a simple, queryable interface for external agents to discover and install tools

from typing import List, Dict, Any, Optional
from pathlib import Path
import yaml
import json

class ToolRegistry:
    """Registry for discovering and querying available tools"""
    
    def __init__(self, tools_dir: str = "tools", templates_dir: str = "environment-templates"):
        self.tools_dir = Path(tools_dir)
        self.templates_dir = Path(templates_dir)
        self.tools = {}
        self.templates = {}
        self.load_tools()
        self.load_templates()
    
    def load_tools(self):
        """Load all tool definitions from YAML files"""
        for tool_path in self.tools_dir.rglob("tool.yaml"):
            try:
                with open(tool_path, 'r') as f:
                    tool_data = yaml.safe_load(f)
                    tool_name = tool_data.get("name")
                    if tool_name:
                        # Add category from directory structure
                        category = tool_path.parent.parent.name
                        tool_data["category"] = category
                        tool_data["path"] = str(tool_path)
                        self.tools[tool_name] = tool_data
            except Exception as e:
                print(f"Error loading {tool_path}: {e}")
    
    def load_templates(self):
        """Load all environment templates from YAML files"""
        for template_path in self.templates_dir.glob("*.yaml"):
            try:
                with open(template_path, 'r') as f:
                    template_data = yaml.safe_load(f)
                    template_name = template_data.get("name")
                    if template_name:
                        template_data["path"] = str(template_path)
                        self.templates[template_name] = template_data
            except Exception as e:
                print(f"Error loading {template_path}: {e}")
    
    def list_tools(self) -> List[str]:
        """Get list of all available tool names"""
        return list(self.tools.keys())
    
    def list_categories(self) -> List[str]:
        """Get list of all tool categories"""
        categories = set()
        for tool in self.tools.values():
            categories.add(tool.get("category", "other"))
        return sorted(list(categories))
    
    def get_tool(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific tool"""
        return self.tools.get(tool_name)
    
    def search_tools(self, keyword: str) -> List[Dict[str, Any]]:
        """Search tools by keyword in name, description, or tags"""
        results = []
        keyword = keyword.lower()
        for tool in self.tools.values():
            if (keyword in tool.get("name", "").lower() or
                keyword in tool.get("description", "").lower() or
                any(keyword in tag.lower() for tag in tool.get("tags", []))):
                results.append(tool)
        return results
    
    def get_tools_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all tools in a specific category"""
        return [tool for tool in self.tools.values() 
                if tool.get("category") == category]
    
    def list_templates(self) -> List[str]:
        """Get list of all available environment templates"""
        return list(self.templates.keys())
    
    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific template"""
        return self.templates.get(template_name)
    
    def get_template_tools(self, template_name: str) -> List[Dict[str, Any]]:
        """Get all tools included in a template"""
        template = self.get_template(template_name)
        if not template:
            return []
        
        all_tools = []
        for tool_info in template.get("required_tools", []):
            tool_name = tool_info.get("name")
            tool = self.get_tool(tool_name)
            if tool:
                all_tools.append({"tool": tool, "type": "required", "version": tool_info.get("version")})
        
        for tool_info in template.get("recommended_tools", []):
            tool_name = tool_info.get("name")
            tool = self.get_tool(tool_name)
            if tool:
                all_tools.append({"tool": tool, "type": "recommended", "version": tool_info.get("version")})
        
        for tool_info in template.get("optional_tools", []):
            tool_name = tool_info.get("name")
            tool = self.get_tool(tool_name)
            if tool:
                all_tools.append({"tool": tool, "type": "optional", "version": tool_info.get("version")})
        
        return all_tools
    
    def recommend_tools(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend tools based on requirements"""
        recommendations = []
        
        # Check if a template matches
        category = requirements.get("category")
        if category:
            template_name = self._category_to_template(category)
            if template_name:
                template = self.get_template(template_name)
                if template:
                    for tool_info in template.get("required_tools", []):
                        tool = self.get_tool(tool_info.get("name"))
                        if tool:
                            recommendations.append({
                                "tool": tool,
                                "priority": "high",
                                "reason": f"Required for {category}"
                            })
                    for tool_info in template.get("recommended_tools", []):
                        tool = self.get_tool(tool_info.get("name"))
                        if tool:
                            recommendations.append({
                                "tool": tool,
                                "priority": "medium",
                                "reason": f"Recommended for {category}"
                            })
        
        # Additional filtering based on OS
        os_filter = requirements.get("os")
        if os_filter and recommendations:
            recommendations = [r for r in recommendations 
                              if os_filter in r["tool"].get("supported_os", [])]
        
        return recommendations
    
    def _category_to_template(self, category: str) -> Optional[str]:
        """Map category to template name"""
        mapping = {
            "web": "fullstack-developer",
            "frontend": "frontend-developer",
            "backend": "backend-developer",
            "ai": "ai-ml-developer",
            "ai-agent": "ai-agent-developer",
            "ml": "ml-engineer",
            "data-science": "data-science",
            "big-data": "big-data-engineer",
            "data-engineering": "data-engineering",
            "devops": "devops-engineer",
            "cloud": "cloud-native-developer",
            "mobile": "mobile-developer",
            "game": "game-developer",
            "blockchain": "blockchain-developer",
            "iot": "iot-developer",
            "embedded": "embedded-developer",
            "security": "security-engineer",
            "qa": "qa-engineer",
            "python": "backend-developer",
            "java": "backend-developer",
            "go": "cloud-native-developer",
            "rust": "embedded-developer",
        }
        return mapping.get(category.lower())
    
    def get_installation_command(self, tool_name: str, os_type: str = "linux") -> Optional[str]:
        """Get the best installation command for a tool on specific OS"""
        tool = self.get_tool(tool_name)
        if not tool:
            return None
        
        sources = tool.get("installation_sources", [])
        
        # Find best source for the OS
        for source in sorted(sources, key=lambda x: x.get("priority", 10)):
            supported_os = source.get("os", [])
            if os_type in supported_os or "all" in supported_os:
                if "command" in source:
                    return source["command"]
                elif source.get("type") == "apt":
                    return f"sudo apt install -y {source.get('package_name')}"
                elif source.get("type") == "brew":
                    return f"brew install {source.get('package_name')}"
                elif source.get("type") == "pip":
                    return f"pip install {source.get('package_name')}"
                elif source.get("type") == "npm":
                    return f"npm install -g {source.get('package_name')}"
                elif source.get("type") == "docker":
                    return f"docker run -d {source.get('command', source.get('image', ''))}"
        
        return None
    
    def export_to_json(self, output_file: str = "tool_registry.json"):
        """Export the entire registry to JSON"""
        data = {
            "tools": self.tools,
            "templates": self.templates,
            "categories": self.list_categories()
        }
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_install_script(self, tool_names: List[str], os_type: str = "linux") -> str:
        """Generate an installation script for specified tools"""
        script_lines = [
            "#!/bin/bash",
            f"# Auto-generated install script for: {', '.join(tool_names)}",
            "# OS: {os_type}",
            "",
            "set -e",
            ""
        ]
        
        for tool_name in tool_names:
            cmd = self.get_installation_command(tool_name, os_type)
            if cmd:
                script_lines.append(f"# Install {tool_name}")
                script_lines.append(cmd)
                script_lines.append("")
        
        script_lines.append("echo 'Installation complete!'")
        
        return "\n".join(script_lines)


# Simple CLI for the registry
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Global-Dev-Setup Tool Registry")
    parser.add_argument("--list-tools", action="store_true", help="List all tools")
    parser.add_argument("--list-categories", action="store_true", help="List all categories")
    parser.add_argument("--list-templates", action="store_true", help="List all templates")
    parser.add_argument("--tool", type=str, help="Get tool details")
    parser.add_argument("--template", type=str, help="Get template details")
    parser.add_argument("--search", type=str, help="Search tools by keyword")
    parser.add_argument("--category", type=str, help="Get tools by category")
    parser.add_argument("--recommend", type=str, help="Recommend tools for category")
    parser.add_argument("--install-command", type=str, help="Get install command for tool")
    parser.add_argument("--export", action="store_true", help="Export registry to JSON")
    
    args = parser.parse_args()
    registry = ToolRegistry()
    
    if args.list_tools:
        print("Available tools:")
        for tool in registry.list_tools():
            print(f"  - {tool}")
    
    elif args.list_categories:
        print("Available categories:")
        for category in registry.list_categories():
            print(f"  - {category}")
    
    elif args.list_templates:
        print("Available templates:")
        for template in registry.list_templates():
            template_data = registry.get_template(template)
            desc = template_data.get("description", "") if template_data else ""
            print(f"  - {template}: {desc}")
    
    elif args.tool:
        tool = registry.get_tool(args.tool)
        if tool:
            print(json.dumps(tool, indent=2, ensure_ascii=False))
        else:
            print(f"Tool '{args.tool}' not found")
    
    elif args.template:
        template = registry.get_template(args.template)
        if template:
            print(json.dumps(template, indent=2, ensure_ascii=False))
        else:
            print(f"Template '{args.template}' not found")
    
    elif args.search:
        results = registry.search_tools(args.search)
        print(f"Found {len(results)} tools:")
        for tool in results:
            print(f"  - {tool['name']}: {tool.get('description', '')}")
    
    elif args.category:
        tools = registry.get_tools_by_category(args.category)
        print(f"Tools in category '{args.category}':")
        for tool in tools:
            print(f"  - {tool['name']}: {tool.get('description', '')}")
    
    elif args.recommend:
        recommendations = registry.recommend_tools({"category": args.recommend})
        print(f"Recommended tools for '{args.recommend}':")
        for rec in recommendations:
            print(f"  [{rec['priority']}] {rec['tool']['name']}: {rec['reason']}")
    
    elif args.install_command:
        cmd = registry.get_installation_command(args.install_command)
        if cmd:
            print(cmd)
        else:
            print(f"No installation command found for '{args.install_command}'")
    
    elif args.export:
        registry.export_to_json()
        print("Registry exported to tool_registry.json")
    
    else:
        parser.print_help()
