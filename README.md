# Global-Dev-Setup

> **Universal Developer Environment Configuration Registry**
> A comprehensive, queryable registry of development tools and environment templates for external AI agents.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Tools Count](https://img.shields.io/badge/tools-187+-green.svg)](tools/)
[![Templates](https://img.shields.io/badge/templates-19-blue.svg)](environment-templates/)

[English](README.md) | [中文](README_zh.md)

---

## 🎯 Purpose

This repository is a **data source** for external AI agents to discover and install development environments. It's not an AI agent application itself.

**What external agents can do with this repository:**

1. **Query Tool Registry** - Get detailed information about available tools
2. **Search Tools** - Find tools by keywords or categories
3. **Get Environment Templates** - Access pre-defined development environment configurations
4. **Retrieve Installation Commands** - Get OS-specific installation instructions with mirror support
5. **Generate Installation Scripts** - Create automated installation scripts for selected tools

---

## ✨ Features

- 📚 **187+ Development Tools** - Comprehensive coverage across all IT domains
- 🔍 **Smart Search** - Search by keyword, category, or tags
- 🌐 **Mirror Support** - Optimized download sources for China region
- 🤖 **Agent API** - REST API and CLI for external agent integration
- 📋 **Environment Templates** - 19 pre-configured development environments
- 💻 **Multi-Platform** - Linux, macOS, Windows support
- 📤 **Data Export** - Export registry to JSON for offline use

---

## 📂 Directory Structure

```
Global-Dev-Setup/
├── README.md                    # Main documentation (English)
├── README_zh.md                # 中文文档 (Chinese)
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
├── mirrors_config.yaml         # Mirror source configurations
├── registry.py                 # Core tool registry module
├── api.py                      # REST API service
├── agent_helper.py             # Agent integration helper
├── index.html                  # Web visualization interface
├── tool_registry.json          # Exported registry data
├── generate_tools.py           # Tool definition generator
├── tools/                      # Tool definitions (187+ tools)
│   ├── programming-languages/  # Python, JavaScript, Go, Rust, etc.
│   ├── web-frameworks/         # React, Vue, Angular, Next.js, etc.
│   ├── databases/             # PostgreSQL, MySQL, MongoDB, etc.
│   ├── devops/                # Docker, Kubernetes, Terraform, etc.
│   ├── security/              # Security and vulnerability tools
│   ├── monitoring/            # Observability and monitoring tools
│   ├── networking/           # Web servers and proxies
│   ├── testing/              # Testing frameworks
│   ├── ai-ml/               # Machine learning and AI tools
│   ├── big-data/            # Big data processing tools
│   ├── messaging/           # Message queues
│   ├── terminal/            # Terminal tools
│   ├── system/              # System utilities
│   └── ...
├── environment-templates/       # Environment templates (19 templates)
│   ├── fullstack-developer.yaml
│   ├── ai-ml-developer.yaml
│   ├── devops-engineer.yaml
│   └── ...
└── docs/                      # Additional documentation
    ├── TOOLS_GUIDE.md
    ├── TEMPLATES_GUIDE.md
    └── API_REFERENCE.md
```

---

## 🚀 Quick Start

### For External Agents

```bash
# Clone the repository
git clone https://github.com/badhope/Global-Dev-Setup.git
cd Global-Dev-Setup

# List all tools
python registry.py --list-tools

# Search for tools
python registry.py --search database

# Get tool details
python registry.py --tool docker

# Get installation command
python registry.py --install-cmd python --region cn

# Export registry to JSON
python registry.py --export
```

### For Manual Installation

```bash
# Linux/macOS
chmod +x install.sh
./install.sh

# Windows
install.bat
```

---

## 🔌 Agent API Usage

### Python API

```python
from registry import ToolRegistry

# Initialize registry
registry = ToolRegistry()

# Query tools
tools = registry.list_tools()
tool = registry.get_tool("docker")

# Search
results = registry.search_tools("python")

# Get installation command
cmd = registry.get_installation_command("docker", os_type="linux")

# Export to JSON
registry.export_to_json("my_registry.json")
```

### REST API

```bash
# Start API server
python api.py

# Query endpoints
curl http://localhost:8000/tools
curl http://localhost:8000/templates
curl http://localhost:8000/tools/docker
```

---

## 📚 Tool Categories

| Category | Examples | Tools |
|----------|----------|-------|
| **Programming Languages** | Python, JavaScript, Go, Rust | 25+ |
| **Web Frameworks** | React, Vue, Angular, Next.js | 15+ |
| **Databases** | PostgreSQL, MySQL, MongoDB | 18+ |
| **DevOps** | Docker, Kubernetes, Terraform | 25+ |
| **Security** | SonarQube, Vault, OWASP ZAP | 10+ |
| **Monitoring** | Prometheus, Grafana, ELK | 12+ |
| **Networking** | Nginx, Traefik, Kong | 10+ |
| **Testing** | Cypress, Playwright, Selenium | 10+ |
| **AI/ML** | PyTorch, TensorFlow, LangChain | 15+ |
| **Big Data** | Spark, Hadoop, Kafka | 10+ |
| **Terminal Tools** | tmux, fzf, ripgrep | 10+ |
| **System Tools** | htop, btop, neofetch | 10+ |

**Total: 187+ tools across 60+ categories**

---

## 📋 Environment Templates

### Web Development
- `fullstack-developer` - Full-stack web development
- `frontend-developer` - Frontend specialization
- `backend-developer` - Backend specialization

### AI & Machine Learning
- `ai-ml-developer` - AI/ML development
- `ai-agent-developer` - AI Agent development
- `ml-engineer` - Machine learning engineering
- `data-science` - Data science environment

### Big Data & Data Engineering
- `big-data-engineer` - Big data engineering
- `data-engineering` - Data pipeline development

### DevOps & Cloud
- `devops-engineer` - DevOps engineering
- `cloud-native-developer` - Cloud native development
- `sysadmin` - System administration

### Specialized
- `mobile-developer` - Mobile app development
- `game-developer` - Game development
- `blockchain-developer` - Blockchain development
- `iot-developer` - IoT development
- `embedded-developer` - Embedded systems
- `security-engineer` - Security engineering
- `qa-engineer` - QA and testing

### Language-Specific
- `python-developer` - Python specialization
- `java-developer` - Java specialization
- `go-developer` - Go specialization
- `rust-developer` - Rust specialization

---

## 🌐 Mirror Configuration

The repository includes optimized mirror sources for China region:

### Package Managers
- **pip**: Tsinghua, Douban, Aliyun
- **npm**: npmmirror, Aliyun
- **Docker**: USTC, NetEase, Tencent Cloud
- **Go**: GOPROXY.CN, Aliyun
- **Maven**: Aliyun, Tsinghua

### Tool Downloads
- **Python**: Huawei Cloud, Tsinghua
- **Node.js**: npmmirror, Tsinghua
- **Go**: Aliyun, Go official CDN

### AI/ML Models
- **HuggingFace**: hf-mirror.com, ModelScope

Configuration file: [mirrors_config.yaml](mirrors_config.yaml)

---

## 📖 Documentation

- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute tools and templates
- [docs/TOOLS_GUIDE.md](docs/TOOLS_GUIDE.md) - Tool definition format guide
- [docs/TEMPLATES_GUIDE.md](docs/TEMPLATES_GUIDE.md) - Template creation guide
- [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - API documentation
- [README_zh.md](README_zh.md) - Chinese documentation

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Adding a New Tool

1. Create directory: `tools/[category]/[tool-name]/`
2. Create `tool.yaml` following the format in [docs/TOOLS_GUIDE.md](docs/TOOLS_GUIDE.md)
3. Run `python registry.py --export` to update registry

### Adding a New Template

1. Create file: `environment-templates/[template-name].yaml`
2. Follow format in [docs/TEMPLATES_GUIDE.md](docs/TEMPLATES_GUIDE.md)
3. Update template mapping in `core/engine/smart_recommender.py`

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by the need for standardized development environment configurations
- Built for external AI agents to discover and install tools efficiently
- Community contributions welcome!

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/badhope/Global-Dev-Setup/issues)
- **Discussions**: [GitHub Discussions](https://github.com/badhope/Global-Dev-Setup/discussions)

---

**Language**: [English](README.md) | [中文](README_zh.md)
