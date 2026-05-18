# Installation Guide

This guide provides detailed installation instructions for all tools in Global-Dev-Setup.

## 📋 Table of Contents

- [General Installation](#general-installation)
- [Programming Languages](#programming-languages)
- [Databases](#databases)
- [DevOps Tools](#devops-tools)
- [Editors](#editors)
- [Configuration](#configuration)

## General Installation

### System Requirements

#### Minimum Requirements
- **OS**: Linux, macOS, or Windows 10/11
- **RAM**: 4GB
- **Disk**: 5GB free space
- **Internet**: Broadband connection

#### Recommended Requirements
- **RAM**: 8GB+
- **Disk**: 20GB+ free space
- **CPU**: Multi-core processor

### Installation Methods

#### Method 1: Quick Install (Recommended)

```bash
# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/badhope/Global-Dev-Setup/main/scripts/install-all.sh | bash

# Windows
irm https://raw.githubusercontent.com/badhope/Global-Dev-Setup/main/scripts/install-all.ps1 | iex
```

#### Method 2: Selective Install

```bash
# Clone the repository
git clone https://github.com/badhope/Global-Dev-Setup.git
cd Global-Dev-Setup

# Install specific category
cd tools/programming-languages
chmod +x install-all.sh
./install-all.sh
```

#### Method 3: Individual Tool Install

```bash
# Navigate to specific tool
cd tools/programming-languages/python

# Run installation
chmod +x install.sh
./install.sh
```

## Programming Languages

### Python

**Location**: `tools/programming-languages/python/`

#### What Gets Installed
- Python 3.11+
- pip package manager
- virtualenv
- Poetry (optional)
- pipenv (optional)

#### Installation
```bash
cd tools/programming-languages/python
chmod +x install.sh
./install.sh
```

#### Verification
```bash
python3 --version
pip3 --version
```

### JavaScript/Node.js

**Location**: `tools/programming-languages/javascript/`

#### What Gets Installed
- Node.js 20 LTS
- npm
- yarn (optional)
- pnpm (optional)

#### Installation
```bash
cd tools/programming-languages/javascript
chmod +x install.sh
./install.sh
```

#### Verification
```bash
node --version
npm --version
```

### Rust

**Location**: `tools/programming-languages/rust/`

#### What Gets Installed
- Rust toolchain
- Cargo package manager
- rustup

#### Installation
```bash
cd tools/programming-languages/rust
chmod +x install.sh
./install.sh
```

#### Verification
```bash
rustc --version
cargo --version
```

### Go

**Location**: `tools/programming-languages/go/`

#### Installation
```bash
cd tools/programming-languages/go
chmod +x install.sh
./install.sh
```

#### Verification
```bash
go version
```

### Java

**Location**: `tools/programming-languages/java/`

#### Installation
```bash
cd tools/programming-languages/java
chmod +x install.sh
./install.sh
```

#### Verification
```bash
java --version
```

## Databases

### PostgreSQL

**Location**: `tools/databases/postgresql/`

#### Installation
```bash
cd tools/databases/postgresql
chmod +x install.sh
./install.sh
```

#### Verification
```bash
psql --version
```

### MySQL

**Location**: `tools/databases/mysql/`

#### Installation
```bash
cd tools/databases/mysql
chmod +x install.sh
./install.sh
```

#### Verification
```bash
mysql --version
```

### MongoDB

**Location**: `tools/databases/mongodb/`

#### Installation
```bash
cd tools/databases/mongodb
chmod +x install.sh
./install.sh
```

#### Verification
```bash
mongod --version
```

### Redis

**Location**: `tools/databases/redis/`

#### Installation
```bash
cd tools/databases/redis
chmod +x install.sh
./install.sh
```

#### Verification
```bash
redis-server --version
```

## DevOps Tools

### Docker

**Location**: `tools/devops/docker/`

#### Prerequisites
- Root/sudo access
- 64-bit OS
- Virtualization enabled

#### Installation
```bash
cd tools/devops/docker
chmod +x install.sh
./install.sh
```

#### Verification
```bash
docker --version
docker-compose --version
```

### Kubernetes (kubectl)

**Location**: `tools/devops/kubernetes/`

#### Installation
```bash
cd tools/devops/kubernetes
chmod +x install.sh
./install.sh
```

#### Verification
```bash
kubectl version --client
```

### Terraform

**Location**: `tools/devops/terraform/`

#### Installation
```bash
cd tools/devops/terraform
chmod +x install.sh
./install.sh
```

#### Verification
```bash
terraform --version
```

## Editors

### VS Code

**Location**: `tools/editors/vscode/`

#### Installation
```bash
cd tools/editors/vscode
chmod +x install.sh
./install.sh
```

#### Install Extensions
```bash
code --install-extension ms-python.python
code --install-extension dbaeumer.vscode-eslint
```

### JetBrains

**Location**: `tools/editors/jetbrains/`

#### Installation
```bash
cd tools/editors/jetbrains
chmod +x install.sh
./install.sh
```

## Configuration

### Git Configuration

```bash
# Set your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Use recommended settings
cp -r config/git-config/* ~/.git-config/
```

### Shell Configuration

```bash
# For bash
cp config/shell-config/.bashrc ~/

# For zsh
cp config/shell-config/.zshrc ~/

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

### VS Code Extensions

```bash
# Install from config
code --install-extension $(cat config/vscode-extensions/extensions.txt | tr '\n' ' ')
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x install.sh
   ```

2. **Command Not Found**
   - Restart your terminal
   - Check PATH configuration

3. **Installation Fails**
   - Check system requirements
   - Update package manager
   - Check internet connection

## Updates

### Update All Tools
```bash
./scripts/update-all.sh
```

### Update Specific Tool
```bash
cd tools/[category]/[tool]
git pull
./install.sh
```

## Uninstallation

### Remove Tool
```bash
cd tools/[category]/[tool]
chmod +x uninstall.sh
./uninstall.sh
```

## Next Steps

After installation, see:
- [FAQ](faq.md) for common questions
- [Home](../README.md) for overview
- Tool-specific documentation in each directory
