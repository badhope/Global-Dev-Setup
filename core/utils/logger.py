"""
Global-Dev-Setup - Logger Module
Provides logging functionality with customizable output
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from enum import Enum


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class Logger:
    """Logger with customizable handlers and formatters"""
    
    def __init__(self, name: str = "GlobalDevSetup", log_dir: Optional[Path] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.log_dir = log_dir
        
        self._setup_console_handler()
        if log_dir:
            self._setup_file_handler()
    
    def _setup_console_handler(self):
        """Setup console output handler"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
    
    def _setup_file_handler(self):
        """Setup file output handler"""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = self.log_dir / f"global-dev-setup-{datetime.now().strftime('%Y%m%d')}.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, extra=kwargs)
    
    def exception(self, message: str, exc_info=True, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, exc_info=exc_info, extra=kwargs)


# Global logger instance
_global_logger: Optional[Logger] = None


def get_logger(name: str = "GlobalDevSetup", log_dir: Optional[Path] = None) -> Logger:
    """Get or create global logger instance"""
    global _global_logger
    
    if _global_logger is None:
        _global_logger = Logger(name, log_dir)
    
    return _global_logger


def set_log_level(level: LogLevel):
    """Set global log level"""
    global _global_logger
    
    if _global_logger:
        for handler in _global_logger.logger.handlers:
            if handler.stream == sys.stdout:  # Console handler
                handler.setLevel(level.value)
            else:  # File handler
                handler.setLevel(logging.DEBUG)


def cleanup_old_logs(log_dir: Path, days: int = 7):
    """Remove log files older than specified days"""
    import time
    
    if not log_dir.exists():
        return
    
    current_time = time.time()
    cutoff_time = current_time - (days * 86400)
    
    for log_file in log_dir.glob("*.log"):
        if log_file.stat().st_mtime < cutoff_time:
            log_file.unlink()
