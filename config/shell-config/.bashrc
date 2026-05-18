# ~/.bashrc - Bash Configuration for Global-Dev-Setup

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Colors
export CLICOLOR=1
export LSCOLORS=ExFxCxDxBxegedabagacad

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

# Common tools
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# Safety
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

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
export PATH="$HOME/bin:$PATH"
export PATH="/usr/local/bin:$PATH"

# History
HISTCONTROL=ignoreboth
HISTSIZE=10000
SHOPT -s histappend

# Prompt (simple version)
PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

# Enable color support
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
fi

# Useful environment variables
export EDITOR='vim'
export VISUAL='vim'

# Development environment
export DEV_DIR="$HOME/Development"

# Load additional configs
[ -f ~/.bash_aliases ] && . ~/.bash_aliases
[ -f ~/.bash_exports ] && . ~/.bash_exports
[ -f ~/.bash_functions ] && . ~/.bash_functions

# Welcome message
echo "Global-Dev-Setup loaded! Type 'help' for commands"
