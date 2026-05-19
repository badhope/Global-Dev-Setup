# Environment Template Guide

This guide explains how to create environment template files for the Global-Dev-Setup registry.

## 📁 File Structure

Templates are YAML files located at:
```
environment-templates/[template-name].yaml
```

Example:
```
environment-templates/ai-ml-developer.yaml
environment-templates/fullstack-developer.yaml
```

## 📝 Basic Structure

```yaml
# Template name - should match filename
name: template-name
# Short description
description: "A brief description of this environment"
# Template category
category: development-category
# Who should use this template
recommended_for:
  - "Target audience 1"
  - "Target audience 2"

# Required tools - must have
required_tools:
  - name: tool-name-1
    version: "version"
  - name: tool-name-2
    version: "version"

# Recommended tools - strongly suggested
recommended_tools:
  - name: tool-name-3
    version: "version"

# Optional tools - nice to have
optional_tools:
  - name: tool-name-4
    version: "version"

# Installation phases
installation_phases:
  phase_1:
    name: "Phase Name"
    tools: [tool1, tool2]
    description: "What this phase does"
  phase_2:
    name: "Phase Name"
    tools: [tool3, tool4]
    description: "What this phase does"

# Commands to run after installation
post_install_steps:
  - "command1"
  - "command2"

# Compatible templates
compatible_templates:
  - other-template-1
  - other-template-2
```

## 📦 Tool Lists

### Required Tools

Essential tools that must be installed:
```yaml
required_tools:
  - name: git
    version: "2.30+"
  - name: python3
    version: "3.11+"
  - name: docker
    version: "20+"
```

### Recommended Tools

Important but not essential:
```yaml
recommended_tools:
  - name: postgresql
    version: "15+"
  - name: redis
    version: "7.0+"
```

### Optional Tools

Nice to have:
```yaml
optional_tools:
  - name: elasticsearch
    version: "8.13+"
```

## 📋 Installation Phases

Organize tools into logical installation phases:

```yaml
installation_phases:
  phase_1:
    name: "Foundation Tools"
    tools: [git, python3]
    description: "Install version control and Python"
  
  phase_2:
    name: "Databases"
    tools: [postgresql, redis]
    description: "Install databases and cache"
  
  phase_3:
    name: "ML Frameworks"
    tools: [pytorch, tensorflow]
    description: "Install machine learning frameworks"
  
  phase_4:
    name: "Development Tools"
    tools: [vscode]
    description: "Install IDE"
```

## 🔄 Post-Installation Steps

Commands to run after tools are installed:

```yaml
post_install_steps:
  - "pip install numpy pandas matplotlib"
  - "npm install -g typescript eslint"
  - "docker ps"
  - "echo 'Environment ready!'"
```

## 🔗 Template Compatibility

Define which templates are related:

```yaml
compatible_templates:
  - web-developer
  - backend-developer
  - frontend-developer
```

## 📝 Example: AI Agent Developer Template

Here's a complete example:

