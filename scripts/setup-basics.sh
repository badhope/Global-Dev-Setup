#!/usr/bin/env bash

################################################################################
# Global-Dev-Setup - Basic Setup Script
# Sets up essential development environment
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        OS="unknown"
    fi
    echo "$OS"
}

# Install Git
install_git() {
    if ! command -v git &> /dev/null; then
        log "Installing Git..."
        case "$(detect_os)" in
            linux)
                if command -v apt-get &> /dev/null; then
                    sudo apt-get update
                    sudo apt-get install -y git
                elif command -v yum &> /dev/null; then
                    sudo yum install -y git
                elif command -v pacman &> /dev/null; then
                    sudo pacman -S git --noconfirm
                fi
                ;;
            macos)
                if command -v brew &> /dev/null; then
                    brew install git
                fi
                ;;
        esac
        success "Git installed"
    else
        log "Git already installed: $(git --version)"
    fi
}

# Install Curl
install_curl() {
    if ! command -v curl &> /dev/null; then
        log "Installing Curl..."
        case "$(detect_os)" in
            linux)
                if command -v apt-get &> /dev/null; then
                    sudo apt-get install -y curl
                elif command -v yum &> /dev/null; then
                    sudo yum install -y curl
                fi
                ;;
            macos)
                brew install curl
                ;;
        esac
        success "Curl installed"
    else
        log "Curl already installed"
    fi
}

# Configure Git
configure_git() {
    log "Configuring Git..."

    if [ -z "$(git config --global user.name)" ]; then
        read -p "Enter your name for Git: " GIT_NAME
        git config --global user.name "$GIT_NAME"
    fi

    if [ -z "$(git config --global user.email)" ]; then
        read -p "Enter your email for Git: " GIT_EMAIL
        git config --global user.email "$GIT_EMAIL"
    fi

    # Useful Git aliases
    git config --global alias.st "status"
    git config --global alias.co "checkout"
    git config --global alias.br "branch"
    git config --global alias.lg "log --oneline --graph --all"
    git config --global core.editor "vim"

    success "Git configured"
}

# Main
main() {
    echo "=========================================="
    echo "  Global-Dev-Setup - Basic Setup"
    echo "=========================================="
    echo ""

    install_git
    install_curl
    configure_git

    echo ""
    success "Basic setup completed!"
    echo ""
    echo "You can now install specific tools using:"
    echo "  ./scripts/install-all.sh"
    echo ""
}

main
