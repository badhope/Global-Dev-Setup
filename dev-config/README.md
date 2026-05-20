# Dev-Config Template System

Welcome to the Global-Dev-Setup Dev-Config system!

## Overview

Dev-Config provides pre-configured settings and templates for various development tools and environments.

## Directory Structure

```
dev-config/
├── README.md                    # This file
├── dev-config.yaml              # Master configuration file
├── templates/                   # Configuration templates
│   ├── git/                    # Git configuration templates
│   ├── shell/                  # Shell configuration templates
│   ├── ide/                    # IDE configuration templates
│   ├── package-manager/        # Package manager configurations
│   ├── docker/                 # Docker configurations
│   ├── database/               # Database configurations
│   ├── web-server/             # Web server configurations
│   ├── ci-cd/                  # CI/CD configurations
│   └── cloud/                  # Cloud provider configurations
├── presets/                    # Pre-configured environment presets
│   ├── web-developer/
│   ├── ai-ml-developer/
│   ├── devops-engineer/
│   └── fullstack-developer/
└── scripts/                    # Configuration scripts
    ├── apply-config.sh
    ├── backup-config.sh
    └── restore-config.sh
```

## Quick Start

### Apply a Preset

```bash
# Apply a preset
bash dev-config/scripts/apply-config.sh web-developer

# List available presets
bash dev-config/scripts/apply-config.sh list

# Backup current config
bash dev-config/scripts/backup-config.sh

# Restore from backup
bash dev-config/scripts/restore-config.sh
```

### Apply Individual Configs

```bash
# Apply git config
git config --global include.path "$(pwd)/dev-config/templates/git/.gitconfig"

# Apply shell config
cat dev-config/templates/shell/.bashrc >> ~/.bashrc

# Copy VSCode extensions
cp dev-config/templates/ide/vscode/extensions.json ~/.vscode/extensions.json
```

## Available Presets

- `web-developer` - Web development preset (VSCode, git, browsers)
- `ai-ml-developer` - AI/ML preset (PyTorch, TensorFlow, Jupyter)
- `devops-engineer` - DevOps preset (Docker, Kubernetes, Terraform)
- `fullstack-developer` - Fullstack preset (Everything)
- `mobile-developer` - Mobile development preset (Flutter, Android Studio)

## Configuration Templates

### Git Configuration

```bash
dev-config/templates/git/
├── .gitconfig                 # Global git config
├── .gitignore_global          # Global git ignore
└── .gitcommit_template        # Commit template
```

### Shell Configuration

```bash
dev-config/templates/shell/
├── .bashrc                    # Bash config
├── .zshrc                    # Zsh config
├── .bash_aliases             # Bash aliases
└── .profile                  # Profile
```

### IDE Configuration

```bash
dev-config/templates/ide/
├── vscode/
│   ├── settings.json         # VSCode settings
│   ├── keybindings.json      # VSCode keybindings
│   └── extensions.json       # VSCode extensions
├── intellij/
│   └── config/               # IntelliJ config
└── pycharm/
    └── config/               # PyCharm config
```

### Package Manager Configurations

```bash
dev-config/templates/package-manager/
├── pip/
│   └── pip.conf              # pip config
├── npm/
│   └── .npmrc               # npm config
├── cargo/
│   └── config                # cargo config
└── yarn/
    └── .yarnrc               # yarn config
```

### Docker Configurations

```bash
dev-config/templates/docker/
├── daemon.json               # Docker daemon config
├── docker-compose.yml        # Default compose file
└── containers/               # Container templates
    ├── postgres.yml
    ├── redis.yml
    └── mongodb.yml
```

### Database Configurations

```bash
dev-config/templates/database/
├── postgresql/
│   └── postgresql.conf
├── mysql/
│   └── my.cnf
└── redis/
    └── redis.conf
```

## Creating Your Own Preset

1. Copy an existing preset:
```bash
cp -r dev-config/presets/web-developer dev-config/presets/my-preset
```

2. Edit the preset.yaml file in your new preset:
```yaml
name: my-preset
description: My personal development preset
configs:
  - git
  - shell
  - vscode
```

3. Create configuration files specific to your preset

4. Test your preset:
```bash
bash dev-config/scripts/apply-config.sh my-preset
```

## Mirror Configuration

Dev-Config works with Global-Dev-Setup's mirror system:

```bash
# Use CN mirrors
export GD_REGION=cn

# Apply config
bash dev-config/scripts/apply-config.sh web-developer
```

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for details.

## License

MIT License
