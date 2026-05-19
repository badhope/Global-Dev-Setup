# 🚀 Global-Dev-Setup

> **Developer Environment Registry & Configuration Repository**
> **定位**: 这是一个**环境配置数据仓库**，供外部智能体查询和使用。智能体可以根据用户需求，查询仓库中的工具定义和环境模板，自动选择并安装所需的开发环境。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 🎯 仓库定位

**这个仓库不是用来开发智能体的，而是作为智能体的辅助数据源。**

外部智能体可以：
1. **查询工具注册表** - 获取所有可用工具的详细信息
2. **搜索工具** - 根据关键词查找相关工具
3. **获取环境模板** - 获取预定义的开发环境配置
4. **获取安装命令** - 获取特定工具在特定操作系统上的安装命令
5. **获取推荐** - 根据开发需求获取推荐的工具列表

## ✨ 核心功能

- 📚 **工具注册表** - 40+ 开发工具的详细定义（安装方式、依赖、兼容性）
- 📋 **环境模板** - 16+ 预定义的开发环境配置
- 🔍 **搜索功能** - 支持按关键词、类别搜索工具
- 🤖 **Agent API** - 提供 REST API 和 CLI 接口供外部智能体调用
- 📤 **数据导出** - 支持将注册表导出为 JSON 格式
- 🌐 **Web 界面** - 可视化工具浏览和搜索界面
- 📦 **跨平台支持** - Linux、macOS、Windows

## 📂 目录结构

```
Global-Dev-Setup/
├── README.md                    # 项目说明文档
├── registry.py                  # 工具注册表核心模块
├── api.py                       # REST API 服务
├── agent_helper.py              # 智能体查询辅助工具
├── index.html                   # Web 可视化界面
├── tool_registry.json           # 注册表 JSON 导出（运行生成）
├── install.sh                   # 一键安装脚本 (Linux/macOS)
├── install.bat                  # 一键安装脚本 (Windows)
├── bootstrap.py                 # 智能引导安装器
├── tools/                       # 工具定义目录
│   ├── programming-languages/   # 编程语言工具
│   ├── databases/               # 数据库工具
│   ├── frameworks/              # 框架工具
│   ├── ai-ml/                   # AI/ML 工具
│   ├── big-data/                # 大数据工具
│   ├── devops/                  # DevOps 工具
│   ├── cloud/                   # 云服务工具
│   └── ...                      # 更多类别
├── environment-templates/       # 环境模板目录
│   ├── fullstack-developer.yaml
│   ├── ai-ml-developer.yaml
│   ├── devops-engineer.yaml
│   └── ...
└── core/                        # 核心模块（可选使用）
```

---

## 🔌 外部智能体使用方式

### 方式一：CLI 查询

```bash
# 列出所有工具
python registry.py --list-tools

# 列出所有模板
python registry.py --list-templates

# 搜索工具
python registry.py --search python

# 获取工具详情
python registry.py --tool docker

# 获取模板详情
python registry.py --template fullstack-developer

# 获取推荐工具
python registry.py --recommend web

# 获取安装命令
python registry.py --install-command docker

# 导出注册表到 JSON
python registry.py --export
```

### 方式二：Python API

```python
from registry import ToolRegistry

# 初始化注册表
registry = ToolRegistry()

# 查询所有工具
tools = registry.list_tools()

# 查询工具详情
tool = registry.get_tool("docker")

# 搜索工具
results = registry.search_tools("python")

# 获取环境模板
template = registry.get_template("ai-ml-developer")

# 获取模板包含的工具
template_tools = registry.get_template_tools("ai-ml-developer")

# 获取安装命令
cmd = registry.get_installation_command("docker", os_type="linux")

# 生成安装脚本
script = registry.generate_install_script(["git", "python3", "docker"])
```

### 方式三：REST API

