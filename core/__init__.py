"""
Global-Dev-Setup - Core Package
Universal Developer Environment Toolkit
"""

__version__ = "1.0.0"
__author__ = "badhope"
__license__ = "MIT"

from core.models.models import (
    Tool, ToolStatus, ToolCategory, Dependency,
    InstallationSource, SystemInfo, InstallationProfile,
    OSType
)
from core.config.config import ConfigManager, AppConfig
from core.engine.engine import ToolEngine, InstallationResult, DependencyResolver
from core.cli.cli import CLI
from core.utils.logger import get_logger, Logger, LogLevel
from core.utils.exceptions import (
    GlobalDevSetupException,
    InstallationError,
    DependencyError,
    ConfigurationError,
    ToolNotFoundError,
    UnsupportedOSError,
    NetworkError,
    PermissionError,
    ValidationError,
    PluginError,
    UpdateError,
    UninstallError,
    IntegrityError
)

__all__ = [
    "__version__",
    "Tool",
    "ToolStatus",
    "ToolCategory",
    "Dependency",
    "InstallationSource",
    "SystemInfo",
    "InstallationProfile",
    "OSType",
    "ConfigManager",
    "AppConfig",
    "ToolEngine",
    "InstallationResult",
    "DependencyResolver",
    "CLI",
    "get_logger",
    "Logger",
    "LogLevel",
    "GlobalDevSetupException",
    "InstallationError",
    "DependencyError",
    "ConfigurationError",
    "ToolNotFoundError",
    "UnsupportedOSError",
    "NetworkError",
    "PermissionError",
    "ValidationError",
    "PluginError",
    "UpdateError",
    "UninstallError",
    "IntegrityError",
]
