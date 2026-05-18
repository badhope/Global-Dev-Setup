# Global-Dev-Setup Configuration

## VS Code Essential Extensions

List of recommended VS Code extensions for different development scenarios.

### Programming Languages

#### Python
```
ms-python.python
ms-python.vscode-pylance
ms-python.debugpy
```

#### JavaScript/TypeScript
```
dbaeumer.vscode-eslint
esbenp.prettier-vscode
```

#### Java
```
redhat.java
vscjava.vscode-java-debug
vscjava.vscode-maven
```

#### Rust
```
rust-lang.rust-analyzer
vadimcn.vscode-lldb
```

#### Go
```
golang.go
ms-vscode.go
```

### Databases

#### General
```
mtxr.sqltools
mtxr.sqltools-driver-pg
```

### DevOps

#### Docker
```
ms-azuretools.vscode-docker
```

#### Kubernetes
```
ms-kubernetes-tools.vscode-kubernetes-tools
```

### Productivity

#### General
```
visualstudioexptteam.vscodeintellicode
GitHub.copilot
GitHub.copilot-chat
```

#### Version Control
```
eamodio.gitlens
```

#### Documentation
```
shd101wyang.markdown-all-in-one
```

### UI/Design

#### Theming
```
Dracula.theme
One Dark Pro
```

#### Icons
```
vscode-icons-team.vscode-icons
```

## Installation

Install all extensions:
```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
# ... and so on
```

Or install from file:
```bash
cat extensions.txt | xargs -I {} code --install-extension {}
```