```bash
# 启动 API 服务
python api.py

# 访问接口
curl http://localhost:8000/tools
curl http://localhost:8000/templates
curl http://localhost:8000/tools/docker
curl http://localhost:8000/templates/fullstack-developer/tools
curl -X POST http://localhost:8000/recommend -H "Content-Type: application/json" -d '{"category": "web"}'
```

### 方式四：JSON 导出

```bash
# 导出注册表
python registry.py --export

# 使用 JSON 文件
cat tool_registry.json
```

---

## 📚 工具分类

| 类别 | 工具 |
|------|------|
| **编程语言** | Python3, Node.js, Java, Go, Rust, C/C++, Ruby, PHP |
| **数据库** | PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, SQLite |
| **框架** | React, Vue, Angular, Next.js, Django, FastAPI |
| **AI/ML** | PyTorch, TensorFlow, Jupyter, Hugging Face |
| **大数据** | Spark, Hadoop, Kafka, Hive |
| **DevOps** | Docker, Kubernetes, Terraform, Helm, Ansible |
| **云服务** | AWS CLI, GCloud CLI, Azure CLI |
| **移动端** | Flutter, Android SDK, iOS |
| **游戏开发** | Unity, Unreal Engine |
| **IoT/嵌入式** | Arduino, Raspberry Pi, ESP32 |

---

## 📋 环境模板列表

| 模板 | 描述 |
|------|------|
| **fullstack-developer** | 全栈 Web 开发环境 |
| **frontend-developer** | 前端开发环境 |
| **backend-developer** | 后端开发环境 |
| **ai-ml-developer** | AI/ML 开发环境 |
| **ai-agent-developer** | AI Agent 开发环境 |
| **ml-engineer** | 机器学习工程环境 |
| **data-science** | 数据科学环境 |
| **big-data-engineer** | 大数据工程师环境 |
| **data-engineering** | 数据工程环境 |
| **devops-engineer** | DevOps 工程师环境 |
| **cloud-native-developer** | 云原生开发环境 |
| **mobile-developer** | 移动开发环境 |
| **game-developer** | 游戏开发环境 |
| **blockchain-developer** | 区块链开发环境 |
| **iot-developer** | IoT 开发环境 |
| **embedded-developer** | 嵌入式开发环境 |

---

## 🔄 工作流程示例

**智能体收到用户需求后的工作流程：**

1. **分析需求** → 用户需要设置一个 AI Agent 开发环境
2. **查询模板** → 调用 `registry.get_template("ai-agent-developer")`
3. **获取工具列表** → 调用 `registry.get_template_tools("ai-agent-developer")`
4. **获取安装命令** → 对每个工具调用 `registry.get_installation_command(tool_name, os)`
5. **执行安装** → 按优先级执行安装命令
6. **验证安装** → 调用工具的验证命令

---

## 🚀 快速开始

### 克隆仓库

```bash
git clone https://github.com/badhope/Global-Dev-Setup.git
cd Global-Dev-Setup
```

### 初始化注册表

```bash
# 导出注册表到 JSON（用于 Web 界面）
python registry.py --export

# 启动 API 服务（可选）
python api.py

# 启动 Web 界面（需要先导出 JSON）
# 使用浏览器打开 index.html
```

### 使用一键安装（可选）

```bash
# Linux/macOS
./install.sh

# Windows
install.bat
```

---

## 📝 贡献指南

欢迎提交 PR 来添加新工具或环境模板！

### 添加新工具

1. 在 `tools/[category]/[tool-name]/` 目录下创建 `tool.yaml` 文件
2. 参考现有工具的格式填写工具信息
3. 运行 `python registry.py --export` 更新注册表

### 添加新模板

1. 在 `environment-templates/` 目录下创建 `[template-name].yaml` 文件
2. 参考现有模板的格式填写配置
3. 更新 `core/engine/smart_recommender.py` 中的模板映射

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 📂 Directory Structure

