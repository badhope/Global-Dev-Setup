"""
Global-Dev-Setup - Custom Exceptions
Defines custom exceptions for error handling
"""


class GlobalDevSetupException(Exception):
    """Base exception for Global-Dev-Setup"""
    
    def __init__(self, message: str, details: str = ""):
        super().__init__(message)
        self.message = message
        self.details = details
    
    def __str__(self):
        if self.details:
            return f"{self.message}\nDetails: {self.details}"
        return self.message


class InstallationError(GlobalDevSetupException):
    """Raised when tool installation fails"""
    pass


class DependencyError(GlobalDevSetupException):
    """Raised when dependency resolution fails"""
    pass


class ConfigurationError(GlobalDevSetupException):
    """Raised when configuration is invalid or missing"""
    pass


class ToolNotFoundError(GlobalDevSetupException):
    """Raised when a requested tool is not found"""
    pass


class UnsupportedOSError(GlobalDevSetupException):
    """Raised when tool is not supported on current OS"""
    pass


class NetworkError(GlobalDevSetupException):
    """Raised when network operation fails"""
    pass


class PermissionError(GlobalDevSetupException):
    """Raised when insufficient permissions"""
    pass


class ValidationError(GlobalDevSetupException):
    """Raised when validation fails"""
    pass


class PluginError(GlobalDevSetupException):
    """Raised when plugin operation fails"""
    pass


class UpdateError(GlobalDevSetupException):
    """Raised when update operation fails"""
    pass


class UninstallError(GlobalDevSetupException):
    """Raised when uninstall operation fails"""
    pass


class IntegrityError(GlobalDevSetupException):
    """Raised when file integrity check fails"""
    pass
