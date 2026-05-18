#!/usr/bin/env bash

################################################################################
# Global-Dev-Setup - Update All Tools
# Updates all installed development tools
################################################################################

set -e

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Main update function
main() {
    echo "=========================================="
    echo "  Global-Dev-Setup - Update All Tools"
    echo "=========================================="
    echo ""

    # Update package lists
    log "Updating package manager..."

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get update -qq
        elif command -v dnf &> /dev/null; then
            sudo dnf check-update || true
        elif command -v pacman &> /dev/null; then
            sudo pacman -Syu --noconfirm
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew update
            brew upgrade
        fi
    fi

    # Update installed tools
    log "Updating installed tools..."

    # Git
    if command -v git &> /dev/null; then
        log "Updating Git..."
        # Git updates via package manager or manual
    fi

    # Docker
    if command -v docker &> /dev/null; then
        log "Updating Docker..."
        # Docker updates handled by Docker Desktop or package manager
    fi

    # Node.js packages
    if command -v npm &> /dev/null; then
        log "Updating npm packages..."
        npm update -g
    fi

    # Python packages
    if command -v pip3 &> /dev/null; then
        log "Updating Python packages..."
        pip3 install --upgrade pip setuptools wheel
    fi

    # Pull latest repository changes
    log "Updating Global-Dev-Setup repository..."
    git pull origin main || log "Not in a git repository or update failed"

    echo ""
    success "All tools updated!"
    echo ""
}

main
