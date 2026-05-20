#!/usr/bin/env python3
# Global-Dev-Setup - Enhanced Tool Registry with Mirror Support
# Provides query, download, and installation with automatic mirror selection

import json
import yaml
import os
import sys
from pathlib import Path
import urllib.parse
import socket
import ssl
import http.client
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
import re

logger = None

try:
    import requests
except ImportError:
    requests = None

try:
    from core.utils.logger import get_logger
    logger = get_logger("registry")
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("registry")


class Region:
    """Supported region configurations"""
    GLOBAL = "global"
    CN = "cn"


class MirrorInfo:
    """Mirror information"""
    def __init__(self, url: str, name: str = "", priority: int = 1, region: str = "global"):
        self.url = url
        self.name = name
        self.priority = priority
        self.region = region
    
    def __repr__(self):
        return f"Mirror({self.name}, {self.url}, priority={self.priority})"


class ToolRegistry:
    """Enhanced registry with mirror support and version management"""
    
    def __init__(
        self, 
        tools_dir: str = "tools", 
        templates_dir: str = "environment-templates",
        mirrors_config_file: str = "mirrors_config.yaml",
        auto_detect_region: bool = True,
        preferred_region: Optional[str] = None
    ):
        self.tools_dir = Path(tools_dir)
        self.templates_dir = Path(templates_dir)
        self.mirrors_config_file = Path(mirrors_config_file)
        
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.mirrors_config: Dict[str, Any] = {}
        
        # Region management
        self.current_region: str = preferred_region or Region.GLOBAL
        if auto_detect_region and preferred_region is None:
            self.current_region = self._detect_region()
        
        self.load_mirrors_config()
        self.load_tools()
        self.load_templates()
    
    def _detect_region(self) -> str:
        """Detect the current region automatically"""
        try:
            conn = http.client.HTTPSConnection("www.baidu.com", timeout=2)
            conn.request("HEAD", "/")
            response = conn.getresponse()
            if response.status in (200, 301, 302):
                logger.info("Region detected: CN (China)")
                return Region.CN
        except:
            pass
        
        logger.info("Region detected: GLOBAL")
        return Region.GLOBAL
    
    def set_region(self, region: Union[Region, str]):
        """Set the current region"""
        if isinstance(region, str):
            self.current_region = region.lower()
        else:
            self.current_region = region
        logger.info(f"Region set to: {self.current_region}")
    
    def get_region(self) -> str:
        """Get current region"""
        return self.current_region
    
    def load_mirrors_config(self):
        """Load mirror configuration file"""
        if not self.mirrors_config_file.exists():
            logger.warning("Mirror config file not found, using defaults")
            self.mirrors_config = self._get_default_mirrors_config()
            return
        
        try:
            with open(self.mirrors_config_file, 'r', encoding='utf-8') as f:
                self.mirrors_config = yaml.safe_load(f)
            logger.info("Mirror config loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load mirror config: {e}")
            self.mirrors_config = self._get_default_mirrors_config()
    
    def _get_default_mirrors_config(self):
        """Get default mirror configuration"""
        return {
            "default_regions": ["cn", "global"],
            "package_managers": {}
        }
    
    # ============================================
    # Mirror selection and management
    # ============================================
    
    def get_mirrors_for_package_manager(self, pm_type: str, region: Optional[str] = None) -> List[MirrorInfo]:
        """Get mirrors for a specific package manager - FIXED to match config structure"""
        region = region or self.current_region
        
        # Navigate the config structure correctly
        pm_config = self.mirrors_config.get("package_managers", {}).get(pm_type, {})
        region_config = pm_config.get(region, {})
        mirrors_list = region_config.get("mirrors", [])
        
        results = []
        
        for idx, mirror_data in enumerate(mirrors_list):
            if isinstance(mirror_data, dict):
                url = mirror_data.get('url', '')
                name = mirror_data.get('name', f"Mirror {idx}")
                priority = mirror_data.get('priority', idx + 1)
            else:
                url = str(mirror_data)
                name = f"Mirror {idx}"
                priority = idx + 1
            
            if url:
                results.append(MirrorInfo(url=url, name=name, priority=priority, region=region))
        
        # Sort by priority
        results.sort(key=lambda m: m.priority)
        return results
    
    def get_best_mirror(self, pm_type: str, region: Optional[str] = None) -> Optional[MirrorInfo]:
        """Get the best mirror for a package manager"""
        mirrors = self.get_mirrors_for_package_manager(pm_type, region)
        if mirrors:
            return mirrors[0]  # Highest priority
        return None
    
    def test_mirror_speed(self, url: str, timeout: int = 3) -> Optional[float]:
        """Test mirror download speed (returns time in seconds)"""
        try:
            start = datetime.now()
            
            if requests:
                response = requests.head(url, timeout=timeout, allow_redirects=True)
                end = datetime.now()
                if response.status_code in (200, 301, 302, 304):
                    speed = (end - start).total_seconds()
                    logger.debug(f"Mirror {url} speed: {speed:.2f}s")
                    return speed
                return None
            else:
                parsed_url = urllib.parse.urlparse(url)
                conn = None
                
                if parsed_url.scheme == 'https':
                    conn = http.client.HTTPSConnection(parsed_url.netloc, timeout=timeout)
                else:
                    conn = http.client.HTTPConnection(parsed_url.netloc, timeout=timeout)
                
                conn.request('HEAD', parsed_url.path or '/')
                response = conn.getresponse()
                end = datetime.now()
                
                if response.status in (200, 301, 302, 304):
                    speed = (end - start).total_seconds()
                    logger.debug(f"Mirror {url} speed: {speed:.2f}s")
                    conn.close()
                    return speed
                
                conn.close()
                return None
                
        except Exception as e:
            logger.debug(f"Failed to test {url}: {e}")
            return None
    
    def find_fastest_mirror(self, pm_type: str, region: Optional[str] = None) -> Optional[MirrorInfo]:
        """Test and find the fastest mirror"""
        mirrors = self.get_mirrors_for_package_manager(pm_type, region)
        if not mirrors:
            return None
        
        fastest_mirror = None
        fastest_time = float('inf')
        
        for mirror in mirrors:
            time_taken = self.test_mirror_speed(mirror.url)
            if time_taken and time_taken < fastest_time:
                fastest_time = time_taken
                fastest_mirror = mirror
        
        if fastest_mirror:
            logger.info(f"Fastest mirror: {fastest_mirror.name} ({fastest_mirror.url}) - {fastest_time:.2f}s")
        
        return fastest_mirror
    
    def get_mirror_url_for_pm(self, pm_type: str, region: Optional[str] = None) -> str:
        """Get the best mirror URL for a package manager"""
        mirror = self.get_best_mirror(pm_type, region)
        if mirror:
            return mirror.url
        return ""
    
    # ============================================
    # Tool query and management
    # ============================================
    
    def load_tools(self):
        """Load all tool definitions from YAML files"""
        if not self.tools_dir.exists():
            logger.warning(f"Tools directory not found: {self.tools_dir}")
            return
        
        for tool_path in self.tools_dir.rglob("tool.yaml"):
            try:
                with open(tool_path, 'r', encoding='utf-8') as f:
                    tool_data = yaml.safe_load(f)
                    if tool_data and tool_data.get('name'):
                        tool_name = tool_data['name']
                        category_parts = tool_path.parts
                        if len(category_parts) >= 2:
                            tool_data['category'] = category_parts[-2]
                        tool_data['path'] = str(tool_path)
                        self.tools[tool_name] = tool_data
                        logger.debug(f"Loaded tool: {tool_name}")
            except Exception as e:
                logger.error(f"Failed to load {tool_path}: {e}")
        
        logger.info(f"Loaded {len(self.tools)} tools")
    
    def load_templates(self):
        """Load all environment templates"""
        if not self.templates_dir.exists():
            logger.warning(f"Templates directory not found: {self.templates_dir}")
            return
        
        for template_path in self.templates_dir.glob("*.yaml"):
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_data = yaml.safe_load(f)
                    if template_data and template_data.get('name'):
                        template_name = template_data['name']
                        template_data['path'] = str(template_path)
                        self.templates[template_name] = template_data
                        logger.debug(f"Loaded template: {template_name}")
            except Exception as e:
                logger.error(f"Failed to load {template_path}: {e}")
        
        logger.info(f"Loaded {len(self.templates)} templates")
    
    def list_tools(self) -> List[str]:
        """Get list of all available tool names"""
        return sorted(list(self.tools.keys()))
    
    def list_categories(self) -> List[str]:
        """Get list of all tool categories"""
        categories = set()
        for tool in self.tools.values():
            categories.add(tool.get('category', 'other'))
        return sorted(list(categories))
    
    def get_tool(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed tool information"""
        return self.tools.get(tool_name)
    
    def search_tools(self, keyword: str) -> List[Dict[str, Any]]:
        """Search tools by keyword"""
        keyword_lower = keyword.lower()
        results = []
        
        for tool_name, tool in self.tools.items():
            name_match = keyword_lower in tool.get('name', '').lower()
            desc_match = keyword_lower in tool.get('description', '').lower()
            tags_match = any(keyword_lower in tag.lower() for tag in tool.get('tags', []))
            
            if name_match or desc_match or tags_match:
                results.append(tool)
        
        return results
    
    def get_tools_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get tools in a category"""
        return [tool for tool in self.tools.values() if tool.get('category') == category]
    
    # ============================================
    # Installation command generation - FIXED
    # ============================================
    
    def _replace_template_variables(self, command: str, tool_name: str, os_type: str, region: str) -> str:
        """Replace template variables in command with actual values"""
        tool = self.get_tool(tool_name)
        
        # Get mirror URLs
        pm_type = self._detect_package_manager_type(tool)
        mirror_url = self.get_mirror_url_for_pm(pm_type, region) if pm_type else ""
        
        # Get default version
        default_version = "latest"
        if tool and 'versions' in tool and tool['versions']:
            for v in tool['versions']:
                if v.get('is_default', False):
                    default_version = v.get('version', 'latest')
                    break
            if default_version == 'latest' and tool['versions']:
                default_version = tool['versions'][0].get('version', 'latest')
        
        # Replace common template variables
        replacements = {
            '{{mirror_url}}': mirror_url,
            '{{version}}': default_version,
            '{{os}}': os_type,
            '{{region}}': region,
            '{{package_name}}': tool.get('installation_sources', [{}])[0].get('package_name', tool_name) if tool else tool_name,
        }
        
        result = command
        for key, value in replacements.items():
            result = result.replace(key, str(value))
        
        return result
    
    def _detect_package_manager_type(self, tool: Optional[Dict[str, Any]]) -> Optional[str]:
        """Detect the package manager type from tool definition"""
        if not tool:
            return None
        
        # Check installation_sources for type
        sources = tool.get('installation_sources', [])
        for source in sources:
            src_type = source.get('type', '')
            if 'pip' in src_type:
                return 'pip'
            elif 'npm' in src_type or 'node' in src_type:
                return 'npm'
            elif 'apt' in src_type:
                return 'apt'
            elif 'brew' in src_type:
                return 'brew'
            elif 'docker' in src_type:
                return 'docker'
            elif 'cargo' in src_type:
                return 'cargo'
            elif 'go' in src_type:
                return 'go'
        
        # Check tags
        tags = tool.get('tags', [])
        if 'python' in tags:
            return 'pip'
        elif 'nodejs' in tags or 'javascript' in tags:
            return 'npm'
        elif 'rust' in tags:
            return 'cargo'
        
        return None
    
    def get_installation_command(
        self, 
        tool_name: str, 
        os_type: str = "linux",
        region: Optional[str] = None,
        version: Optional[str] = None
    ) -> Optional[str]:
        """Get the best installation command for a tool - FIXED with template variable replacement"""
        region = region or self.current_region
        tool = self.get_tool(tool_name)
        
        if not tool:
            logger.warning(f"Tool '{tool_name}' not found")
            return None
        
        sources = tool.get('installation_sources', [])
        
        # Find best source based on OS and region
        best_source = None
        
        for source in sources:
            # Check OS support
            source_os = source.get('os', [])
            if source_os and os_type not in source_os and 'all' not in source_os:
                continue
            
            # Check region preference
            regions_pref = source.get('region_preference', [])
            if regions_pref:
                if region in regions_pref:
                    best_source = source
                    break
                elif region == 'cn' and 'global' in regions_pref:
                    best_source = source
                    break
            
            if not best_source:
                best_source = source
        
        if not best_source:
            logger.warning(f"No installation source found for {tool_name} on {os_type}")
            return None
        
        # Get the command
        command = best_source.get('command', '')
        
        if not command:
            # Generate command based on type
            source_type = best_source.get('type', '')
            package_name = best_source.get('package_name', tool_name)
            
            if 'apt' in source_type:
                command = f"sudo apt update && sudo apt install -y {package_name}"
            elif 'brew' in source_type:
                command = f"brew install {package_name}"
            elif 'pip' in source_type:
                pip_mirror = self.get_best_mirror('pip', region)
                index_url = pip_mirror.url if pip_mirror else 'https://pypi.org/simple'
                command = f"pip install -i {index_url} {package_name}"
            elif 'npm' in source_type or 'node' in source_type:
                npm_mirror = self.get_best_mirror('npm', region)
                registry = npm_mirror.url if npm_mirror else 'https://registry.npmjs.org'
                command = f"npm install -g --registry={registry} {package_name}"
            elif 'cargo' in source_type:
                command = f"cargo install {package_name}"
            elif 'go' in source_type:
                command = f"go install {package_name}@latest"
        
        # Replace template variables - THIS IS THE KEY FIX
        if command:
            command = self._replace_template_variables(command, tool_name, os_type, region)
        
        return command
    
    def generate_install_script(
        self, 
        tool_names: List[str], 
        os_type: str = "linux",
        region: Optional[str] = None,
        auto_fallback: bool = True
    ) -> str:
        """Generate complete installation script - FIXED"""
        region = region or self.current_region
        script_lines = [
            "#!/bin/bash",
            f"# Global-Dev-Setup - Auto-generated Installation Script",
            f"# Region: {region}",
            f"# OS: {os_type}",
            f"# Generated: {datetime.now().isoformat()}",
            "",
            "set -e",
            "",
            "# Utility functions",
            "log_info() { echo \"[INFO] $1\"; }",
            "log_error() { echo \"[ERROR] $1\"; }",
            "",
        ]
        
        for tool_name in tool_names:
            command = self.get_installation_command(tool_name, os_type, region)
            
            if command:
                script_lines.append(f"# Install: {tool_name}")
                script_lines.append(f"log_info \"Installing {tool_name}...\"")
                # Wrap command properly
                script_lines.append(f"{command}")
                script_lines.append(f"log_info \"Successfully installed {tool_name}\"")
                script_lines.append("")
            else:
                script_lines.append(f"# Warning: No installation command found for {tool_name}")
                script_lines.append(f"log_error \"Tool '{tool_name}' not found\"")
                script_lines.append("")
        
        script_lines.append("log_info \"Installation process completed\"")
        
        return "\n".join(script_lines)
    
    # ============================================
    # Template management
    # ============================================
    
    def list_templates(self) -> List[str]:
        """List all templates"""
        return sorted(list(self.templates.keys()))
    
    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get template details"""
        return self.templates.get(template_name)
    
    def get_template_tools(self, template_name: str) -> List[Dict[str, Any]]:
        """Get tools in a template"""
        template = self.get_template(template_name)
        if not template:
            return []
        
        all_tools = []
        
        # Try different field names for tools
        tool_fields = ['core_tools', 'required_tools', 'recommended_tools', 'ml_tools', 'optional_tools']
        
        for field in tool_fields:
            tools_list = template.get(field, [])
            if isinstance(tools_list, list):
                for tool_info in tools_list:
                    if isinstance(tool_info, dict):
                        tool_name = tool_info.get('name', '')
                    else:
                        tool_name = str(tool_info)
                    
                    tool_data = self.get_tool(tool_name)
                    if tool_data:
                        all_tools.append({
                            'tool': tool_data,
                            'type': field,
                            'version': tool_info.get('version') if isinstance(tool_info, dict) else None
                        })
                    else:
                        logger.warning(f"Tool '{tool_name}' referenced in template '{template_name}' not found")
        
        return all_tools
    
    # ============================================
    # Export and serialization
    # ============================================
    
    def export_to_json(self, output_file: str = "tool_registry.json"):
        """Export registry to JSON"""
        data = {
            "tools": self.tools,
            "templates": self.templates,
            "categories": self.list_categories(),
            "mirrors_config": self.mirrors_config,
            "current_region": self.current_region,
            "export_time": datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Registry exported to {output_file}")
        return output_file
    
    # ============================================
    # Validation methods
    # ============================================
    
    def validate_tool(self, tool_name: str) -> Dict[str, Any]:
        """Validate a tool definition"""
        tool = self.get_tool(tool_name)
        if not tool:
            return {'valid': False, 'errors': ['Tool not found']}
        
        errors = []
        warnings = []
        
        # Check required fields
        required_fields = ['name', 'category', 'description', 'homepage', 'tags', 'supported_os', 'installation_sources']
        for field in required_fields:
            if field not in tool or not tool[field]:
                errors.append(f"Missing required field: {field}")
        
        # Check installation_sources
        if 'installation_sources' in tool:
            sources = tool['installation_sources']
            if not isinstance(sources, list) or len(sources) == 0:
                errors.append("installation_sources must be a non-empty list")
            else:
                for idx, source in enumerate(sources):
                    if 'type' not in source:
                        errors.append(f"installation_sources[{idx}] missing 'type'")
                    if 'description' not in source:
                        warnings.append(f"installation_sources[{idx}] missing 'description'")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def validate_all_tools(self) -> Dict[str, Any]:
        """Validate all tools"""
        results = {
            'total': len(self.tools),
            'valid': 0,
            'invalid': 0,
            'tools': {}
        }
        
        for tool_name in self.list_tools():
            validation = self.validate_tool(tool_name)
            results['tools'][tool_name] = validation
            if validation['valid']:
                results['valid'] += 1
            else:
                results['invalid'] += 1
        
        return results
    
    def validate_template_references(self, template_name: str) -> Dict[str, Any]:
        """Validate that all tools referenced in a template exist"""
        template = self.get_template(template_name)
        if not template:
            return {'valid': False, 'errors': ['Template not found']}
        
        errors = []
        referenced_tools = self.get_template_tools(template_name)
        referenced_names = [t['tool']['name'] for t in referenced_tools]
        
        # Check for missing tools
        template_tools = []
        for field in ['core_tools', 'required_tools', 'recommended_tools', 'ml_tools', 'optional_tools']:
            tools_list = template.get(field, [])
            for tool_info in tools_list:
                if isinstance(tool_info, dict):
                    template_tools.append(tool_info.get('name', ''))
                else:
                    template_tools.append(str(tool_info))
        
        for tool_name in template_tools:
            if tool_name not in self.tools:
                errors.append(f"Referenced tool '{tool_name}' does not exist")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'referenced_tools': referenced_names
        }


# Simple CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Global-Dev-Setup Enhanced Registry")
    parser.add_argument("--list-tools", action="store_true", help="List all tools")
    parser.add_argument("--list-categories", action="store_true", help="List all categories")
    parser.add_argument("--list-templates", action="store_true", help="List all templates")
    parser.add_argument("--tool", type=str, help="Get tool details")
    parser.add_argument("--template", type=str, help="Get template details")
    parser.add_argument("--search", type=str, help="Search tools by keyword")
    parser.add_argument("--category", type=str, help="Get tools by category")
    parser.add_argument("--install-cmd", type=str, help="Get install command for tool")
    parser.add_argument("--region", type=str, choices=["cn", "global"], help="Set region: cn or global")
    parser.add_argument("--export", action="store_true", help="Export registry to JSON")
    parser.add_argument("--gen-script", type=str, help="Generate install script (comma-separated tools)")
    parser.add_argument("--os", type=str, default="linux", help="OS type (linux, macos, windows)")
    parser.add_argument("--test-mirror", type=str, help="Test mirror for package manager")
    parser.add_argument("--validate", action="store_true", help="Validate all tools")
    parser.add_argument("--validate-template", type=str, help="Validate template references")
    
    args = parser.parse_args()
    
    registry = ToolRegistry()
    
    if args.region:
        registry.set_region(args.region)
        print(f"Region set to: {args.region}")
    
    if args.validate:
        print("Validating all tools...")
        results = registry.validate_all_tools()
        print(f"Total: {results['total']}, Valid: {results['valid']}, Invalid: {results['invalid']}")
        for tool_name, validation in results['tools'].items():
            if not validation['valid']:
                print(f"\n{tool_name}: INVALID")
                for error in validation['errors']:
                    print(f"  - {error}")
        print("\nValidation complete.")
    
    elif args.validate_template:
        print(f"Validating template: {args.validate_template}")
        result = registry.validate_template_references(args.validate_template)
        if result['valid']:
            print("Template references are valid!")
        else:
            print("Template has invalid references:")
            for error in result['errors']:
                print(f"  - {error}")
    
    elif args.test_mirror:
        print(f"Testing mirror for: {args.test_mirror}")
        mirror = registry.get_best_mirror(args.test_mirror)
        if mirror:
            print(f"Best mirror: {mirror.name} - {mirror.url}")
            speed = registry.test_mirror_speed(mirror.url)
            if speed:
                print(f"Speed: {speed:.2f}s")
        else:
            print("No mirrors found")
    
    elif args.list_tools:
        print("Available tools:")
        for tool in registry.list_tools():
            print(f"  - {tool}")
    
    elif args.list_categories:
        print("Available categories:")
        for cat in registry.list_categories():
            print(f"  - {cat}")
    
    elif args.list_templates:
        print("Available templates:")
        for t in registry.list_templates():
            template = registry.get_template(t)
            desc = template.get('description', '') if template else ''
            print(f"  - {t}: {desc}")
    
    elif args.tool:
        tool = registry.get_tool(args.tool)
        if tool:
            print(json.dumps(tool, ensure_ascii=False, indent=2))
        else:
            print(f"Tool '{args.tool}' not found")
    
    elif args.template:
        template = registry.get_template(args.template)
        if template:
            print(json.dumps(template, ensure_ascii=False, indent=2))
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
    
    elif args.install_cmd:
        cmd = registry.get_installation_command(args.install_cmd, args.os)
        if cmd:
            print(cmd)
        else:
            print(f"No installation command found for '{args.install_cmd}'")
    
    elif args.gen_script:
        tool_list = [t.strip() for t in args.gen_script.split(',')]
        script = registry.generate_install_script(tool_list, args.os)
        print(script)
    
    elif args.export:
        registry.export_to_json()
        print("Registry exported to tool_registry.json")
    
    else:
        parser.print_help()