```
Global-Dev-Setup/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── setup.json
├── install.sh                   # One-click installer (Linux/macOS)
├── install.bat                  # One-click installer (Windows)
├── bootstrap.py                 # Smart bootstrapper
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
│   │   ├── smart_recommender.py  # Intelligent recommendations
│   │   ├── smart_installer.py    # Smart installer
│   │   └── __init__.py
│   ├── models/                  # Data models
│   │   ├── models.py
│   │   └── __init__.py
│   ├── agent_interface.py      # External AI agent API
│   └── utils/                   # Utilities
│       ├── exceptions.py
│       ├── logger.py
│       └── __init__.py
├── docs/
│   ├── architecture/
│   │   └── ARCHITECTURE.md     # System architecture
│   ├── AGENT_API.md            # Agent integration guide
│   ├── COMPATIBILITY.md        # Tool compatibility matrix
│   ├── getting-started.md
│   ├── installation-guide.md
│   └── faq.md
├── tools/                       # Tool definitions (YAML)
│   ├── programming-languages/
│   │   ├── python3/
│   │   │   └── tool.yaml
│   │   └── nodejs/
│   │       └── tool.yaml
│   ├── databases/
│   │   └── postgresql/
│   │       └── tool.yaml
│   ├── devops/
│   │   └── docker/
│   │       └── tool.yaml
│   ├── editors/
│   │   └── vscode/
│   │       └── tool.yaml
│   └── productivity/
│       └── git/
│           └── tool.yaml
├── environment-templates/       # Pre-defined environments
│   ├── web-developer.yaml
│   ├── ai-ml-developer.yaml
│   ├── mobile-developer.yaml
│   └── devops-engineer.yaml
├── scripts/                     # Installation scripts
│   ├── install-all.sh
│   ├── update-all.sh
│   └── setup-basics.sh
├── examples/                    # Usage examples
│   ├── usage_examples.py
│   ├── quick_start.py
│   └── agent_integration.py     # Agent API examples
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

### Option 1: One-Click Install

**Linux/macOS:**
```bash
git clone https://github.com/badhope/Global-Dev-Setup.git
cd Global-Dev-Setup
chmod +x install.sh
./install.sh
```

**Windows:**
```bash
git clone https://github.com/badhope/Global-Dev-Setup.git
cd Global-Dev-Setup
install.bat
```

### Option 2: Smart Bootstrap

```bash
# Auto-select tools based on your needs
python3 bootstrap.py full-stack
```

### Option 3: Use as CLI Tool

```bash
# Install specific tools
python3 global-dev-setup.py install python3 git docker

# List installed tools
python3 global-dev-setup.py list

# Update tools
python3 global-dev-setup.py update

# Check status
python3 global-dev-setup.py status

# Search for tools
python3 global-dev-setup.py search python

# List templates
python3 global-dev-setup.py templates
```

### Option 4: Use as External Agent

See [AGENT_API.md](docs/AGENT_API.md) for integrating with external AI systems.

```python
from core.agent_interface import DevSetupAgent, AgentCommand

agent = DevSetupAgent()

# Get smart recommendations
result = agent.execute_command(
    AgentCommand.RECOMMEND_TOOLS,
    {"style": "ai-ml"}
)

# Install tools
result = agent.execute_command(
    AgentCommand.INSTALL_MULTIPLE,
    {"tools": ["git", "python3", "docker"]}
)
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
- [Agent API Guide](docs/AGENT_API.md) - Integrate with external AI
- [Compatibility Matrix](docs/COMPATIBILITY.md) - Tool compatibility info
- [Getting Started](docs/getting-started.md) - Begin your journey
- [Installation Guide](docs/installation-guide.md) - Detailed setup
- [FAQ](docs/faq.md) - Frequently asked questions
- [Contributing Guide](CONTRIBUTING.md) - How to contribute

## 🛠️ Usage Examples

See `examples/` directory for complete examples:

