"""
Global-Dev-Setup - Core Engine
Main orchestration engine for tool management
"""

import subprocess
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from core.models.models import (
    Tool, ToolStatus, Dependency, InstallationSource,
    ToolCategory, OSType, SystemInfo
)
from core.config.config import ConfigManager
from core.utils.exceptions import (
    InstallationError, DependencyError, NetworkError,
    PermissionError, ToolNotFoundError, UnsupportedOSError
)
from core.utils.logger import get_logger


@dataclass
class InstallationResult:
    """Result of an installation operation"""
    success: bool
    tool_name: str
    message: str
    error: Optional[str] = None
    duration: float = 0.0


class DependencyResolver:
    """Resolves and installs tool dependencies"""
    
    def __init__(self, config: ConfigManager, logger):
        self.config = config
        self.logger = logger
        self.installed_tools = set()
    
    def resolve(self, tool: Tool) -> List[Dependency]:
        """Resolve all dependencies for a tool"""
        resolved = []
        
        for dep in tool.dependencies:
            if dep.name not in self.installed_tools:
                if not dep.optional:
                    resolved.append(dep)
                else:
                    self.logger.debug(f"Optional dependency: {dep.name}")
        
        return resolved
    
    def install_dependency(self, dep: Dependency, engine: 'ToolEngine') -> bool:
        """Install a single dependency"""
        try:
            self.logger.info(f"Installing dependency: {dep.name}")
            
            tool = Tool(
                name=dep.name,
                category=ToolCategory.UTILITY,
                description=dep.description or f"Dependency: {dep.name}"
            )
            
            if dep.version:
                tool.version = dep.version
            
            result = engine.install_tool(tool)
            return result.success
        except Exception as e:
            self.logger.error(f"Failed to install dependency {dep.name}: {e}")
            return False


