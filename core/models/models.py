"""
Global-Dev-Setup - Data Models
Defines core data structures for the tool management system
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class ToolStatus(Enum):
    """Tool installation status"""
    NOT_INSTALLED = "not_installed"
    INSTALLING = "installing"
    INSTALLED = "installed"
    UPDATE_AVAILABLE = "update_available"
    FAILED = "failed"
    UNKNOWN = "unknown"


class ToolCategory(Enum):
    """Tool categories"""
    PROGRAMMING_LANGUAGE = "programming_language"
    DATABASE = "database"
    DEVOPS = "devops"
    EDITOR = "editor"
    PRODUCTIVITY = "productivity"
    FRAMEWORK = "framework"
    AI_ML = "ai_ml"
    DESIGN = "design"
    UTILITY = "utility"


class OSType(Enum):
    """Supported operating systems"""
    LINUX = "linux"
    MACOS = "macos"
    WINDOWS = "windows"
    ALL = "all"


@dataclass
class Dependency:
    """Tool dependency model"""
    name: str
    version: Optional[str] = None
    optional: bool = False
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "optional": self.optional,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Dependency':
        return cls(
            name=data.get("name", ""),
            version=data.get("version"),
            optional=data.get("optional", False),
            description=data.get("description", "")
        )


@dataclass
class InstallationSource:
    """Tool installation source"""
    type: str  # apt, brew, pip, curl, git, manual
    url: Optional[str] = None
    command: Optional[str] = None
    package_name: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "url": self.url,
            "command": self.command,
            "package_name": self.package_name
        }


@dataclass
class Tool:
    """Tool definition model"""
    name: str
    category: ToolCategory
    description: str
    version: Optional[str] = None
    latest_version: Optional[str] = None
    status: ToolStatus = ToolStatus.NOT_INSTALLED
    installed_version: Optional[str] = None
    installation_sources: List[InstallationSource] = field(default_factory=list)
    dependencies: List[Dependency] = field(default_factory=list)
    supported_os: List[OSType] = field(default_factory=list)
    homepage: Optional[str] = None
    documentation: Optional[str] = None
    license: Optional[str] = None
    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    config_files: List[str] = field(default_factory=list)
    environment_vars: Dict[str, str] = field(default_factory=dict)
    installed_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    
    def is_installed(self) -> bool:
        return self.status == ToolStatus.INSTALLED
    
    def needs_update(self) -> bool:
        return (self.status == ToolStatus.UPDATE_AVAILABLE or
                (self.version and self.latest_version and 
                 self.version != self.latest_version))
    
    def supports_current_os(self) -> bool:
        import platform
        current_os = platform.system().lower()
        
        if OSType.ALL in self.supported_os:
            return True
        
        os_map = {
            "linux": OSType.LINUX,
            "darwin": OSType.MACOS,
            "windows": OSType.WINDOWS
        }
        
        current = os_map.get(current_os)
        return current in self.supported_os if current else False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "version": self.version,
            "latest_version": self.latest_version,
            "status": self.status.value,
            "installed_version": self.installed_version,
            "installation_sources": [s.to_dict() for s in self.installation_sources],
            "dependencies": [d.to_dict() for d in self.dependencies],
            "supported_os": [os.value for os in self.supported_os],
            "homepage": self.homepage,
            "documentation": self.documentation,
            "license": self.license,
            "author": self.author,
            "tags": self.tags,
            "requirements": self.requirements,
            "config_files": self.config_files,
            "environment_vars": self.environment_vars,
            "installed_at": self.installed_at.isoformat() if self.installed_at else None,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tool':
        sources = [InstallationSource(**s) for s in data.get("installation_sources", [])]
        deps = [Dependency.from_dict(d) for d in data.get("dependencies", [])]
        supported = [OSType(os) for os in data.get("supported_os", [])]
        
        return cls(
            name=data.get("name", ""),
            category=ToolCategory(data.get("category", "utility")),
            description=data.get("description", ""),
            version=data.get("version"),
            latest_version=data.get("latest_version"),
            status=ToolStatus(data.get("status", "not_installed")),
            installed_version=data.get("installed_version"),
            installation_sources=sources,
            dependencies=deps,
            supported_os=supported,
            homepage=data.get("homepage"),
            documentation=data.get("documentation"),
            license=data.get("license"),
            author=data.get("author"),
            tags=data.get("tags", []),
            requirements=data.get("requirements", []),
            config_files=data.get("config_files", []),
            environment_vars=data.get("environment_vars", {})
        )


@dataclass
class ToolCategory:
    """Category model for organizing tools"""
    id: str
    name: str
    description: str
    icon: str = "📦"
    tools: List[Tool] = field(default_factory=list)
    parent: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "parent": self.parent,
            "tool_count": len(self.tools)
        }


@dataclass
class InstallationProfile:
    """Installation profile for different use cases"""
    name: str
    description: str
    tools: List[str]
    settings: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "tools": self.tools,
            "settings": self.settings
        }


@dataclass
class SystemInfo:
    """System information"""
    os: str
    os_version: str
    architecture: str
    python_version: str
    home_dir: str
    cache_dir: str
    config_dir: str
    
    @classmethod
    def detect(cls) -> 'SystemInfo':
        import platform
        import os
        
        return cls(
            os=platform.system().lower(),
            os_version=platform.release(),
            architecture=platform.machine(),
            python_version=platform.python_version(),
            home_dir=os.path.expanduser("~"),
            cache_dir=os.path.join(os.path.expanduser("~"), ".cache", "global-dev-setup"),
            config_dir=os.path.join(os.path.expanduser("~"), ".config", "global-dev-setup")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "os": self.os,
            "os_version": self.os_version,
            "architecture": self.architecture,
            "python_version": self.python_version,
            "home_dir": self.home_dir,
            "cache_dir": self.cache_dir,
            "config_dir": self.config_dir
        }
