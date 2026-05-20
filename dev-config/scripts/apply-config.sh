#!/bin/bash
# Dev-Config Application Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
PRESETS_DIR="$ROOT_DIR/dev-config/presets"
TEMPLATES_DIR="$ROOT_DIR/dev-config/templates"
BACKUP_DIR="$HOME/.global-dev-setup/backup"

# Help function
print_help() {
    echo -e "${GREEN}Global-Dev-Setup - Dev-Config System${NC}"
    echo "Usage: $0 [options] <preset>"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -l, --list     List available presets"
    echo "  -b, --backup   Backup current config before applying"
    echo "  -n, --no-backup Don't backup config"
    echo
    echo "Available presets:"
    list_presets
}

# List available presets
list_presets() {
    echo "  $(ls -1 "$PRESETS_DIR" 2>/dev/null || echo "None found")"
}

# Backup configuration
backup_config() {
    echo -e "${YELLOW}Creating backup of current config...${NC}"
    mkdir -p "$BACKUP_DIR"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/config_$timestamp.tar.gz"

    # Backup common config files
    tar czf "$backup_file" -C "$HOME" \
        .bashrc 2>/dev/null || true \
        .zshrc 2>/dev/null || true \
        .gitconfig 2>/dev/null || true \
        .vscode 2>/dev/null || true \
        .npmrc 2>/dev/null || true \
        .yarnrc 2>/dev/null || true

    echo -e "${GREEN}Backup saved to: $backup_file${NC}"
}

# Apply git config
apply_git_config() {
    echo -e "${GREEN}Applying git configuration...${NC}"
    local git_template="$TEMPLATES_DIR/git"

    if [ -f "$git_template/.gitconfig" ]; then
        cp "$git_template/.gitconfig" ~/.gitconfig
        git config --global --get user.name
        git config --global --get user.email
        echo -e "${GREEN}Git config applied!${NC}"
    fi

    if [ -f "$git_template/.gitignore_global" ]; then
        cp "$git_template/.gitignore_global" ~/.gitignore_global
        git config --global core.excludesfile ~/.gitignore_global
        echo -e "${GREEN}Git global ignore applied!${NC}"
    fi
}

# Apply shell config
apply_shell_config() {
    echo -e "${GREEN}Applying shell configuration...${NC}"
    local shell_template="$TEMPLATES_DIR/shell"

    if [ -f "$shell_template/.bashrc" ]; then
        if [ -f ~/.bashrc ]; then
            echo -e "${YELLOW}Backing up existing .bashrc...${NC}"
            cp ~/.bashrc ~/.bashrc.backup
        fi
        cp "$shell_template/.bashrc" ~/.bashrc
        echo -e "${GREEN}Bash config applied!${NC}"
    fi

    if [ -f "$shell_template/.zshrc" ]; then
        if [ -f ~/.zshrc ]; then
            echo -e "${YELLOW}Backing up existing .zshrc...${NC}"
            cp ~/.zshrc ~/.zshrc.backup
        fi
        cp "$shell_template/.zshrc" ~/.zshrc
        echo -e "${GREEN}Zsh config applied!${NC}"
    fi
}

# Apply VSCode config
apply_vscode_config() {
    echo -e "${GREEN}Applying VSCode configuration...${NC}"
    local vscode_template="$TEMPLATES_DIR/ide/vscode"

    mkdir -p ~/.config/Code/User
    mkdir -p ~/.vscode

    if [ -f "$vscode_template/settings.json" ]; then
        cp "$vscode_template/settings.json" ~/.config/Code/User/settings.json
        echo -e "${GREEN}VSCode settings applied!${NC}"
    fi

    if [ -f "$vscode_template/extensions.json" ]; then
        cp "$vscode_template/extensions.json" ~/.vscode/extensions.json
        echo -e "${GREEN}VSCode extensions list applied!${NC}"
    fi
}

# Apply package manager configs
apply_package_config() {
    echo -e "${GREEN}Applying package manager configurations...${NC}"
    local pm_template="$TEMPLATES_DIR/package-manager"

    # pip
    if [ -f "$pm_template/pip/pip.conf" ]; then
        mkdir -p ~/.pip
        cp "$pm_template/pip/pip.conf" ~/.pip/pip.conf
        echo -e "${GREEN}pip config applied!${NC}"
    fi

    # npm
    if [ -f "$pm_template/npm/.npmrc" ]; then
        cp "$pm_template/npm/.npmrc" ~/.npmrc
        echo -e "${GREEN}npm config applied!${NC}"
    fi

    # cargo
    if [ -f "$pm_template/cargo/config" ]; then
        mkdir -p ~/.cargo
        cp "$pm_template/cargo/config" ~/.cargo/config
        echo -e "${GREEN}cargo config applied!${NC}"
    fi
}

# Apply docker config
apply_docker_config() {
    echo -e "${GREEN}Applying docker configuration...${NC}"
    local docker_template="$TEMPLATES_DIR/docker"

    if [ -f "$docker_template/daemon.json" ]; then
        if [ -d /etc/docker ]; then
            sudo cp "$docker_template/daemon.json" /etc/docker/daemon.json
            echo -e "${GREEN}Docker daemon config applied!${NC}"
        else
            echo -e "${YELLOW}Docker not installed, skipping config.${NC}"
        fi
    fi
}

# Apply preset
apply_preset() {
    local preset_name=$1
    local preset_dir="$PRESETS_DIR/$preset_name"
    local preset_file="$preset_dir/preset.yaml"

    if [ ! -f "$preset_file" ]; then
        echo -e "${RED}Error: Preset '$preset_name' not found!${NC}"
        exit 1
    fi

    echo -e "${GREEN}Applying preset: $preset_name${NC}"

    # Parse preset and apply configs
    apply_git_config
    apply_shell_config
    apply_vscode_config
    apply_package_config
    apply_docker_config

    echo -e "${GREEN}Preset '$preset_name' applied successfully!${NC}"
}

# Main
main() {
    local backup=true
    local preset=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        key="$1"
        case $key in
            -h|--help)
                print_help
                exit 0
                ;;
            -l|--list)
                list_presets
                exit 0
                ;;
            -b|--backup)
                backup=true
                shift
                ;;
            -n|--no-backup)
                backup=false
                shift
                ;;
            *)
                if [ -z "$preset" ]; then
                    preset="$1"
                fi
                shift
                ;;
        esac
    done

    if [ -z "$preset" ]; then
        print_help
        exit 1
    fi

    # Backup if requested
    if [ "$backup" = true ]; then
        backup_config
    fi

    # Apply preset
    apply_preset "$preset"
}

main "$@"
