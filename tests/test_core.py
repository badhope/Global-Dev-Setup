#!/usr/bin/env python3
"""
Unit Tests for Global-Dev-Setup Core Components
"""

import unittest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.models.models import (
    Tool, ToolStatus, ToolCategory, Dependency,
    InstallationSource, OSType, SystemInfo
)
from core.config.config import ConfigManager, AppConfig
from core.engine.engine import ToolEngine, DependencyResolver, InstallationResult


class TestToolModel(unittest.TestCase):
    """Test Tool model"""
    
    def test_tool_creation(self):
        """Test creating a Tool instance"""
        tool = Tool(
            name="test-tool",
            category=ToolCategory.UTILITY,
            description="A test tool"
        )
        
        self.assertEqual(tool.name, "test-tool")
        self.assertEqual(tool.category, ToolCategory.UTILITY)
        self.assertEqual(tool.status, ToolStatus.NOT_INSTALLED)
    
    def test_tool_is_installed(self):
        """Test is_installed method"""
        tool = Tool(name="test", category=ToolCategory.UTILITY, description="test")
        
        self.assertFalse(tool.is_installed())
        
        tool.status = ToolStatus.INSTALLED
        self.assertTrue(tool.is_installed())
    
    def test_tool_to_dict(self):
        """Test tool serialization"""
        tool = Tool(
            name="test",
            category=ToolCategory.PROGRAMMING_LANGUAGE,
            description="Test tool"
        )
        
        data = tool.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], "test")
        self.assertEqual(data['category'], "programming_language")
    
    def test_tool_from_dict(self):
        """Test tool deserialization"""
        data = {
            "name": "test",
            "category": "database",
            "description": "Test database"
        }
        
        tool = Tool.from_dict(data)
        
        self.assertEqual(tool.name, "test")
        self.assertEqual(tool.category, ToolCategory.DATABASE)


class TestDependency(unittest.TestCase):
    """Test Dependency model"""
    
    def test_dependency_creation(self):
        """Test creating a Dependency"""
        dep = Dependency(
            name="python",
            version="3.8",
            optional=False
        )
        
        self.assertEqual(dep.name, "python")
        self.assertEqual(dep.version, "3.8")
        self.assertFalse(dep.optional)
    
    def test_dependency_to_dict(self):
        """Test dependency serialization"""
        dep = Dependency(name="git", version="2.30")
        data = dep.to_dict()
        
        self.assertEqual(data['name'], "git")
        self.assertEqual(data['version'], "2.30")


class TestInstallationSource(unittest.TestCase):
    """Test InstallationSource model"""
    
    def test_source_creation(self):
        """Test creating an InstallationSource"""
        source = InstallationSource(
            type="apt",
            package_name="python3"
        )
        
        self.assertEqual(source.type, "apt")
        self.assertEqual(source.package_name, "python3")


class TestSystemInfo(unittest.TestCase):
    """Test SystemInfo"""
    
    def test_system_info_detection(self):
        """Test system info detection"""
        info = SystemInfo.detect()
        
        self.assertIsNotNone(info.os)
        self.assertIsNotNone(info.architecture)
        self.assertIsNotNone(info.python_version)
        self.assertIsNotNone(info.home_dir)
    
    def test_system_info_to_dict(self):
        """Test system info serialization"""
        info = SystemInfo.detect()
        data = info.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertIn('os', data)
        self.assertIn('architecture', data)


class TestConfigManager(unittest.TestCase):
    """Test ConfigManager"""
    
    def setUp(self):
        """Setup test configuration"""
        self.test_dir = Path("/tmp/test-global-dev-setup")
        self.test_dir.mkdir(exist_ok=True)
        self.config = ConfigManager(self.test_dir)
    
    def test_default_config(self):
        """Test default configuration"""
        self.assertIsNotNone(self.config.config)
        self.assertEqual(self.config.config.parallel_installs, 3)
    
    def test_update_config(self):
        """Test updating configuration"""
        self.config.update_config(parallel_installs=5)
        
        self.assertEqual(self.config.config.parallel_installs, 5)
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration"""
        self.config.save_config()
        
        new_config = ConfigManager(self.test_dir)
        self.assertEqual(
            new_config.config.parallel_installs,
            self.config.config.parallel_installs
        )


class TestToolEngine(unittest.TestCase):
    """Test ToolEngine"""
    
    def setUp(self):
        """Setup test engine"""
        self.test_dir = Path("/tmp/test-global-dev-setup")
        self.test_dir.mkdir(exist_ok=True)
        self.config = ConfigManager(self.test_dir)
        self.engine = ToolEngine(self.config)
    
    def test_engine_creation(self):
        """Test engine initialization"""
        self.assertIsNotNone(self.engine)
        self.assertIsNotNone(self.engine.config)
        self.assertIsNotNone(self.system_info)
    
    def test_check_tool_installed(self):
        """Test checking if tool is installed"""
        result = self.engine.check_tool_installed("nonexistent")
        self.assertFalse(result)


class TestDependencyResolver(unittest.TestCase):
    """Test DependencyResolver"""
    
    def setUp(self):
        """Setup test resolver"""
        self.test_dir = Path("/tmp/test-global-dev-setup")
        self.config = ConfigManager(self.test_dir)
        self.engine = ToolEngine(self.config)
        self.resolver = DependencyResolver(self.config, Mock())
    
    def test_resolver_creation(self):
        """Test resolver initialization"""
        self.assertIsNotNone(self.resolver)
    
    def test_resolve_dependencies(self):
        """Test dependency resolution"""
        tool = Tool(
            name="test",
            category=ToolCategory.UTILITY,
            description="test",
            dependencies=[
                Dependency(name="python", optional=False),
                Dependency(name="git", optional=True)
            ]
        )
        
        deps = self.resolver.resolve(tool)
        
        self.assertEqual(len(deps), 1)
        self.assertEqual(deps[0].name, "python")


class TestInstallationResult(unittest.TestCase):
    """Test InstallationResult"""
    
    def test_result_creation(self):
        """Test creating an InstallationResult"""
        result = InstallationResult(
            success=True,
            tool_name="test",
            message="Installed successfully",
            duration=1.5
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.tool_name, "test")
        self.assertEqual(result.duration, 1.5)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
