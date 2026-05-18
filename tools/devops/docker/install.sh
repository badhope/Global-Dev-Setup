#!/usr/bin/env bash

################################################################################
# Docker Installation Script
################################################################################

set -e

echo "🐳 Installing Docker..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Install Docker on Linux
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER

    # Install Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

elif [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v brew &> /dev/null; then
        brew install --cask docker
    fi
fi

echo "✅ Docker installation completed!"
docker --version
docker-compose --version
