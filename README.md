# 🚀 Global-Dev-Setup

> **Universal Developer Environment Setup Toolkit**
> Quick installer for 100+ dev tools, SDKs, databases, editors, and productivity software.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/badhope/Global-Dev-Setup)](https://github.com/badhope/Global-Dev-Setup/stargazers)

## ✨ Features

- 📦 **100+ Development Tools** - Everything you need in one place
- ⚡ **Quick Installation** - One-click setup scripts
- 🔧 **Cross-Platform** - Windows, macOS, Linux support
- 📚 **Comprehensive Guides** - Step-by-step installation instructions
- 🔄 **Auto-Update** - Keep all tools up to date
- 🎯 **Category-Based** - Organized by functionality

## 📂 Directory Structure

```
Global-Dev-Setup/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── docs/
│   ├── getting-started.md
│   ├── installation-guide.md
│   └── faq.md
├── tools/
│   ├── programming-languages/
│   │   ├── python/
│   │   ├── javascript/
│   │   ├── rust/
│   │   ├── go/
│   │   └── java/
│   ├── databases/
│   │   ├── postgresql/
│   │   ├── mysql/
│   │   ├── mongodb/
│   │   └── redis/
│   ├── devops/
│   │   ├── docker/
│   │   ├── kubernetes/
│   │   └── ci-cd/
│   ├── editors/
│   │   ├── vscode/
│   │   ├── jetbrains/
│   │   └── vim/
│   ├── productivity/
│   │   ├── terminal/
│   │   ├── shell/
│   │   └── utilities/
│   └── frameworks/
│       ├── react/
│       ├── vue/
│       ├── angular/
│       └── nextjs/
├── scripts/
│   ├── install-all.sh
│   ├── update-all.sh
│   └── setup-basics.sh
└── config/
    ├── vscode-extensions.json
    ├── git-config/
    └── shell-config/
```

## 🎯 Quick Start

### One-Command Installation

**Linux/macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/badhope/Global-Dev-Setup/main/scripts/install-all.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/badhope/Global-Dev-Setup/main/scripts/install-all.ps1 | iex
```

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/badhope/Global-Dev-Setup.git
cd Global-Dev-Setup
```

2. Browse categories and select tools you need
3. Follow installation guides in each tool's directory

## 📦 Available Categories

### 🐍 Programming Languages
- **Python** - Python 3.x with pip, virtualenv, Poetry
- **JavaScript/Node.js** - Node.js, npm, yarn, pnpm
- **Rust** - Rust toolchain with Cargo
- **Go** - Go programming language
- **Java** - JDK 11/17/21
- **C/C++** - GCC, Clang, CMake
- **Ruby** - Ruby with RVM/Rbenv
- **PHP** - PHP with Composer

### 🗄️ Databases
- **PostgreSQL** - Advanced relational database
- **MySQL** - Popular RDBMS
- **MongoDB** - NoSQL document database
- **Redis** - In-memory data store
- **SQLite** - Lightweight database
- **Elasticsearch** - Search engine

### 🐳 DevOps & Containers
- **Docker** - Container platform
- **Kubernetes** - Container orchestration
- **Terraform** - Infrastructure as Code
- **Ansible** - Configuration management
- **Jenkins** - CI/CD pipeline
- **GitLab Runner** - GitLab CI

### 💻 Code Editors & IDEs
- **VS Code** - Microsoft's editor
- **JetBrains** - IntelliJ, PyCharm, WebStorm
- **Vim/Neovim** - Terminal editors
- **Emacs** - Extensible editor
- **Sublime Text** - Lightweight editor

### ⚡ Productivity Tools
- **Git** - Version control
- **tmux** - Terminal multiplexer
- **zsh/bash** - Shell configurations
- **fzf/ripgrep** - CLI fuzzy finder
- **httpie/curl** - HTTP clients

### 🌐 Web Frameworks
- **React** - UI library
- **Vue.js** - Progressive framework
- **Angular** - Platform framework
- **Next.js** - React framework
- **Django** - Python web framework
- **FastAPI** - Python API framework

### 🤖 AI/ML Tools
- **Python ML Stack** - NumPy, Pandas, Scikit-learn
- **TensorFlow** - ML framework
- **PyTorch** - Deep learning
- **Jupyter** - Interactive notebooks
- **Hugging Face** - NLP tools

### 🎨 Design & Documentation
- **Figma** - Design tool
- **Draw.io** - Diagrams
- **Swagger/OpenAPI** - API documentation
- **Docusaurus** - Documentation sites

## 📖 Documentation

- [Getting Started](docs/getting-started.md) - Begin your journey
- [Installation Guide](docs/installation-guide.md) - Detailed setup instructions
- [FAQ](docs/faq.md) - Frequently asked questions
- [Contributing Guide](CONTRIBUTING.md) - How to contribute

## 🛠️ Usage Examples

### Install Python Development Environment
```bash
cd tools/programming-languages/python
chmod +x install.sh
./install.sh
```

### Setup Docker Environment
```bash
cd tools/devops/docker
chmod +x install.sh
./install.sh
```

### Configure VS Code Extensions
```bash
cd config
code --install-extension < config/vscode-extensions.json
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) before submitting PRs.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-tool`)
3. Commit changes (`git commit -m 'Add amazing tool installation'`)
4. Push to branch (`git push origin feature/amazing-tool`)
5. Open a Pull Request

## 📋 Requirements

- **Operating System**: Linux, macOS, or Windows 10/11
- **Disk Space**: 5GB minimum for basic tools
- **Internet**: Required for downloading tools
- **Administrator/Root**: Required for system-wide installation

## 🔄 Keeping Updated

Pull latest changes:
```bash
git pull origin main
```

Update all tools:
```bash
./scripts/update-all.sh
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- All open-source tool maintainers
- Contributors to this repository
- Developer community

## 📞 Support

- Create an Issue for bugs
- Discussions for questions
- Star the repo if it helps you!

---

**⭐ If this repository helps you, please give it a star!**
