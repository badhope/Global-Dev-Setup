#!/usr/bin/env python3
"""
Global-Dev-Setup - Quick Start Examples
Simple examples to get started quickly
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core import ToolEngine, Tool, ToolCategory, OSType


def quick_install_python():
    """Quick install Python"""
    engine = ToolEngine()
    
    python = Tool(
        name="python3",
        category=ToolCategory.PROGRAMMING_LANGUAGE,
        description="Python 3 programming language"
    )
    
    result = engine.install_tool(python)
    print(f"Python installation: {'Success' if result.success else 'Failed'}")


def quick_install_git():
    """Quick install Git"""
    engine = ToolEngine()
    
    git = Tool(
        name="git",
        category=ToolCategory.PRODUCTIVITY,
        description="Git version control system"
    )
    
    result = engine.install_tool(git)
    print(f"Git installation: {'Success' if result.success else 'Failed'}")


def quick_install_docker():
    """Quick install Docker"""
    engine = ToolEngine()
    
    docker = Tool(
        name="docker",
        category=ToolCategory.DEVOPS,
        description="Docker container platform"
    )
    
    result = engine.install_tool(docker)
    print(f"Docker installation: {'Success' if result.success else 'Failed'}")


def install_development_stack():
    """Install complete development stack"""
    engine = ToolEngine()
    
    tools = [
        Tool(name="git", category=ToolCategory.PRODUCTIVITY, description="Git"),
        Tool(name="python3", category=ToolCategory.PROGRAMMING_LANGUAGE, description="Python"),
        Tool(name="nodejs", category=ToolCategory.PROGRAMMING_LANGUAGE, description="Node.js"),
        Tool(name="docker", category=ToolCategory.DEVOPS, description="Docker"),
    ]
    
    print("Installing development stack...")
    results = engine.install_batch(tools, parallel=True)
    
    success = sum(1 for r in results if r.success)
    print(f"Installed {success}/{len(tools)} tools successfully")


if __name__ == '__main__':
    print("Quick Start Examples")
    print("-" * 40)
    
    quick_install_git()
    quick_install_python()
    install_development_stack()