class ToolEngine:
    """Core engine for tool installation and management"""
    
    def __init__(self, config: Optional[ConfigManager] = None):
        self.config = config or ConfigManager()
        self.logger = get_logger()
        self.dependency_resolver = DependencyResolver(self.config, self.logger)
        
        self.system_info = SystemInfo.detect()
        self.installed_tools_db = self._load_installed_tools()
        
        self.install_hooks: List[Callable] = []
        self.uninstall_hooks: List[Callable] = []
        self.update_hooks: List[Callable] = []
    
    def _load_installed_tools(self) -> Dict[str, Any]:
        """Load installed tools database"""
        return self.config.load_installed_tools()
    
    def _save_installed_tools(self):
        """Save installed tools database"""
        self.config.save_installed_tools(self.installed_tools_db)
    
    def check_tool_installed(self, tool_name: str) -> bool:
        """Check if a tool is already installed"""
        return tool_name in self.installed_tools_db.get("tools", [])
    
    def get_installed_version(self, tool_name: str) -> Optional[str]:
        """Get installed version of a tool"""
        tools = self.installed_tools_db.get("tools", [])
        for tool_data in tools:
            if tool_data.get("name") == tool_name:
                return tool_data.get("version")
        return None
    
    def install_tool(self, tool: Tool, skip_deps: bool = False) -> InstallationResult:
        """Install a single tool"""
        import time
        start_time = time.time()
        
        self.logger.info(f"Starting installation: {tool.name}")
        
        try:
            if not tool.supports_current_os():
                raise UnsupportedOSError(
                    f"Tool {tool.name} is not supported on {self.system_info.os}"
                )
            
            if self.check_tool_installed(tool.name):
                self.logger.info(f"Tool {tool.name} is already installed")
                return InstallationResult(
                    success=True,
                    tool_name=tool.name,
                    message="Already installed",
                    duration=time.time() - start_time
                )
            
            if not skip_deps:
                deps = self.dependency_resolver.resolve(tool)
                for dep in deps:
                    if not self.dependency_resolver.install_dependency(dep, self):
                        raise DependencyError(f"Failed to install dependency: {dep.name}")
            
            for source in tool.installation_sources:
                self._install_from_source(tool, source)
                break
            
            self._register_installed_tool(tool)
            
            for hook in self.install_hooks:
                hook(tool)
            
            duration = time.time() - start_time
            self.logger.info(f"Successfully installed {tool.name} in {duration:.2f}s")
            
            return InstallationResult(
                success=True,
                tool_name=tool.name,
                message="Installation successful",
                duration=duration
            )
            
        except Exception as e:
            duration = time.time() - start_time
            error_msg = str(e)
            self.logger.error(f"Failed to install {tool.name}: {error_msg}")
            
            return InstallationResult(
                success=False,
                tool_name=tool.name,
                message="Installation failed",
                error=error_msg,
                duration=duration
            )
    
    def _install_from_source(self, tool: Tool, source: InstallationSource):
        """Install tool from specified source"""
        self.logger.debug(f"Installing from source: {source.type}")
        
        if source.type == "apt":
            self._install_apt(tool, source)
        elif source.type == "brew":
            self._install_brew(tool, source)
        elif source.type == "pip":
            self._install_pip(tool, source)
        elif source.type == "curl":
            self._install_curl(tool, source)
        elif source.type == "git":
            self._install_git(tool, source)
        else:
            raise InstallationError(f"Unknown installation source type: {source.type}")
    
    def _install_apt(self, tool: Tool, source: InstallationSource):
        """Install tool using apt (Debian/Ubuntu)"""
        if self.system_info.os != "linux":
            raise UnsupportedOSError("apt is only available on Linux")
        
        package = source.package_name or tool.name
        
        try:
            subprocess.run(
                ["sudo", "apt-get", "update"],
                check=True,
                capture_output=True
            )
            subprocess.run(
                ["sudo", "apt-get", "install", "-y", package],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            raise InstallationError(f"apt-get failed: {e.stderr.decode()}")
    
    def _install_brew(self, tool: Tool, source: InstallationSource):
        """Install tool using Homebrew (macOS)"""
        if self.system_info.os != "darwin":
            raise UnsupportedOSError("brew is only available on macOS")
        
        package = source.package_name or tool.name
        
        try:
            subprocess.run(
                ["brew", "install", package],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            raise InstallationError(f"brew install failed: {e.stderr.decode()}")
    
    def _install_pip(self, tool: Tool, source: InstallationSource):
        """Install tool using pip"""
        package = source.package_name or tool.name
        
        try:
            subprocess.run(
                ["pip3", "install", package],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            raise InstallationError(f"pip install failed: {e.stderr.decode()}")
    
    def _install_curl(self, tool: Tool, source: InstallationSource):
        """Download and install tool using curl"""
        if not source.url:
            raise InstallationError("URL required for curl installation")
        
        try:
            install_dir = Path(self.config.config.install_dir).expanduser()
            install_dir.mkdir(parents=True, exist_ok=True)
            
            if source.command:
                subprocess.run(
                    source.command,
                    shell=True,
                    check=True,
                    capture_output=True
                )
            else:
                filename = Path(source.url).name
                output_path = install_dir / filename
                
                urllib.request.urlretrieve(source.url, output_path)
                
                if source.command:
                    subprocess.run(
                        source.command,
                        shell=True,
                        check=True,
                        capture_output=True
                    )
        except Exception as e:
            raise InstallationError(f"curl installation failed: {e}")
    
    def _install_git(self, tool: Tool, source: InstallationSource):
        """Clone and install tool from Git"""
        if not source.url:
            raise InstallationError("Git URL required")
        
        try:
            install_dir = Path(self.config.config.install_dir).expanduser()
            install_dir.mkdir(parents=True, exist_ok=True)
            
            subprocess.run(
                ["git", "clone", source.url, str(install_dir / tool.name)],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            raise InstallationError(f"git clone failed: {e.stderr.decode()}")
    
    def _register_installed_tool(self, tool: Tool):
        """Register installed tool in database"""
        tools = self.installed_tools_db.get("tools", [])
        
        tools.append({
            "name": tool.name,
            "version": tool.version,
            "installed_at": tool.installed_at.isoformat() if tool.installed_at else None,
            "category": tool.category.value,
            "config_files": tool.config_files
        })
        
        self.installed_tools_db["tools"] = tools
        self._save_installed_tools()
    
    def uninstall_tool(self, tool_name: str) -> InstallationResult:
        """Uninstall a tool"""
        import time
        start_time = time.time()
        
        self.logger.info(f"Starting uninstallation: {tool_name}")
        
        try:
            if not self.check_tool_installed(tool_name):
                raise ToolNotFoundError(f"Tool {tool_name} is not installed")
            
            tool_data = None
            tools = self.installed_tools_db.get("tools", [])
            for t in tools:
                if t.get("name") == tool_name:
                    tool_data = t
                    break
            
            if not tool_data:
                raise ToolNotFoundError(f"Tool {tool_name} not found in database")
            
            self.logger.info(f"Uninstalling {tool_name}")
            
            tools = [t for t in tools if t.get("name") != tool_name]
            self.installed_tools_db["tools"] = tools
            self._save_installed_tools()
            
            for hook in self.uninstall_hooks:
                hook(tool_name)
            
            duration = time.time() - start_time
            self.logger.info(f"Successfully uninstalled {tool_name}")
            
            return InstallationResult(
                success=True,
                tool_name=tool_name,
                message="Uninstallation successful",
                duration=duration
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"Failed to uninstall {tool_name}: {e}")
            
            return InstallationResult(
                success=False,
                tool_name=tool_name,
                message="Uninstallation failed",
                error=str(e),
                duration=duration
            )
    
    def update_tool(self, tool_name: str) -> InstallationResult:
        """Update a tool to latest version"""
        import time
        start_time = time.time()
        
        self.logger.info(f"Checking update for: {tool_name}")
        
        try:
            if not self.check_tool_installed(tool_name):
                raise ToolNotFoundError(f"Tool {tool_name} is not installed")
            
            tool = Tool(
                name=tool_name,
                category=ToolCategory.UTILITY,
                description=f"Tool: {tool_name}"
            )
            
            result = self.install_tool(tool)
            
            if result.success:
                for hook in self.update_hooks:
                    hook(tool_name)
            
            duration = time.time() - start_time
            return InstallationResult(
                success=result.success,
                tool_name=tool_name,
                message=result.message,
                duration=duration
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"Failed to update {tool_name}: {e}")
            
            return InstallationResult(
                success=False,
                tool_name=tool_name,
                message="Update failed",
                error=str(e),
                duration=duration
            )
    
    def install_batch(self, tools: List[Tool], 
                     parallel: bool = False,
                     max_workers: int = 3) -> List[InstallationResult]:
        """Install multiple tools"""
        if parallel:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(self.install_tool, tool): tool
                    for tool in tools
                }
                
                results = []
                for future in as_completed(futures):
                    results.append(future.result())
                
                return results
        else:
            return [self.install_tool(tool) for tool in tools]
    
    def verify_installation(self, tool_name: str) -> bool:
        """Verify if tool is properly installed"""
        if not self.check_tool_installed(tool_name):
            return False
        
        try:
            result = subprocess.run(
                ["which", tool_name],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False
