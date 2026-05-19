# Tool Definition Guide

This guide explains how to create tool definition files for the Global-Dev-Setup registry.

## 📁 File Structure

Tool definitions are YAML files located at:
```
tools/[category]/[tool-name]/tool.yaml
```

Example:
```
tools/programming-languages/python/tool.yaml
tools/databases/postgresql/tool.yaml
tools/devops/docker/tool.yaml
```

## 📝 Basic Structure

```yaml
# Tool name - should match directory name
name: tool-name
# Category - should match parent directory
category: programming-language
# Short description
description: "A brief description of the tool"
# Official homepage
homepage: "https://example.com"
# Documentation URL
documentation: "https://example.com/docs"
# License type
license: "MIT"
# Author or organization
author: "Organization Name"

# Tags for searchability
tags:
  - tag1
  - tag2
  - tag3

# Supported operating systems
supported_os:
  - linux
  - macos
  - windows

# Installation sources (see below)
installation_sources: []

# Optional tools that complement this tool
optional_tools: []

# Environment variables to set
environment_vars: {}

# Commands to verify installation
verify_commands: []

# Tools this tool works well with
compatible_with: []
```

## 🔧 Installation Sources

The most important part is `installation_sources`. Each source should specify:

### Example: APT (Debian/Ubuntu)

```yaml
installation_sources:
  - type: apt
    os: [linux]
    package_name: package-name
    description: "Description of this installation method"
    priority: 1
    region_preference: ["global", "cn"]
    command: |
      sudo apt update
      sudo apt install -y package-name
```

### Example: Official Download

```yaml
installation_sources:
  - type: manual-download
    os: [linux, macos, windows]
    description: "Official binary download"
    priority: 1
    command: |
      wget https://example.com/tool.tar.gz
      tar -xzf tool.tar.gz
      sudo mv tool /usr/local/bin/
```

### Example: npm

```yaml
installation_sources:
  - type: npm
    os: [all]
    package_name: package-name
    description: "Install via npm"
    priority: 1
    command: npm install -g package-name
```

### Example: Docker

```yaml
installation_sources:
  - type: docker
    os: [all]
    image: "image-name:tag"
    description: "Run in Docker container"
    priority: 1
    command: docker run -d --name tool-name image-name:tag
```

## 📦 Version Support

For tools with multiple versions, use the `versions` field:

```yaml
versions:
  - version: "3.12"
    alias: ["3.12", "latest"]
    description: "Python 3.12 - Latest stable"
    supported_os: ["linux", "macos", "windows"]
    download_urls:
      global:
        linux: "https://example.com/v3.12/linux.tar.gz"
        macos: "https://example.com/v3.12/macos.pkg"
      cn:
        linux: "https://mirror.example.com/v3.12/linux.tar.gz"
    is_default: true
  
  - version: "3.11"
    alias: ["3.11"]
    description: "Python 3.11 - LTS"
    supported_os: ["linux", "macos", "windows"]
    download_urls:
      global:
        linux: "https://example.com/v3.11/linux.tar.gz"
```

## 🏷️ Tags

Tags are important for searchability. Common tags:

**Programming Languages:**
- `programming-language`, `script`, `compiled`, `functional`, `object-oriented`

**Web Frameworks:**
- `web-framework`, `frontend`, `backend`, `fullstack`, `spa`, `ssr`

**Databases:**
- `database`, `sql`, `nosql`, `relational`, `document`, `graph`, `time-series`

**DevOps:**
- `devops`, `ci-cd`, `container`, `orchestration`, `infrastructure`

## 🔗 Compatibility

The `compatible_with` field helps the smart recommender suggest related tools:

```yaml
compatible_with:
  - python3
  - docker
  - postgresql
```

## 📋 Optional Tools

Define tools that complement this tool:

```yaml
optional_tools:
  - name: plugin-name
    description: "Useful plugin or extension"
    recommended: true  # or false
```

## 🌐 Mirror Support

For Chinese users, support mirrors:

```yaml
pip_config:
  cn:
    index-url: "https://pypi.tuna.tsinghua.edu.cn/simple"
    trusted-host: "pypi.tuna.tsinghua.edu.cn"
  global:
    index-url: "https://pypi.org/simple"

npm_config:
  cn:
    registry: "https://registry.npmmirror.com"
  global:
    registry: "https://registry.npmjs.org"
```

## ✅ Verification

Always include verification commands:

```yaml
verify_commands:
  - "tool-name --version"
  - "tool-name --help"
```

## 📦 System Requirements

```yaml
system_requirements:
  disk_space: "500MB minimum"
  memory: "1GB minimum"
  cpu: "x86_64 architecture"
```

## 🔄 Fallback Sources

Define fallback installation methods:

```yaml
fallback_sources:
  - type: alternative-package
    os: [linux]
    reason: "Fallback if primary source fails"
```

## 📝 Example: Complete Tool Definition

Here's a complete example for Docker:

```yaml
name: docker
category: devops
description: "Docker - Container platform for developers"
homepage: "https://www.docker.com/"
documentation: "https://docs.docker.com/"
license: "Apache 2.0"
author: "Docker Inc."

tags:
  - docker
  - container
  - devops
  - microservices
  - containerization

supported_os:
  - linux
  - macos
  - windows

installation_sources:
  - type: docker-install-script
    os: [linux]
    description: "Official Docker Install Script with Mirror"
    priority: 1
    region_preference: ["cn", "global"]
    uses_mirrors: true
    command: |
      curl -fsSL https://get.daocloud.io/docker | sh
      sudo systemctl start docker
      sudo systemctl enable docker
  
  - type: apt-docker-ce
    os: [linux]
    description: "Docker CE APT Repository"
    priority: 2
    region_preference: ["global", "cn"]
    command: |
      sudo apt-get update
      sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
      echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
      sudo apt-get update
      sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

  - type: brew
    os: [macos]
    package_name: docker
    description: "Homebrew Docker"
    priority: 1

docker_registry_mirrors:
  cn:
    - "https://docker.mirrors.ustc.edu.cn"
    - "https://hub-mirror.c.163.com"
  global:
    - "https://registry-1.docker.io"

optional_tools:
  - name: docker-compose
    description: "Docker Compose - Container orchestration"
    recommended: true

environment_vars:
  DOCKER_CONFIG: "$HOME/.docker"

verify_commands:
  - "docker --version"
  - "docker info"
  - "docker run hello-world"

compatible_with:
  - kubernetes
  - docker-compose

system_requirements:
  disk_space: "10GB minimum, 50GB recommended"
  memory: "2GB minimum, 4GB recommended"
```

## 🎯 Best Practices

1. **Include multiple installation sources** - Different OS support
2. **Prioritize mirrors for CN region** - Better download speed
3. **Always add verification commands** - Ensure installation succeeded
4. **Use comprehensive tags** - Improve searchability
5. **Document compatibility** - Help with tool recommendations
6. **Include fallback sources** - Handle installation failures gracefully

## 📚 See Also

- [CONTRIBUTING.md](../CONTRIBUTING.md) - General contribution guidelines
- [TEMPLATES_GUIDE.md](./TEMPLATES_GUIDE.md) - Environment template format
- [API_REFERENCE.md](./API_REFERENCE.md) - API documentation
