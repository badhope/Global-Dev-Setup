#!/usr/bin/env bash

################################################################################
# Python Installation Script
################################################################################

set -e

echo "🐍 Installing Python Development Environment..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-pip
    elif command -v pacman &> /dev/null; then
        sudo pacman -S python python-pip --noconfirm
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v brew &> /dev/null; then
        brew install python
    fi
fi

# Install Poetry (optional)
if command -v curl &> /dev/null; then
    curl -sSL https://install.python-poetry.org | python3 -
fi

echo "✅ Python installation completed!"
python3 --version
pip3 --version