```yaml
name: ai-agent-developer
description: "Complete environment for AI Agent development"
category: ai-ml
recommended_for:
  - "AI Agent developers"
  - "LLM application builders"
  - "Chatbot developers"
  - "RAG system developers"

required_tools:
  - name: python3
    version: "3.11+"
  - name: git
    version: "2.30+"
  - name: docker
    version: "20+"

recommended_tools:
  - name: pytorch
    version: "2.0+"
  - name: huggingface
    version: "4.30+"
  - name: jupyter
    version: "7.0+"
  - name: redis
    version: "7.0+"
  - name: postgresql
    version: "15+"
  - name: vscode
    version: "1.80+"

optional_tools:
  - name: tensorflow
    version: "2.15+"
  - name: langchain
    version: "latest"
  - name: llama-index
    version: "latest"

installation_phases:
  phase_1:
    name: "Foundation Tools"
    tools: [git, python3, docker]
    description: "Install version control, Python and Docker"
  
  phase_2:
    name: "Databases and Cache"
    tools: [redis, postgresql]
    description: "Install Redis and PostgreSQL for data storage"
  
  phase_3:
    name: "ML Frameworks"
    tools: [pytorch, huggingface]
    description: "Install PyTorch and Hugging Face transformers"
  
  phase_4:
    name: "Development Tools"
    tools: [jupyter, vscode]
    description: "Install Jupyter Lab and VS Code"
  
  phase_5:
    name: "LLM Frameworks"
    tools: [langchain, llama-index]
    description: "Install LangChain and LlamaIndex for LLM apps"

post_install_steps:
  - "pip install langchain llama-index openai anthropic"
  - "pip install pydantic fastapi uvicorn"
  - "pip install redis psycopg2-binary"
  - "docker run -d -p 6379:6379 --name redis redis:7-alpine"
  - "docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=secret --name postgres postgres:15"
  - "echo 'AI Agent development environment ready!'"

compatible_templates:
  - web-developer
  - backend-developer
  - data-science
  - ml-engineer
```

## 📝 Example: DevOps Engineer Template

```yaml
name: devops-engineer
description: "Complete environment for DevOps engineering"
category: devops
recommended_for:
  - "DevOps engineers"
  - "SRE engineers"
  - "Platform engineers"
  - "Cloud engineers"

required_tools:
  - name: docker
    version: "20+"
  - name: git
    version: "2.30+"
  - name: kubectl
    version: "1.29+"
  - name: terraform
    version: "1.7+"

recommended_tools:
  - name: helm
    version: "3.14+"
  - name: ansible
    version: "9.0+"
  - name: aws-cli
    version: "2.15+"
  - name: gcloud-cli
    version: "455+"
  - name: azure-cli
    version: "2.57+"

optional_tools:
  - name: argocd
    version: "latest"
  - name: prometheus
    version: "latest"
  - name: grafana
    version: "latest"

installation_phases:
  phase_1:
    name: "Container Foundation"
    tools: [git, docker, kubectl]
    description: "Install container runtime and Kubernetes CLI"
  
  phase_2:
    name: "Infrastructure as Code"
    tools: [terraform, ansible]
    description: "Install IaC tools"
  
  phase_3:
    name: "Cloud CLIs"
    tools: [aws-cli, gcloud-cli, azure-cli]
    description: "Install cloud provider CLIs"
  
  phase_4:
    name: "Kubernetes Tools"
    tools: [helm]
    description: "Install Helm package manager"

post_install_steps:
  - "helm repo add stable https://charts.helm.sh/stable"
  - "helm repo add bitnami https://charts.bitnami.com/bitnami"
  - "kubectl completion bash >> ~/.bashrc"
  - "echo 'DevOps environment ready!'"

compatible_templates:
  - cloud-native-developer
  - sysadmin
  - security-engineer
```

## 🎯 Best Practices

1. **Logical Phasing** - Group tools into logical installation phases
2. **Clear Descriptions** - Explain what each tool does
3. **Version Specifications** - Specify minimum required versions
4. **Comprehensive Tools** - Include required, recommended, and optional
5. **Post-Install Steps** - Include configuration and setup commands
6. **Template Compatibility** - Link related templates for upgrades

## 🔄 Template Categories

Use these category values:
- `web-development` - Web development
- `ai-ml` - AI and machine learning
- `big-data` - Big data engineering
- `devops` - DevOps and infrastructure
- `mobile` - Mobile development
- `game-dev` - Game development
- `security` - Security engineering
- `data-engineering` - Data engineering
- `embedded` - Embedded systems
- `blockchain` - Blockchain development

## 📚 See Also

- [CONTRIBUTING.md](../CONTRIBUTING.md) - General contribution guidelines
- [TOOLS_GUIDE.md](./TOOLS_GUIDE.md) - Tool definition format
- [API_REFERENCE.md](./API_REFERENCE.md) - API documentation
