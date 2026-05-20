#!/bin/bash
# Bash configuration for Global-Dev-Setup

# Enable color support
export CLICOLOR=1
export LSCOLORS=ExFxBxDxCxegedabagacad

# History settings
export HISTSIZE=10000
export HISTFILESIZE=10000
export HISTCONTROL=ignoreboth:erasedups
export HISTTIMEFORMAT='%F %T '
shopt -s histappend
shopt -s cmdhist

# Better ls
alias ls='ls -G'
alias ll='ls -lG'
alias la='ls -AG'
alias l='ls -CFG'

# Git aliases
alias gs='git status'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gd='git diff'
alias ga='git add'
alias gb='git branch'
alias gco='git checkout'
alias gcm='git commit -m'
alias gcb='git checkout -b'
alias gca='git commit -a'
alias gcam='git commit -a -m'
alias gps='git push'
alias gpl='git pull'

# Directory navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'

# cd shortcuts
alias home='cd ~'
alias root='cd /'

# Quick edit
alias edbash='nano ~/.bashrc'
alias rebash='source ~/.bashrc'

# Quick view
alias path='echo $PATH'
alias now='date +"%Y-%m-%d %H:%M:%S"'

# Python
alias python=python3
alias pip=pip3
alias py=python
alias py2=python2
alias py3=python3

# Package management
alias apt-get='sudo apt-get'
alias apt='sudo apt'
alias update='sudo apt update'
alias upgrade='sudo apt upgrade -y'
alias install='sudo apt install -y'

# Network
alias ports='netstat -tulpn'
alias public-ip='curl ifconfig.me'
alias local-ip='ip addr'

# System
alias meminfo='free -m -l -t'
alias psmem='ps auxf | sort -nr -k 4'
alias psmem10='ps auxf | sort -nr -k 4 | head -10'
alias pscpu='ps auxf | sort -nr -k 3'
alias pscpu10='ps auxf | sort -nr -k 3 | head -10'
alias cpuinfo='lscpu'

# File operations
alias mv='mv -i'
alias cp='cp -i'
alias rm='rm -i'
alias mkdir='mkdir -p'

# Grep with color
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Diff with color
alias diff='colordiff'

# Use colordiff if available
if which colordiff >/dev/null; then
    alias diff='colordiff'
fi

# Enable programmable completion
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi

# Add local bin to PATH
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/bin:$PATH"

# Default editors
export EDITOR='nano'
export VISUAL='nano'

# Pager
export PAGER='less'
export LESS='-R'

# Prompt
PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

# Set default locale
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8

# Add timestamp to history
HISTTIMEFORMAT="%F %T "

# Append history, don't overwrite
shopt -s histappend

# Check window size
shopt -s checkwinsize

# Make less more friendly
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# Git branch in prompt
parse_git_branch() {
  git branch 2>/dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}

export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] $ "
