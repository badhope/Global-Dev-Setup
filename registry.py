# Global-Dev-Setup - Enhanced Tool Registry with Mirror Support
# Provides query, download, and installation with automatic mirror selection

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
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

logger = None

# Optional requests import
requests = None
try:
    import requests
except ImportError:
    pass

try:
    from core.utils.logger import get_logger
    logger = get_logger("registry")
except ImportError:
    # Fallback to simple logging
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("registry")

class Region(Enum):
    """Supported region configurations"""
    GLOBAL = "global"
    CN = "cn"

@dataclass
class MirrorInfo:
    """Mirror information"""
    url: str
    name: str
    priority: int
    region: Region

@dataclass
class ToolVersion:
    """Tool version information"""
    version: str
    aliases: List[str]
    description: str
    supported_os: List[str]
    download_urls: Dict[str, Dict[str, str]]  # {region: {os: url}}
    is_default: bool = False

class ToolRegistry:
    """Enhanced registry with mirror support and version management"""
    
    def __init__(
        self, 
        tools_dir: str = "tools", 
        templates_dir: str = "environment-templates",
        mirrors_config_file: str = "mirrors_config.yaml",
        auto_detect_region: bool = True,
        preferred_region: Optional[Region] = None
    ):
        self.tools_dir = Path(tools_dir)
        self.templates_dir = Path(templates_dir)
        self.mirrors_config_file = Path(mirrors_config_file)
        
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.mirrors_config: Dict[str, Any] = {}
        
        # Region management
        self.current_region: Region = preferred_region or Region.GLOBAL
        if auto_detect_region and preferred_region is None:
            self.current_region = self._detect_region()
        
        self.load_mirrors_config()
        self.load_tools()
        self.load_templates()
    
    def load_mirrors_config(self):
        """Load mirror configuration file"""
        if not self.mirrors_config_file.exists():
            logger.warning("Mirror config file not found, using defaults")
            self.mirrors_config = self._get_default_mirrors_config()
            return
        
        try:
            with open(self.mirrors_config_file, 'r', encoding='utf-8') as f:
                self.mirrors_config = yaml.safe_load(f)
            logger.info(f"Mirror config loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load mirror config: {e}")
            self.mirrors_config = self._get_default_mirrors_config()
    
    def _get_default_mirrors_config(self):
        """Get default mirror configuration"""
        return {
            "default_regions": ["cn", "global"],
            "default_mirrors": {
                "cn": {"name": "China Mirror", "description": "Mirrors for China", "priority": 10},
                "global": {"name": "Global Official", "description": "Official sources", "priority": 1}
            },
            "package_managers": {}
        }
    
    def _detect_region(self) -> Region:
        """Detect the current region automatically"""
        try:
            # Try to check IP location or network
            # Simple detection: check if common CN domains are fast
            try:
                # Quick check for baidu.com
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
        except Exception as e:
            logger.warning(f"Failed to detect region: {e}, defaulting to GLOBAL")
            return Region.GLOBAL
    
    def set_region(self, region: Union[Region, str]):
        """Set the current region"""
        if isinstance(region, str):
            region = Region(region.lower())
        self.current_region = region
        logger.info(f"Region set to: {self.current_region.value}")
    
    def get_region(self) -> Region:
        """Get current region"""
        return self.current_region
    
    def load_tools(self):
        """Load all tool definitions from YAML files"""
        if not self.tools_dir.exists():
            logger.warning(f"Tools directory not found: {self.tools_dir}")
            return
        
        # Recursively find tool.yaml files
        for tool_path in self.tools_dir.rglob("tool.yaml"):
            try:
                with open(tool_path, 'r', encoding='utf-8') as f:
                    tool_data = yaml.safe_load(f)
                    if tool_data and tool_data.get('name'):
                        tool_name = tool_data['name']
                        # Add category from directory structure
                        category_parts = tool_path.parts
                        if len(category_parts) >= 2:
                            # Parent directory is category
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
    
    # ============================================
    # Mirror selection and management
    # ============================================
    
    def get_mirrors_for_package_manager(self, pm_type: str, region: Optional[Region] = None) -> List[MirrorInfo]:
        """Get mirrors for a specific package manager"""
        region = region or self.current_region
        region_str = region.value
        
        pm_config = self.mirrors_config.get("package_managers", {}).get(pm_type, {})
        
        mirrors_list = pm_config.get(region_str, {}).get("mirrors", [])
        results = []
        
        for idx, mirror_data in enumerate(mirrors_list):
            url = mirror_data if isinstance(mirror_data, str) else mirror_data.get('url', '')
            name = mirror_data.get('name', f"Mirror {idx}") if isinstance(mirror_data, dict) else url
            priority = mirror_data.get('priority', idx) if isinstance(mirror_data, dict) else idx
            
            results.append(MirrorInfo(url=url, name=name, priority=priority, region=region))
        
        return sorted(results, key=lambda m: m.priority)
    
    def get_best_mirror(self, pm_type: str, region: Optional[Region] = None) -> Optional[MirrorInfo]:
        """Get the best mirror for a package manager"""
        mirrors = self.get_mirrors_for_package_manager(pm_type, region)
        if mirrors:
            return mirrors[0]  # Highest priority
        return None
    
    def test_mirror_speed(self, url: str, timeout: int = 3) -> Optional[float]:
        """Test mirror download speed (returns time in seconds)"""
        try:
            start = datetime.now()
            
            # Use requests if available
            if requests:
                response = requests.head(url, timeout=timeout, allow_redirects=True)
                end = datetime.now()
                if response.status_code in (200, 301, 302, 304):
                    speed = (end - start).total_seconds()
                    logger.debug(f"Mirror {url} speed: {speed:.2f}s")
                    return speed
                return None
            else:
                # Fallback to http.client
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
    
    def find_fastest_mirror(self, pm_type: str, region: Optional[Region] = None) -> Optional[MirrorInfo]:
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
    
    # ============================================
    # Tool query and management
    # ============================================
    
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
    
    def get_tool_versions(self, tool_name: str) -> List[ToolVersion]:
        """Get available versions for a tool"""
        tool = self.get_tool(tool_name)
        if not tool:
            return []
        
        versions_data = tool.get('versions', [])
        versions = []
        
        for v_data in versions_data:
            tool_version = ToolVersion(
                version=v_data.get('version', ''),
                aliases=v_data.get('alias', []),
                description=v_data.get('description', ''),
                supported_os=v_data.get('supported_os', []),
                download_urls=v_data.get('download_urls', {}),
                is_default=v_data.get('is_default', False)
            )
            versions.append(tool_version)
        
        return versions
    
    def get_default_version(self, tool_name: str) -> Optional[ToolVersion]:
        """Get default version for a tool"""
        versions = self.get_tool_versions(tool_name)
        for v in versions:
            if v.is_default:
                return v
        return versions[0] if versions else None
    
    def get_download_url(
        self, 
        tool_name: str, 
        version: Optional[str] = None,
        os: str = "linux",
        region: Optional[Region] = None
    ) -> Optional[str]:
        """Get download URL for a specific tool version and region"""
        region = region or self.current_region
        tool_version = None
        
        if version:
            versions = self.get_tool_versions(tool_name)
            for v in versions:
                if v.version == version or version in v.aliases:
                    tool_version = v
                    break
        else:
            tool_version = self.get_default_version(tool_name)
        
        if not tool_version:
            return None
        
        # Get URL for region and OS
        urls = tool_version.download_urls.get(region.value, {})
        url = urls.get(os)
        
        if not url:
            # Fallback to global
            urls = tool_version.download_urls.get('global', {})
            url = urls.get(os)
        
        return url
    
    # ============================================
    # Installation command generation
    # ============================================
    
    def get_installation_command(
        self, 
        tool_name: str, 
        os_type: str = "linux",
        region: Optional[Region] = None,
        version: Optional[str] = None
    ) -> Optional[str]:
        """Get the best installation command for a tool"""
        region = region or self.current_region
        tool = self.get_tool(tool_name)
        if not tool:
            return None
        
        sources = tool.get('installation_sources', [])
        
        # Find best source
        best_source = None
        
        for source in sources:
            # Check OS support
            source_os = source.get('os', [])
            if source_os and os_type not in source_os and 'all' not in source_os:
                continue
            
            # Check region preference
            regions_pref = source.get('region_preference', [])
            if regions_pref:
                region_str = region.value
                if region_str in regions_pref:
                    best_source = source
                    break
            
            if not best_source:
                best_source = source
        
        if not best_source:
            return None
        
        # Check for command
        command = best_source.get('command')
        
        if not command:
            # Generate command based on type
            source_type = best_source.get('type')
            package_name = best_source.get('package_name')
            
            if source_type == 'apt' and package_name:
                command = f"sudo apt update && sudo apt install -y {package_name}"
            elif source_type == 'brew' and package_name:
                command = f"brew install {package_name}"
            elif source_type == 'pip' and package_name:
                pip_mirror = self.get_best_mirror('pip', region)
                index_url = pip_mirror.url if pip_mirror else 'https://pypi.org/simple'
                command = f"pip install -i {index_url} {package_name}"
            elif source_type == 'npm' and package_name:
                npm_mirror = self.get_best_mirror('npm', region)
                registry = npm_mirror.url if npm_mirror else 'https://registry.npmjs.org'
                command = f"npm install -g --registry={registry} {package_name}"
        
        return command
    
    def generate_install_script(
        self, 
        tool_names: List[str], 
        os_type: str = "linux",
        region: Optional[Region] = None,
        auto_fallback: bool = True
    ) -> str:
        """Generate complete installation script"""
        region = region or self.current_region
        script_lines = [
            "#!/bin/bash",
            f"# Global-Dev-Setup - Auto-generated Installation Script",
            f"# Region: {region.value}",
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
                script_lines.append(f"if {command}; then")
                script_lines.append(f"    log_info \"Successfully installed {tool_name}\"")
                script_lines.append("else")
                script_lines.append(f"    log_error \"Failed to install {tool_name}\"")
                
                if auto_fallback:
                    script_lines.append("    # Try alternative sources...")
                
                script_lines.append("fi")
                script_lines.append("")
            else:
                script_lines.append(f"# Warning: No installation command found for {tool_name}")
                script_lines.append("")
        
        script_lines.append("log_info \"Installation process completed\"")
        script_lines.append("exit 0")
        
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
        
        for tool_info in template.get('required_tools', []):
            tool_data = self.get_tool(tool_info.get('name', ''))
            if tool_data:
                all_tools.append({
                    'tool': tool_data,
                    'type': 'required',
                    'version': tool_info.get('version')
                })
        
        for tool_info in template.get('recommended_tools', []):
            tool_data = self.get_tool(tool_info.get('name', ''))
            if tool_data:
                all_tools.append({
                    'tool': tool_data,
                    'type': 'recommended',
                    'version': tool_info.get('version')
                })
        
        for tool_info in template.get('optional_tools', []):
            tool_data = self.get_tool(tool_info.get('name', ''))
            if tool_data:
                all_tools.append({
                    'tool': tool_data,
                    'type': 'optional',
                    'version': tool_info.get('version')
                })
        
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
            "current_region": self.current_region.value,
            "export_time": datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Registry exported to {output_file}")
        return output_file

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
    parser.add_argument("--list-versions", type=str, help="List versions for tool")
    parser.add_argument("--test-mirrors", type=str, help="Test mirrors for package manager")
    parser.add_argument("--export", action="store_true", help="Export registry to JSON")
    parser.add_argument("--gen-script", type=str, help="Generate install script (comma-separated tools)")
    parser.add_argument("--os", type=str, default="linux", help="OS type (linux, macos, windows)")
    
    args = parser.parse_args()
    
    registry = ToolRegistry()
    
    if args.region:
        registry.set_region(args.region)
        print(f"Region set to: {args.region}")
    
    if args.list_tools:
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
    
    elif args.list_versions:
        versions = registry.get_tool_versions(args.list_versions)
        print(f"Versions for {args.list_versions}:")
        for v in versions:
            default = " [DEFAULT]" if v.is_default else ""
            print(f"  - v{v.version}{default}: {v.description}")
    
    elif args.test_mirrors:
        print(f"Testing mirrors for {args.test_mirrors}...")
        fastest = registry.find_fastest_mirror(args.test_mirrors)
        if fastest:
            print(f"Fastest mirror: {fastest.name} ({fastest.url})")
        else:
            print("No working mirrors found")
    
    elif args.gen_script:
        tool_list = [t.strip() for t in args.gen_script.split(',')]
        script = registry.generate_install_script(tool_list, args.os)
        print(script)
    
    elif args.export:
        registry.export_to_json()
    
    else:
        parser.print_help()
