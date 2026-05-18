# 🐳 Docker Development Environment

## 📖 Description

Docker container platform for development:
- Docker Engine
- Docker Compose
- Docker CLI tools

## 📋 Requirements

- Linux, macOS, or Windows with WSL2
- 64-bit processor with virtualization
- 4GB RAM minimum
- 10GB disk space

## 🚀 Installation

```bash
chmod +x install.sh
sudo ./install.sh
```

## ✅ Verification

```bash
docker --version
docker-compose --version
docker run hello-world
```

## 📝 Usage

### Basic Commands

```bash
# Pull image
docker pull ubuntu:latest

# Run container
docker run -it ubuntu bash

# List containers
docker ps -a

# Build from Dockerfile
docker build -t myapp .
```

## 🔄 Updating

```bash
sudo ./install.sh
```

## 🗑️ Uninstalling

```bash
./uninstall.sh
```

## 📚 Resources

- [Docker Official](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Docker Hub](https://hub.docker.com/)
