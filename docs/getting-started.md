# Getting Started

Welcome to Global-Dev-Setup! This guide will help you get started with setting up your development environment.

## 🎯 What is Global-Dev-Setup?

Global-Dev-Setup is a comprehensive toolkit that provides:

- **Quick Installation** - Install development tools with a single command
- **Organized Structure** - Tools are categorized for easy discovery
- **Cross-Platform** - Works on Linux, macOS, and Windows
- **Community Driven** - Open to contributions

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:

- A computer with Linux, macOS, or Windows 10/11
- Internet connection
- Basic command-line knowledge
- 5GB+ free disk space

### Step 1: Choose Your Platform

Select your operating system:

- **Linux** - Ubuntu, Debian, Fedora, Arch, etc.
- **macOS** - Apple Silicon or Intel
- **Windows** - Windows 10/11 with WSL2 recommended

### Step 2: Install Essential Tools

#### Linux/macOS

```bash
# Clone the repository
git clone https://github.com/badhope/Global-Dev-Setup.git
cd Global-Dev-Setup

# Run the basic setup
chmod +x scripts/setup-basics.sh
./scripts/setup-basics.sh
```

#### Windows

```powershell
# Open PowerShell as Administrator
# Clone the repository
git clone https://github.com/badhope/Global-Dev-Setup.git
cd Global-Dev-Setup

# Run the basic setup
.\scripts\setup-basics.ps1
```

### Step 3: Install Your Tools

Browse the `tools/` directory and install what you need:

```bash
# Example: Install Python
cd tools/programming-languages/python
chmod +x install.sh
./install.sh

# Example: Install Docker
cd ../../devops/docker
chmod +x install.sh
./install.sh
```

## 📦 Tool Categories

### Programming Languages
- Python, JavaScript, Rust, Go, Java, C/C++, Ruby, PHP

### Databases
- PostgreSQL, MySQL, MongoDB, Redis, SQLite

### DevOps Tools
- Docker, Kubernetes, Terraform, Ansible

### Code Editors
- VS Code, JetBrains IDEs, Vim, Neovim

### Productivity
- Git, tmux, zsh, bash

### Web Frameworks
- React, Vue, Angular, Next.js, Django

## 🔧 Basic Configuration

After installation, you may want to:

1. Configure your shell
2. Set up Git credentials
3. Install editor extensions
4. Customize your environment

See [Installation Guide](installation-guide.md) for detailed instructions.

## ❓ Need Help?

- Check the [FAQ](faq.md) for common questions
- Open an issue on GitHub
- Join our discussions

## ✅ Next Steps

Once you have your basic environment set up:

1. Explore the tools directory
2. Install tools specific to your workflow
3. Customize configurations
4. Keep tools updated

Happy coding! 🚀
