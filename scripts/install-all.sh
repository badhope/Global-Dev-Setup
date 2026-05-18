#!/usr/bin/env bash

################################################################################
# Global-Dev-Setup - Master Installation Script
# Quick installer for 100+ development tools
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$ID
        else
            OS="linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
    else
        OS="unknown"
    fi
    echo "$OS"
}

# Main installation
main() {
    echo "=========================================="
    echo "  Global-Dev-Setup Installation"
    echo "  Universal Developer Environment Toolkit"
    echo "=========================================="
    echo ""

    # Detect OS
    OS=$(detect_os)
    log_info "Detected OS: $OS"
    echo ""

    # System update (Linux only)
    if [ "$OS" != "macos" ] && [ "$OS" != "windows" ]; then
        log_info "Updating package manager..."
        case "$OS" in
            ubuntu|debian)
                sudo apt update -qq
                sudo apt install -y curl wget git build-essential
                ;;
            fedora)
                sudo dnf update -y
                sudo dnf install -y curl wget git
                ;;
            arch)
                sudo pacman -Syuu --noconfirm
                sudo pacman install -y curl wget git
                ;;
        esac
    fi

    # Install basic tools
    log_info "Installing basic dependencies..."

    if [ "$OS" == "macos" ]; then
        if ! command -v brew &> /dev/null; then
            log_info "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install curl wget git
    fi

    # Install development tools by category
    log_info "Starting tool installation..."
    echo ""

    # Programming Languages
    if [ "$1" == "all" ] || [ "$1" == "languages" ] || [ -z "$1" ]; then
        log_info "Installing programming languages..."
        cd tools/programming-languages
        for lang in python javascript rust go java c-cpp ruby php; do
            if [ -d "$lang" ]; then
                cd "$lang"
                if [ -f "install.sh" ]; then
                    log_info "Installing $lang..."
                    chmod +x install.sh
                    ./install.sh || log_warning "Failed to install $lang"
                fi
                cd ..
            fi
        done
        cd ../..
    fi

    # Databases
    if [ "$1" == "all" ] || [ "$1" == "databases" ] || [ -z "$1" ]; then
        log_info "Installing databases..."
        cd tools/databases
        for db in postgresql mysql mongodb redis; do
            if [ -d "$db" ]; then
                cd "$db"
                if [ -f "install.sh" ]; then
                    log_info "Installing $db..."
                    chmod +x install.sh
                    ./install.sh || log_warning "Failed to install $db"
                fi
                cd ..
            fi
        done
        cd ../..
    fi

    # DevOps Tools
    if [ "$1" == "all" ] || [ "$1" == "devops" ] || [ -z "$1" ]; then
        log_info "Installing DevOps tools..."
        cd tools/devops
        for tool in docker kubernetes terraform; do
            if [ -d "$tool" ]; then
                cd "$tool"
                if [ -f "install.sh" ]; then
                    log_info "Installing $tool..."
                    chmod +x install.sh
                    ./install.sh || log_warning "Failed to install $tool"
                fi
                cd ..
            fi
        done
        cd ../..
    fi

    # Editors
    if [ "$1" == "all" ] || [ "$1" == "editors" ] || [ -z "$1" ]; then
        log_info "Installing code editors..."
        cd tools/editors
        for editor in vscode jetbrains; do
            if [ -d "$editor" ]; then
                cd "$editor"
                if [ -f "install.sh" ]; then
                    log_info "Installing $editor..."
                    chmod +x install.sh
                    ./install.sh || log_warning "Failed to install $editor"
                fi
                cd ..
            fi
        done
        cd ../..
    fi

    echo ""
    echo "=========================================="
    log_success "Installation completed!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "  1. Restart your terminal"
    echo "  2. Configure your tools"
    echo "  3. Check docs/getting-started.md"
    echo ""
}

# Usage
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "Usage: $0 [category|all]"
    echo ""
    echo "Categories:"
    echo "  all        - Install all tools"
    echo "  languages  - Install programming languages"
    echo "  databases - Install databases"
    echo "  devops    - Install DevOps tools"
    echo "  editors   - Install code editors"
    echo ""
    echo "Examples:"
    echo "  $0           # Install recommended tools"
    echo "  $0 all       # Install everything"
    echo "  $0 python    # Install only Python"
    exit 0
fi

# Run main
main "$1"