- `usage_examples.py` - Comprehensive API examples
- `quick_start.py` - Quick start examples
- `agent_integration.py` - External agent integration examples

Run examples:
```bash
python3 examples/usage_examples.py
python3 examples/quick_start.py
python3 examples/agent_integration.py
```

## 🎯 Environment Templates

Get started quickly with pre-configured environments. We support **23+ development profiles**:

### Web Development
| Template | Description | Key Tools |
|----------|-------------|-----------|
| **fullstack-developer** | Full-stack web developer | git, nodejs, python3, docker, postgresql, redis, react, nextjs |
| **frontend-developer** | Frontend specialist | git, nodejs, vscode, react, vue, typescript |
| **backend-developer** | Backend specialist | git, python3, docker, postgresql, redis, fastapi, django |

### AI & Machine Learning
| Template | Description | Key Tools |
|----------|-------------|-----------|
| **ai-ml-developer** | AI/ML developer | git, python3, docker, vscode, jupyter, pytorch, tensorflow |
| **ai-agent-developer** | AI Agent builder | git, python3, docker, redis, pytorch, huggingface |
| **ml-engineer** | ML engineer | git, python3, docker, pytorch, tensorflow, jupyter |
| **data-science** | Data scientist | git, python3, jupyter, pandas, numpy, scikit-learn |

### Big Data & Data Engineering
| Template | Description | Key Tools |
|----------|-------------|-----------|
| **big-data-engineer** | Big data engineer | git, java, python3, spark, hadoop, kafka |
| **data-engineering** | Data engineer | git, python3, java, spark, dbt, airflow |

### DevOps & Cloud
| Template | Description | Key Tools |
|----------|-------------|-----------|
| **devops-engineer** | DevOps engineer | git, docker, kubectl, terraform, ansible |
| **cloud-native-developer** | Cloud native dev | git, docker, kubectl, helm, terraform, go |
| **sysadmin** | System administrator | git, python3, docker, ansible, terraform |

### Mobile & Game Development
| Template | Description | Key Tools |
|----------|-------------|-----------|
| **mobile-developer** | Mobile app dev | git, nodejs, java, vscode, react-native, android-sdk |
| **game-developer** | Game developer | git, c-cpp, unity, python3 |

### Specialized
| Template | Description | Key Tools |
|----------|-------------|-----------|
| **blockchain-developer** | Blockchain dev | git, nodejs, ethereum, docker |
| **iot-developer** | IoT developer | git, python3, arduino, raspberry-pi, mqtt |
| **embedded-developer** | Embedded dev | git, c-cpp, arduino, esp32, cmake |
| **security-engineer** | Security engineer | git, python3, docker, openssl, go |
| **qa-engineer** | QA/testing engineer | git, python3, nodejs, docker, postgresql |

### Language-Specific
| Template | Description | Key Tools |
|----------|-------------|-----------|
| **python-developer** | Python specialist | git, python3, vscode, poetry, docker |
| **java-developer** | Java specialist | git, java, vscode, maven, docker |
| **go-developer** | Go specialist | git, go, vscode, docker, kubernetes |
| **rust-developer** | Rust specialist | git, rust, vscode, cargo |

Apply a template:
```python
agent = DevSetupAgent()
result = agent.execute_command(
    AgentCommand.APPLY_TEMPLATE,
    {"template_name": "web-developer"}
)
```

## 🧠 Smart Recommendation Engine

The system analyzes your needs and suggests the best tools:

```python
from core.agent_interface import DevSetupAgent, AgentCommand

agent = DevSetupAgent()

# Get personalized recommendations
result = agent.execute_command(
    AgentCommand.RECOMMEND_TOOLS,
    {
        "style": "full-stack",
        "size": "medium",
        "cloud": "aws",
        "existing": ["git"]
    }
)

# Get installation plan with phases
plan = result.data
```

The recommender considers:
- Your development style
- Team size
- Cloud provider preference
- Tools you already have
- Compatibility checks

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
