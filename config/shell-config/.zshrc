# ~/.zshrc - Zsh Configuration for Global-Dev-Setup

# If not running interactively, don't do anything
[[ -o interactive ]] || return

# History
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt HIST_IGNORE_DUPS
setopt HIST_FIND_NO_DUPS
setopt HIST_IGNORE_SPACE
setopt SHARE_HISTORY
setopt APPEND_HISTORY

# Core settings
setopt AUTO_CD
setopt CORRECT
setopt NO_BEEP

# Colors
autoload -U colors && colors

# Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph --all'
alias gd='git diff'
alias gco='git checkout'

# Docker aliases
alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias di='docker images'

# Python aliases
alias py='python3'
alias pip='pip3'

# Safety
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# Functions
mkcd() {
    mkdir -p "$1" && cd "$1"
}

extract() {
    if [ -f "$1" ]; then
        case "$1" in
            *.tar.bz2) tar xjf "$1" ;;
            *.tar.gz) tar xzf "$1" ;;
            *.bz2) bunzip2 "$1" ;;
            *.rar) unrar x "$1" ;;
            *.gz) gunzip "$1" ;;
            *.tar) tar xf "$1" ;;
            *.tbz2) tar xjf "$1" ;;
            *.tgz) tar xzf "$1" ;;
            *.zip) unzip "$1" ;;
            *.Z) uncompress "$1" ;;
            *) echo "'$1' cannot be extracted via extract()" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}

# PATH configuration
export PATH="$HOME/bin:/usr/local/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"

# Development directories
export DEV_DIR="$HOME/Development"

# Editor
export EDITOR='vim'
export VISUAL='vim'

# Load additional configs
[ -f ~/.zsh_aliases ] && source ~/.zsh_aliases
[ -f ~/.zsh_exports ] && source ~/.zsh_exports
[ -f ~/.zsh_functions ] && source ~/.zsh_functions

# Prompt
PROMPT='%F{green}%n@%m%f:%F{blue}%~%f$ '

# Enable completion
autoload -Uz compinit
compinit

# Enable menu selection
zstyle ':completion:*' menu select

# Case insensitive completion
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'

# Load colors
autoload -U promptinit
promptinit

# Welcome message
echo "Global-Dev-Setup loaded!"
