"""
Global-Dev-Setup - Configuration Manager
Handles loading, saving, and managing configuration
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

from core.utils.exceptions import ConfigurationError
from core.utils.logger import get_logger


@dataclass
class AppConfig:
    """Application configuration"""
    install_dir: str = "~/.local/share/global-dev-setup"
    cache_dir: str = "~/.cache/global-dev-setup"
    config_dir: str = "~/.config/global-dev-setup"
    log_level: str = "INFO"
    auto_update: bool = False
    check_updates: bool = True
    parallel_installs: int = 3
    timeout: int = 300
    retry_attempts: int = 3
    retry_delay: int = 5
    mirror_url: Optional[str] = None
    proxy: Optional[str] = None
    custom_paths: List[str] = field(default_factory=list)
    default_shell: str = "bash"
    enable_telemetry: bool = False
    theme: str = "default"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "install_dir": self.install_dir,
            "cache_dir": self.cache_dir,
            "config_dir": self.config_dir,
            "log_level": self.log_level,
            "auto_update": self.auto_update,
            "check_updates": self.check_updates,
            "parallel_installs": self.parallel_installs,
            "timeout": self.timeout,
            "retry_attempts": self.retry_attempts,
            "retry_delay": self.retry_delay,
            "mirror_url": self.mirror_url,
            "proxy": self.proxy,
            "custom_paths": self.custom_paths,
            "default_shell": self.default_shell,
            "enable_telemetry": self.enable_telemetry,
            "theme": self.theme
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppConfig':
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


class ConfigManager:
    """Configuration manager for Global-Dev-Setup"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        if config_dir:
            self.config_dir = Path(config_dir).expanduser()
        else:
            self.config_dir = Path("~/.config/global-dev-setup").expanduser()
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / "config.json"
        self.profiles_file = self.config_dir / "profiles.json"
        self.installed_file = self.config_dir / "installed.json"
        
        self.logger = get_logger()
        self._config: Optional[AppConfig] = None
    
    @property
    def config(self) -> AppConfig:
        """Get current configuration"""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def load_config(self) -> AppConfig:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                return AppConfig.from_dict(data)
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}")
                return AppConfig()
        return AppConfig()
    
    def save_config(self, config: Optional[AppConfig] = None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config.to_dict(), f, indent=2)
            self.logger.info("Configuration saved successfully")
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")
    
    def update_config(self, **kwargs):
        """Update specific configuration values"""
        config = self.config
        
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
            else:
                raise ConfigurationError(f"Unknown configuration option: {key}")
        
        self.save_config(config)
    
    def load_profiles(self) -> Dict[str, Any]:
        """Load installation profiles"""
        if self.profiles_file.exists():
            try:
                with open(self.profiles_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load profiles: {e}")
        return {}
    
    def save_profiles(self, profiles: Dict[str, Any]):
        """Save installation profiles"""
        try:
            with open(self.profiles_file, 'w') as f:
                json.dump(profiles, f, indent=2)
        except Exception as e:
            raise ConfigurationError(f"Failed to save profiles: {e}")
    
    def load_installed_tools(self) -> Dict[str, Any]:
        """Load installed tools database"""
        if self.installed_file.exists():
            try:
                with open(self.installed_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load installed tools: {e}")
        return {"tools": []}
    
    def save_installed_tools(self, data: Dict[str, Any]):
        """Save installed tools database"""
        try:
            with open(self.installed_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise ConfigurationError(f"Failed to save installed tools: {e}")
    
    def reset_config(self):
        """Reset configuration to defaults"""
        self._config = AppConfig()
        self.save_config()
        self.logger.info("Configuration reset to defaults")
    
    def export_config(self, path: Path):
        """Export configuration to file"""
        with open(path, 'w') as f:
            json.dump(self.config.to_dict(), f, indent=2)
    
    def import_config(self, path: Path):
        """Import configuration from file"""
        with open(path, 'r') as f:
            data = json.load(f)
        self._config = AppConfig.from_dict(data)
        self.save_config()
        self.logger.info(f"Configuration imported from {path}")


class ToolConfigLoader:
    """Loads tool-specific configuration from YAML files"""
    
    def __init__(self, tools_dir: Path):
        self.tools_dir = tools_dir
        self.logger = get_logger()
        self._cache: Dict[str, Any] = {}
    
    def load_tool_config(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Load configuration for a specific tool"""
        if tool_name in self._cache:
            return self._cache[tool_name]
        
        tool_dir = self.tools_dir / tool_name
        config_file = tool_dir / "tool.yaml"
        
        if not config_file.exists():
            return None
        
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            self._cache[tool_name] = config
            return config
        except Exception as e:
            self.logger.error(f"Failed to load tool config for {tool_name}: {e}")
            return None
    
    def load_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load all tool configurations"""
        configs = {}
        
        for tool_dir in self.tools_dir.iterdir():
            if tool_dir.is_dir():
                config = self.load_tool_config(tool_dir.name)
                if config:
                    configs[tool_dir.name] = config
        
        return configs
    
    def clear_cache(self):
        """Clear configuration cache"""
        self._cache.clear()
