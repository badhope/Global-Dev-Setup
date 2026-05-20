#!/usr/bin/env python3
# Global-Dev-Setup - Tool Validation Script
# Validates all tool definitions and template references

import sys
import os
from pathlib import Path
import yaml
from typing import Dict, List, Any

# Colors for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_error(msg):
    print(f"{Colors.RED}❌ ERROR: {msg}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  WARNING: {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

class Validator:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.tools_dir = self.root_dir / "tools"
        self.templates_dir = self.root_dir / "environment-templates"
        self.mirrors_config = self.root_dir / "mirrors_config.yaml"
        
        self.tools: Dict[str, Dict] = {}
        self.templates: Dict[str, Dict] = {}
        
        self.total_tools = 0
        self.valid_tools = 0
        self.invalid_tools = 0
        
        self.total_templates = 0
        self.valid_templates = 0
        self.invalid_templates = 0
        
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def load_tools(self):
        """Load all tool definitions"""
        print_info("Loading tools...")
        
        if not self.tools_dir.exists():
            print_error(f"Tools directory not found: {self.tools_dir}")
            return
        
        for tool_path in self.tools_dir.rglob("tool.yaml"):
            try:
                with open(tool_path, 'r', encoding='utf-8') as f:
                    tool_data = yaml.safe_load(f)
                    if tool_data and tool_data.get('name'):
                        self.tools[tool_data['name']] = tool_data
            except Exception as e:
                self.errors.append(f"Failed to load {tool_path}: {e}")
        
        self.total_tools = len(self.tools)
        print_success(f"Loaded {self.total_tools} tools")
    
    def load_templates(self):
        """Load all environment templates"""
        print_info("Loading templates...")
        
        if not self.templates_dir.exists():
            print_error(f"Templates directory not found: {self.templates_dir}")
            return
        
        for template_path in self.templates_dir.glob("*.yaml"):
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_data = yaml.safe_load(f)
                    if template_data and template_data.get('name'):
                        self.templates[template_data['name']] = template_data
            except Exception as e:
                self.errors.append(f"Failed to load {template_path}: {e}")
        
        self.total_templates = len(self.templates)
        print_success(f"Loaded {self.total_templates} templates")
    
    def validate_tool_fields(self, tool_name: str, tool: Dict) -> bool:
        """Validate required fields in tool definition"""
        required_fields = [
            'name', 'category', 'description', 
            'homepage', 'tags', 'supported_os', 'installation_sources'
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in tool or not tool[field]:
                missing_fields.append(field)
        
        if missing_fields:
            self.errors.append(f"Tool '{tool_name}' missing fields: {', '.join(missing_fields)}")
            return False
        
        return True
    
    def validate_installation_sources(self, tool_name: str, sources: List) -> bool:
        """Validate installation_sources structure"""
        if not isinstance(sources, list) or len(sources) == 0:
            self.errors.append(f"Tool '{tool_name}' has empty installation_sources")
            return False
        
        valid = True
        for idx, source in enumerate(sources):
            if not isinstance(source, dict):
                self.errors.append(f"Tool '{tool_name}' installation_sources[{idx}] is not a dict")
                valid = False
                continue
            
            if 'type' not in source:
                self.warnings.append(f"Tool '{tool_name}' installation_sources[{idx}] missing 'type'")
            
            if 'description' not in source:
                self.warnings.append(f"Tool '{tool_name}' installation_sources[{idx}] missing 'description'")
        
        return valid
    
    def validate_all_tools(self):
        """Validate all tool definitions"""
        print_info("Validating all tools...")
        print()
        
        for tool_name, tool in self.tools.items():
            if self.validate_tool_fields(tool_name, tool):
                sources = tool.get('installation_sources', [])
                if self.validate_installation_sources(tool_name, sources):
                    self.valid_tools += 1
                else:
                    self.invalid_tools += 1
            else:
                self.invalid_tools += 1
        
        print()
        print(f"{Colors.BOLD}Tool Validation Results:{Colors.END}")
        print_success(f"Valid: {self.valid_tools}/{self.total_tools}")
        if self.invalid_tools > 0:
            print_error(f"Invalid: {self.invalid_tools}/{self.total_tools}")
        print()
    
    def validate_template_references(self):
        """Validate that all tools referenced in templates exist"""
        print_info("Validating template tool references...")
        print()
        
        template_tool_fields = ['core_tools', 'required_tools', 'recommended_tools', 'ml_tools', 'optional_tools']
        
        for template_name, template in self.templates.items():
            missing_tools = []
            
            for field in template_tool_fields:
                tools_list = template.get(field, [])
                if not isinstance(tools_list, list):
                    continue
                
                for tool_info in tools_list:
                    if isinstance(tool_info, dict):
                        tool_name = tool_info.get('name', '')
                    else:
                        tool_name = str(tool_info)
                    
                    if tool_name and tool_name not in self.tools:
                        missing_tools.append(tool_name)
            
            if missing_tools:
                self.errors.append(f"Template '{template_name}' references non-existent tools: {', '.join(missing_tools)}")
                self.invalid_templates += 1
            else:
                self.valid_templates += 1
        
        print()
        print(f"{Colors.BOLD}Template Validation Results:{Colors.END}")
        print_success(f"Valid: {self.valid_templates}/{self.total_templates}")
        if self.invalid_templates > 0:
            print_error(f"Invalid: {self.invalid_templates}/{self.total_templates}")
        print()
    
    def validate_mirrors_config(self):
        """Validate mirrors configuration"""
        print_info("Validating mirrors configuration...")
        print()
        
        if not self.mirrors_config.exists():
            self.errors.append("mirrors_config.yaml not found")
            return
        
        try:
            with open(self.mirrors_config, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if not config:
                self.errors.append("mirrors_config.yaml is empty")
                return
            
            pm = config.get('package_managers', {})
            if not pm:
                self.errors.append("No package_managers in mirrors_config.yaml")
                return
            
            print_success(f"Found {len(pm)} package managers configured")
            
            # Check for CN mirrors
            for pm_name, pm_config in pm.items():
                cn_mirrors = pm_config.get('cn', {}).get('mirrors', [])
                global_mirrors = pm_config.get('global', {}).get('mirrors', [])
                
                if not cn_mirrors:
                    self.warnings.append(f"Package manager '{pm_name}' has no CN mirrors")
                
                if not global_mirrors:
                    self.warnings.append(f"Package manager '{pm_name}' has no global mirrors")
            
            print_success("Mirrors configuration is valid")
            
        except Exception as e:
            self.errors.append(f"Failed to parse mirrors_config.yaml: {e}")
        
        print()
    
    def print_report(self):
        """Print final validation report"""
        print()
        print("=" * 70)
        print(f"{Colors.BOLD}FINAL VALIDATION REPORT{Colors.END}")
        print("=" * 70)
        print()
        
        if self.errors:
            print(f"{Colors.BOLD}ERRORS ({len(self.errors)}):{Colors.END}")
            for error in self.errors:
                print_error(error)
            print()
        
        if self.warnings:
            print(f"{Colors.BOLD}WARNINGS ({len(self.warnings)}):{Colors.END}")
            for warning in self.warnings:
                print_warning(warning)
            print()
        
        if not self.errors and not self.warnings:
            print_success("✅ ALL VALIDATIONS PASSED!")
        elif self.errors:
            print_error(f"❌ VALIDATION FAILED with {len(self.errors)} errors")
        else:
            print_warning(f"⚠️  VALIDATION COMPLETED with {len(self.warnings)} warnings")
        
        print()
        print(f"Total Tools: {self.total_tools}")
        print(f"Total Templates: {self.total_templates}")
        print()
        
        return len(self.errors) == 0
    
    def run(self):
        """Run all validations"""
        print()
        print("=" * 70)
        print(f"{Colors.BOLD}Global-Dev-Setup Validation System{Colors.END}")
        print("=" * 70)
        print()
        
        self.load_tools()
        self.load_templates()
        self.validate_all_tools()
        self.validate_template_references()
        self.validate_mirrors_config()
        
        success = self.print_report()
        
        return 0 if success else 1

if __name__ == "__main__":
    validator = Validator()
    exit_code = validator.run()
    sys.exit(exit_code)
