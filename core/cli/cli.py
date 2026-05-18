"""
Global-Dev-Setup - CLI Interface
Command-line interface for tool management
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional

from core.config.config import ConfigManager
from core.engine.engine import ToolEngine
from core.models.models import Tool, ToolCategory, ToolStatus, SystemInfo
from core.utils.logger import get_logger


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class CLI:
    """Command-line interface for Global-Dev-Setup"""
    
    def __init__(self):
        self.logger = get_logger()
        self.config = ConfigManager()
        self.engine = ToolEngine(self.config)
        self.system_info = SystemInfo.detect()
    
    def print_banner(self):
        """Print application banner"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   🚀 Global-Dev-Setup                               ║
║   Universal Developer Environment Toolkit           ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.WHITE}System: {self.system_info.os.title()} {self.system_info.architecture}
Python: {self.system_info.python_version}
{Colors.RESET}
"""
        print(banner)
    
    def print_success(self, message: str):
        """Print success message"""
        print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"{Colors.RED}✗ {message}{Colors.RESET}")
    
    def print_warning(self, message: str):
        """Print warning message"""
        print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")
    
    def print_info(self, message: str):
        """Print info message"""
        print(f"{Colors.BLUE}ℹ {message}{Colors.RESET}")
    
    def cmd_install(self, args):
        """Handle install command"""
        if not args.tools:
            self.print_error("No tools specified for installation")
            return 1
        
        self.print_info(f"Installing {len(args.tools)} tool(s)...")
        
        tools = []
        for tool_name in args.tools:
            tool = Tool(
                name=tool_name,
                category=ToolCategory.UTILITY,
                description=f"Tool: {tool_name}"
            )
            tools.append(tool)
        
        results = self.engine.install_batch(tools, parallel=args.parallel)
        
        success_count = sum(1 for r in results if r.success)
        failed_count = len(results) - success_count
        
        print()
        for result in results:
            if result.success:
                self.print_success(f"{result.tool_name}: {result.message}")
            else:
                self.print_error(f"{result.tool_name}: {result.error}")
        
        print()
        print(f"Installation complete: {success_count} succeeded, {failed_count} failed")
        
        return 0 if failed_count == 0 else 1
    
    def cmd_uninstall(self, args):
        """Handle uninstall command"""
        if not args.tools:
            self.print_error("No tools specified for uninstallation")
            return 1
        
        self.print_info(f"Uninstalling {len(args.tools)} tool(s)...")
        
        for tool_name in args.tools:
            result = self.engine.uninstall_tool(tool_name)
            
            if result.success:
                self.print_success(f"{result.tool_name}: Uninstalled")
            else:
                self.print_error(f"{result.tool_name}: {result.error}")
        
        return 0
    
    def cmd_update(self, args):
        """Handle update command"""
        if args.tools:
            tools = args.tools
        else:
            installed = self.engine.installed_tools_db.get("tools", [])
            tools = [t.get("name") for t in installed]
        
        self.print_info(f"Updating {len(tools)} tool(s)...")
        
        for tool_name in tools:
            result = self.engine.update_tool(tool_name)
            
            if result.success:
                self.print_success(f"{result.tool_name}: Updated")
            else:
                self.print_error(f"{result.tool_name}: {result.error}")
        
        return 0
    
    def cmd_list(self, args):
        """Handle list command"""
        installed = self.engine.installed_tools_db.get("tools", [])
        
        if not installed:
            self.print_warning("No tools installed yet")
            return 0
        
        print(f"\n{Colors.BOLD}Installed Tools ({len(installed)}):{Colors.RESET}\n")
        
        for tool_data in installed:
            name = tool_data.get("name", "Unknown")
            version = tool_data.get("version", "N/A")
            category = tool_data.get("category", "utility")
            
            print(f"  {Colors.GREEN}•{Colors.RESET} {Colors.CYAN}{name}{Colors.RESET}")
            print(f"    Version: {version}")
            print(f"    Category: {category}")
            print()
        
        return 0
    
    def cmd_search(self, args):
        """Handle search command"""
        self.print_info(f"Searching for: {args.query}")
        
        installed = self.engine.installed_tools_db.get("tools", [])
        
        matching = [
            t for t in installed
            if args.query.lower() in t.get("name", "").lower()
        ]
        
        if matching:
            print(f"\n{Colors.BOLD}Found {len(matching)} matching tool(s):{Colors.RESET}\n")
            for tool_data in matching:
                print(f"  {Colors.GREEN}•{Colors.RESET} {Colors.CYAN}{tool_data.get('name')}{Colors.RESET}")
        else:
            self.print_warning("No matching tools found")
        
        return 0
    
    def cmd_info(self, args):
        """Handle info command"""
        tool_name = args.tool
        
        if not self.engine.check_tool_installed(tool_name):
            self.print_error(f"Tool '{tool_name}' is not installed")
            return 1
        
        installed = self.engine.installed_tools_db.get("tools", [])
        tool_data = None
        
        for t in installed:
            if t.get("name") == tool_name:
                tool_data = t
                break
        
        if not tool_data:
            return 1
        
        print(f"\n{Colors.BOLD}Tool Information:{Colors.RESET}\n")
        print(f"  {Colors.CYAN}Name:{Colors.RESET} {tool_data.get('name')}")
        print(f"  {Colors.CYAN}Version:{Colors.RESET} {tool_data.get('version', 'N/A')}")
        print(f"  {Colors.CYAN}Category:{Colors.RESET} {tool_data.get('category', 'N/A')}")
        print(f"  {Colors.CYAN}Installed:{Colors.RESET} {tool_data.get('installed_at', 'N/A')}")
        
        return 0
    
    def cmd_status(self, args):
        """Handle status command"""
        print(f"\n{Colors.BOLD}System Status:{Colors.RESET}\n")
        print(f"  {Colors.CYAN}OS:{Colors.RESET} {self.system_info.os.title()} {self.system_info.os_version}")
        print(f"  {Colors.CYAN}Architecture:{Colors.RESET} {self.system_info.architecture}")
        print(f"  {Colors.CYAN}Python:{Colors.RESET} {self.system_info.python_version}")
        print(f"  {Colors.CYAN}Config Dir:{Colors.RESET} {self.config.config_dir}")
        print()
        
        installed = self.engine.installed_tools_db.get("tools", [])
        print(f"  {Colors.CYAN}Installed Tools:{Colors.RESET} {len(installed)}")
        
        print()
        return 0
    
    def cmd_config(self, args):
        """Handle config command"""
        if args.show:
            print(f"\n{Colors.BOLD}Current Configuration:{Colors.RESET}\n")
            config_dict = self.config.config.to_dict()
            for key, value in config_dict.items():
                print(f"  {Colors.CYAN}{key}:{Colors.RESET} {value}")
            print()
        elif args.reset:
            self.config.reset_config()
            self.print_success("Configuration reset to defaults")
        else:
            self.print_error("No config action specified")
            return 1
        
        return 0
    
    def run(self, argv: Optional[List[str]] = None):
        """Run the CLI"""
        parser = self._create_parser()
        args = parser.parse_args(argv)
        
        if hasattr(args, 'func'):
            return args.func(args)
        else:
            self.print_banner()
            parser.print_help()
            return 0
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            description="Global-Dev-Setup - Universal Developer Environment Toolkit",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        install_parser = subparsers.add_parser('install', help='Install tools')
        install_parser.add_argument('tools', nargs='+', help='Tool names to install')
        install_parser.add_argument('--parallel', action='store_true', help='Install in parallel')
        install_parser.set_defaults(func=self.cmd_install)
        
        uninstall_parser = subparsers.add_parser('uninstall', help='Uninstall tools')
        uninstall_parser.add_argument('tools', nargs='+', help='Tool names to uninstall')
        uninstall_parser.set_defaults(func=self.cmd_uninstall)
        
        update_parser = subparsers.add_parser('update', help='Update tools')
        update_parser.add_argument('tools', nargs='*', help='Tool names to update (all if not specified)')
        update_parser.set_defaults(func=self.cmd_update)
        
        list_parser = subparsers.add_parser('list', help='List installed tools')
        list_parser.set_defaults(func=self.cmd_list)
        
        search_parser = subparsers.add_parser('search', help='Search for tools')
        search_parser.add_argument('query', help='Search query')
        search_parser.set_defaults(func=self.cmd_search)
        
        info_parser = subparsers.add_parser('info', help='Show tool information')
        info_parser.add_argument('tool', help='Tool name')
        info_parser.set_defaults(func=self.cmd_info)
        
        status_parser = subparsers.add_parser('status', help='Show system status')
        status_parser.set_defaults(func=self.cmd_status)
        
        config_parser = subparsers.add_parser('config', help='Manage configuration')
        config_parser.add_argument('--show', action='store_true', help='Show current configuration')
        config_parser.add_argument('--reset', action='store_true', help='Reset configuration to defaults')
        config_parser.set_defaults(func=self.cmd_config)
        
        return parser


def main():
    """Main entry point"""
    cli = CLI()
    return cli.run()


if __name__ == '__main__':
    sys.exit(main())
