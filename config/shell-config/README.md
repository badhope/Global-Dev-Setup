# Shell Configuration

## Supported Shells

- Bash
- Zsh (recommended)
- Fish

## Installation

### Bash

```bash
cp .bashrc ~/
source ~/.bashrc
```

### Zsh

```bash
cp .zshrc ~/
source ~/.zshrc

# Install Oh My Zsh (recommended)
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### Fish

```bash
cp .config/fish/config.fish ~/
```

## Features

### Aliases
- `ll` - Long list with details
- `la` - List all files
- `gs` - Git status
- `ga` - Git add
- `gc` - Git commit
- `gp` - Git push
- `gl` - Git log

### Functions
- `mkcd` - Create directory and cd into it
- `extract` - Extract various archive types
- `backup` - Create backup of file

### Prompt
- Shows current directory
- Git branch and status
- Current git branch in different color
- Timestamp (optional)

## Customization

Edit the config files to customize:
- Aliases
- Environment variables
- PATH
- Functions
- Prompt

## Plugins (Zsh)

If using Oh My Zsh, these plugins are enabled:
- git
- docker
- python
- node
- vscode
