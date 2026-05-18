# 🚀 Global-Dev-Setup

> **Universal Developer Environment Setup Toolkit**
> A comprehensive, modular system for managing development tools and environments.
> Built with Python - extensible, scalable, and cross-platform.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/badhope/Global-Dev-Setup)](https://github.com/badhope/Global-Dev-Setup/stargazers)

## ✨ Features

- 🏗️ **Modular Architecture** - Clean, extensible core system
- 📦 **100+ Development Tools** - Everything you need in one place
- ⚡ **Quick Installation** - One-command setup scripts
- 🔧 **Cross-Platform** - Windows, macOS, Linux support
- 📚 **Comprehensive Documentation** - Architecture guides and API docs
- 🔄 **Auto-Update** - Keep all tools up to date
- 🎯 **Category-Based** - Organized by functionality
- 🧩 **Plugin System** - Extend functionality easily
- 📊 **Dependency Management** - Automatic dependency resolution
- 💻 **CLI & Library** - Use as CLI tool or Python library

## 📂 Directory Structure

```
Global-Dev-Setup/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── setup.json
├── global-dev-setup.py          # CLI entry point
├── global-dev-setup             # CLI launcher
├── core/                        # Core modules
│   ├── __init__.py
│   ├── cli/                    # Command-line interface
│   │   ├── cli.py
│   │   └── __init__.py
│   ├── config/                  # Configuration management
│   │   ├── config.py
│   │   └── __init__.py
│   ├── engine/                  # Core engine
│   │   ├── engine.py
│   │   └── __init__.py
│   ├── models/                  # Data models
│   │   ├── models.py
│   │   └── __init__.py
│   └── utils/                   # Utilities
│       ├── exceptions.py
│       ├── logger.py
│       └── __init__.py
├── docs/
│   ├── architecture/
│   │   └── ARCHITECTURE.md     # System architecture
│   ├── getting-started.md
│   ├── installation-guide.md
│   └── faq.md
├── tools/                       # Tool definitions
│   ├── programming-languages/
│   ├── databases/
│   ├── devops/
│   ├── editors/
│   ├── productivity/
│   └── frameworks/
├── scripts/                     # Installation scripts
│   ├── install-all.sh
│   ├── update-all.sh
│   └── setup-basics.sh
├── examples/                    # Usage examples
│   ├── usage_examples.py
│   └── quick_start.py
├── tests/                       # Unit tests
│   └── test_core.py
└── config/                     # Configuration templates
    ├── vscode-extensions/
    ├── git-config/
    └── shell-config/
```

## 🏗️ Architecture Overview

The system is built with a modular, layered architecture:

```
┌─────────────────────────────────────────┐
│     User Interface (CLI)                │
├─────────────────────────────────────────┤
│     Core Engine                         │
│     ├─ Dependency Resolver              │
│     ├─ Tool Installer                   │
│     └─ Verification Module              │
├─────────────────────────────────────────┤
│     Installation Sources                 │
│     (apt, brew, pip, curl, git)        │
├─────────────────────────────────────────┤
│     Configuration & Data Models          │
└─────────────────────────────────────────┘
```

### Key Components

- **CLI Layer** - Command-line interface with colored output
- **Core Engine** - Orchestrates all operations
- **Dependency Resolver** - Automatic dependency resolution
- **Configuration Manager** - Persistent configuration storage
- **Data Models** - Type-safe data structures

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/badhope/Global-Dev-Setup.git
cd Global-Dev-Setup
```

### 2. Use as CLI Tool

```bash
# Install a tool
python3 global-dev-setup.py install python3 git docker

# List installed tools
python3 global-dev-setup.py list

# Update tools
python3 global-dev-setup.py update

# Check status
python3 global-dev-setup.py status

# Search for tools
python3 global-dev-setup.py search python
```

### 3. Use as Python Library

```python
from core import ToolEngine, Tool, ToolCategory

engine = ToolEngine()

tool = Tool(
    name="python3",
    category=ToolCategory.PROGRAMMING_LANGUAGE,
    description="Python programming language"
)

result = engine.install_tool(tool)

if result.success:
    print(f"Installed {tool.name}")
else:
    print(f"Failed: {result.error}")
```

## 🐍 Python API Examples

### Basic Installation

```python
from core import Tool, ToolCategory, ToolEngine

engine = ToolEngine()

tool = Tool(
    name="git",
    category=ToolCategory.PRODUCTIVITY,
    description="Git version control"
)

result = engine.install_tool(tool)
print(f"Success: {result.success}")
```

### Batch Installation

```python
tools = [
    Tool(name="python3", category=ToolCategory.PROGRAMMING_LANGUAGE, description="Python"),
    Tool(name="git", category=ToolCategory.PRODUCTIVITY, description="Git"),
    Tool(name="docker", category=ToolCategory.DEVOPS, description="Docker"),
]

results = engine.install_batch(tools, parallel=True, max_workers=3)
```

### With Dependencies

```python
from core.models.models import Dependency

tool = Tool(
    name="mylib",
    category=ToolCategory.UTILITY,
    description="My library",
    dependencies=[
        Dependency(name="python3", version="3.8", optional=False),
        Dependency(name="git", optional=True)
    ]
)

result = engine.install_tool(tool)
```

### Configuration Management

```python
from core import ConfigManager

config = ConfigManager()

config.update_config(
    parallel_installs=5,
    auto_update=True
)

print(config.config.install_dir)
```

### Error Handling

```python
from core import InstallationError, ToolNotFoundError

try:
    result = engine.install_tool(tool)
    
    if not result.success:
        print(f"Installation failed: {result.error}")
        
except InstallationError as e:
    print(f"Installation error: {e.message}")
```

## 📦 Available Categories

### 🐍 Programming Languages
- **Python** - Python 3.x with pip, virtualenv, Poetry
- **JavaScript/Node.js** - Node.js, npm, yarn, pnpm
- **Rust** - Rust toolchain with Cargo
- **Go** - Go programming language
- **Java** - JDK 11/17/21
- **C/C++** - GCC, Clang, CMake

### 🗄️ Databases
- **PostgreSQL**, **MySQL**, **MongoDB**, **Redis**, **SQLite**

### 🐳 DevOps & Containers
- **Docker**, **Kubernetes**, **Terraform**, **Ansible**

### 💻 Code Editors & IDEs
- **VS Code**, **JetBrains**, **Vim/Neovim**, **Emacs**

### ⚡ Productivity Tools
- **Git**, **tmux**, **zsh/bash**, **fzf/ripgrep**

## 📖 Documentation

- [Architecture Guide](docs/architecture/ARCHITECTURE.md) - System architecture
- [Getting Started](docs/getting-started.md) - Begin your journey
- [Installation Guide](docs/installation-guide.md) - Detailed setup
- [FAQ](docs/faq.md) - Frequently asked questions
- [Contributing Guide](CONTRIBUTING.md) - How to contribute

## 🛠️ Usage Examples

See `examples/` directory for complete examples:

- `usage_examples.py` - Comprehensive API examples
- `quick_start.py` - Quick start examples

Run examples:
```bash
python3 examples/usage_examples.py
python3 examples/quick_start.py
```

## 🧪 Testing

Run unit tests:
```bash
python3 -m pytest tests/
```

Or directly:
```bash
python3 tests/test_core.py
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md).

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Submit a pull request

## 📋 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows 10/11
- **Disk Space**: 5GB minimum
- **Internet**: Required for downloading tools
- **Permissions**: Root/sudo for system-wide installation

## 🔧 Configuration

Configuration files are stored in:
- Linux/macOS: `~/.config/global-dev-setup/`
- Windows: `%APPDATA%/global-dev-setup/`

### Configuration Options

```json
{
  "install_dir": "~/.local/share/global-dev-setup",
  "cache_dir": "~/.cache/global-dev-setup",
  "parallel_installs": 3,
  "auto_update": false,
  "check_updates": true,
  "timeout": 300
}
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- All open-source tool maintainers
- Contributors to this repository
- Developer community

## 📞 Support

- Create an Issue for bugs
- Start a Discussion for questions
- Star the repo if it helps you!

---

**⭐ If this repository helps you, please give it a star!**
