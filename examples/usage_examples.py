#!/usr/bin/env python3
"""
Example Usage of Global-Dev-Setup
Demonstrates various ways to use the library
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from core import (
    Tool, ToolCategory, ToolStatus, OSType,
    ToolEngine, ConfigManager,
    get_logger, InstallationError
)
from core.models.models import InstallationSource, Dependency


def example_basic_install():
    """Basic tool installation example"""
    print("\n=== Example: Basic Tool Installation ===\n")
    
    engine = ToolEngine()
    
    tool = Tool(
        name="python",
        category=ToolCategory.PROGRAMMING_LANGUAGE,
        description="Python programming language",
        version="3.11",
        installation_sources=[
            InstallationSource(type="apt", package_name="python3")
        ],
        supported_os=[OSType.LINUX, OSType.MACOS, OSType.ALL]
    )
    
    result = engine.install_tool(tool)
    
    if result.success:
        print(f"✓ Successfully installed {result.tool_name}")
        print(f"  Duration: {result.duration:.2f}s")
    else:
        print(f"✗ Failed to install {result.tool_name}")
        print(f"  Error: {result.error}")


def example_with_dependencies():
    """Tool installation with dependencies"""
    print("\n=== Example: Installation with Dependencies ===\n")
    
    engine = ToolEngine()
    
    tool = Tool(
        name="mylib",
        category=ToolCategory.UTILITY,
        description="My custom library",
        dependencies=[
            Dependency(name="python", version="3.8", optional=False),
            Dependency(name="git", optional=True)
        ]
    )
    
    result = engine.install_tool(tool)
    print(f"Result: {result.message}")


def example_batch_install():
    """Batch installation example"""
    print("\n=== Example: Batch Installation ===\n")
    
    engine = ToolEngine()
    
    tools = [
        Tool(name="git", category=ToolCategory.PRODUCTIVITY, description="Git version control"),
        Tool(name="docker", category=ToolCategory.DEVOPS, description="Docker container platform"),
        Tool(name="vim", category=ToolCategory.EDITOR, description="Vim text editor"),
    ]
    
    for source in tools[0].installation_sources:
        source.type = "apt"
        source.package_name = "git"
    
    results = engine.install_batch(tools, parallel=True, max_workers=3)
    
    for result in results:
        status = "✓" if result.success else "✗"
        print(f"{status} {result.tool_name}: {result.message}")


def example_configuration():
    """Configuration management example"""
    print("\n=== Example: Configuration Management ===\n")
    
    config = ConfigManager()
    
    print(f"Install directory: {config.config.install_dir}")
    print(f"Parallel installs: {config.config.parallel_installs}")
    print(f"Auto update: {config.config.auto_update}")
    
    config.update_config(
        parallel_installs=5,
        auto_update=True
    )
    
    print("\nUpdated config:")
    print(f"Parallel installs: {config.config.parallel_installs}")
    print(f"Auto update: {config.config.auto_update}")


def example_list_tools():
    """List installed tools example"""
    print("\n=== Example: List Installed Tools ===\n")
    
    engine = ToolEngine()
    installed = engine.installed_tools_db.get("tools", [])
    
    if not installed:
        print("No tools installed yet")
        return
    
    print(f"Installed tools ({len(installed)}):\n")
    for tool in installed:
        print(f"  • {tool.get('name')} ({tool.get('version', 'N/A')})")


def example_uninstall():
    """Tool uninstallation example"""
    print("\n=== Example: Tool Uninstallation ===\n")
    
    engine = ToolEngine()
    
    result = engine.uninstall_tool("vim")
    
    if result.success:
        print(f"✓ Successfully uninstalled {result.tool_name}")
    else:
        print(f"✗ Failed to uninstall: {result.error}")


def example_custom_logger():
    """Custom logging example"""
    print("\n=== Example: Custom Logging ===\n")
    
    from pathlib import Path
    
    logger = get_logger("CustomLogger", Path("/tmp/logs"))
    
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    print("Check /tmp/logs/ for log files")


def example_error_handling():
    """Error handling example"""
    print("\n=== Example: Error Handling ===\n")
    
    from core.utils.exceptions import InstallationError, ToolNotFoundError
    
    engine = ToolEngine()
    
    try:
        result = engine.install_tool(
            Tool(
                name="nonexistent",
                category=ToolCategory.UTILITY,
                description="This tool doesn't exist"
            )
        )
        
        if not result.success:
            print(f"Handled error: {result.error}")
    
    except InstallationError as e:
        print(f"Installation error: {e.message}")
    except ToolNotFoundError as e:
        print(f"Tool not found: {e.message}")


def example_plugin_system():
    """Plugin system example"""
    print("\n=== Example: Plugin System ===\n")
    
    engine = ToolEngine()
    
    def my_install_hook(tool):
        print(f"Custom hook: Installed {tool.name}")
    
    def my_uninstall_hook(tool_name):
        print(f"Custom hook: Uninstalled {tool_name}")
    
    engine.install_hooks.append(my_install_hook)
    engine.uninstall_hooks.append(my_uninstall_hook)
    
    print("Hooks registered successfully")


def main():
    """Run all examples"""
    print("=" * 60)
    print("Global-Dev-Setup - Usage Examples")
    print("=" * 60)
    
    try:
        example_basic_install()
        example_with_dependencies()
        example_batch_install()
        example_configuration()
        example_list_tools()
        example_uninstall()
        example_custom_logger()
        example_error_handling()
        example_plugin_system()
        
        print("\n" + "=" * 60)
        print("All examples completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
