#!/usr/bin/env python3
# 批量生成缺失的工具定义

import os

# 定义所有缺失的工具
MISSING_TOOLS = {
    # 数据库
    "oracle": {
        "category": "database",
        "description": "Oracle Database - 企业级关系数据库",
        "homepage": "https://www.oracle.com/database/",
        "tags": ["oracle", "database", "enterprise", "sql", "plsql"]
    },
    "sqlserver": {
        "category": "database",
        "description": "SQL Server - Microsoft企业级数据库",
        "homepage": "https://www.microsoft.com/en-us/sql-server/",
        "tags": ["sqlserver", "microsoft", "database", "enterprise"]
    },
    "dynamodb": {
        "category": "database",
        "description": "Amazon DynamoDB - 托管NoSQL数据库",
        "homepage": "https://aws.amazon.com/dynamodb/",
        "tags": ["dynamodb", "aws", "nosql", "serverless", "key-value"]
    },
    "cockroachdb": {
        "category": "database",
        "description": "CockroachDB - 分布式SQL数据库",
        "homepage": "https://www.cockroachlabs.com/",
        "tags": ["cockroachdb", "distributed", "sql", "scalable"]
    },
    # 容器
    "podman": {
        "category": "devops",
        "description": "Podman - Docker兼容的容器引擎",
        "homepage": "https://podman.io/",
        "tags": ["podman", "container", "docker-alternative", "oci"]
    },
    "minikube": {
        "category": "devops",
        "description": "Minikube - 本地Kubernetes测试环境",
        "homepage": "https://minikube.sigs.k8s.io/",
        "tags": ["minikube", "kubernetes", "local", "testing"]
    },
    "docker-compose": {
        "category": "devops",
        "description": "Docker Compose - 容器编排工具",
        "homepage": "https://docs.docker.com/compose/",
        "tags": ["docker-compose", "containers", "orchestration", "development"]
    },
    # CI/CD
    "github-actions": {
        "category": "devops",
        "description": "GitHub Actions - CI/CD工作流",
        "homepage": "https://github.com/features/actions",
        "tags": ["github-actions", "ci-cd", "automation", "github"]
    },
    "gitlab-ci": {
        "category": "devops",
        "description": "GitLab CI - CI/CD流水线",
        "homepage": "https://docs.gitlab.com/ee/ci/",
        "tags": ["gitlab-ci", "ci-cd", "gitlab", "automation"]
    },
    "circleci": {
        "category": "devops",
        "description": "CircleCI - CI/CD平台",
        "homepage": "https://circleci.com/",
        "tags": ["circleci", "ci-cd", "cloud", "automation"]
    },
    # 代码质量
    "eslint": {
        "category": "dev-tools",
        "description": "ESLint - JavaScript代码检查工具",
        "homepage": "https://eslint.org/",
        "tags": ["eslint", "lint", "javascript", "typescript", "code-quality"]
    },
    "prettier": {
        "category": "dev-tools",
        "description": "Prettier - 代码格式化工具",
        "homepage": "https://prettier.io/",
        "tags": ["prettier", "formatter", "code-style", "javascript"]
    },
    "black": {
        "category": "dev-tools",
        "description": "Black - Python代码格式化工具",
        "homepage": "https://black.readthedocs.io/",
        "tags": ["black", "python", "formatter", "code-style"]
    },
    "flake8": {
        "category": "dev-tools",
        "description": "Flake8 - Python代码检查工具",
        "homepage": "https://flake8.pycqa.org/",
        "tags": ["flake8", "python", "lint", "code-quality"]
    },
    # 消息队列
    "rabbitmq": {
        "category": "messaging",
        "description": "RabbitMQ - 消息队列系统",
        "homepage": "https://www.rabbitmq.com/",
        "tags": ["rabbitmq", "message-queue", "amqp", "messaging"]
    },
    "activemq": {
        "category": "messaging",
        "description": "ActiveMQ - 企业消息队列",
        "homepage": "https://activemq.apache.org/",
        "tags": ["activemq", "message-queue", "jms", "enterprise"]
    },
    "pulsar": {
        "category": "messaging",
        "description": "Apache Pulsar - 云原生消息平台",
        "homepage": "https://pulsar.apache.org/",
        "tags": ["pulsar", "messaging", "streaming", "cloud-native"]
    },
    "nats": {
        "category": "messaging",
        "description": "NATS - 高性能消息系统",
        "homepage": "https://nats.io/",
        "tags": ["nats", "messaging", "high-performance", "cloud-native"]
    },
    # 大数据
    "flink": {
        "category": "big-data",
        "description": "Apache Flink - 流处理框架",
        "homepage": "https://flink.apache.org/",
        "tags": ["flink", "streaming", "big-data", "real-time"]
    },
    "druid": {
        "category": "big-data",
        "description": "Apache Druid - 实时OLAP数据库",
        "homepage": "https://druid.apache.org/",
        "tags": ["druid", "olap", "analytics", "real-time"]
    },
    "pinot": {
        "category": "big-data",
        "description": "Apache Pinot - 实时分析数据库",
        "homepage": "https://pinot.apache.org/",
        "tags": ["pinot", "olap", "analytics", "real-time"]
    },
    # 缓存
    "memcached": {
        "category": "cache",
        "description": "Memcached - 分布式内存缓存",
        "homepage": "https://memcached.org/",
        "tags": ["memcached", "cache", "distributed", "in-memory"]
    },
    # API网关
    "kong-gateway": {
        "category": "api",
        "description": "Kong Gateway - 企业级API网关",
        "homepage": "https://konghq.com/products/kong-gateway/",
        "tags": ["kong", "api-gateway", "microservices", "api-management"]
    },
    "tyk": {
        "category": "api",
        "description": "Tyk - 开源API网关",
        "homepage": "https://tyk.io/",
        "tags": ["tyk", "api-gateway", "open-source", "api-management"]
    },
    # 文档工具
    "docusaurus": {
        "category": "docs",
        "description": "Docusaurus - 现代化文档框架",
        "homepage": "https://docusaurus.io/",
        "tags": ["docusaurus", "documentation", "react", "markdown"]
    },
    "mkdocs": {
        "category": "docs",
        "description": "MkDocs - 基于Markdown的文档工具",
        "homepage": "https://www.mkdocs.org/",
        "tags": ["mkdocs", "documentation", "markdown", "python"]
    },
    # 终端工具
    "oh-my-zsh": {
        "category": "terminal",
        "description": "Oh My Zsh - Zsh配置框架",
        "homepage": "https://ohmyz.sh/",
        "tags": ["oh-my-zsh", "zsh", "terminal", "shell"]
    },
    "powerlevel10k": {
        "category": "terminal",
        "description": "Powerlevel10k - Zsh主题",
        "homepage": "https://github.com/romkatv/powerlevel10k",
        "tags": ["powerlevel10k", "zsh", "theme", "terminal"]
    },
    "tmux": {
        "category": "terminal",
        "description": "tmux - 终端复用器",
        "homepage": "https://tmux.github.io/",
        "tags": ["tmux", "terminal", "multiplexer", "shell"]
    },
    "fzf": {
        "category": "terminal",
        "description": "fzf - 模糊搜索工具",
        "homepage": "https://github.com/junegunn/fzf",
        "tags": ["fzf", "fuzzy-search", "terminal", "productivity"]
    },
    "ripgrep": {
        "category": "terminal",
        "description": "ripgrep - 快速文件搜索",
        "homepage": "https://github.com/BurntSushi/ripgrep",
        "tags": ["ripgrep", "search", "terminal", "fast"]
    },
    "httpie": {
        "category": "terminal",
        "description": "HTTPie - 友好的HTTP客户端",
        "homepage": "https://httpie.io/",
        "tags": ["httpie", "http-client", "api", "terminal"]
    },
    "jq": {
        "category": "terminal",
        "description": "jq - JSON处理工具",
        "homepage": "https://stedolan.github.io/jq/",
        "tags": ["jq", "json", "terminal", "cli"]
    },
    # 系统工具
    "htop": {
        "category": "system",
        "description": "htop - 进程监控工具",
        "homepage": "https://htop.dev/",
        "tags": ["htop", "process", "monitoring", "system"]
    },
    "btop": {
        "category": "system",
        "description": "btop - 现代系统监控工具",
        "homepage": "https://github.com/aristocratos/btop",
        "tags": ["btop", "monitoring", "system", "terminal"]
    },
    "neofetch": {
        "category": "system",
        "description": "neofetch - 系统信息显示",
        "homepage": "https://github.com/dylanaraps/neofetch",
        "tags": ["neofetch", "system-info", "terminal", "shell"]
    },
    "lazygit": {
        "category": "system",
        "description": "lazygit - Git终端UI",
        "homepage": "https://github.com/jesseduffield/lazygit",
        "tags": ["lazygit", "git", "terminal", "ui"]
    },
    # AI/ML工具
    "mlflow": {
        "category": "ai-ml",
        "description": "MLflow - ML生命周期管理",
        "homepage": "https://mlflow.org/",
        "tags": ["mlflow", "machine-learning", "mlops", "tracking"]
    },
    "langchain": {
        "category": "ai-ml",
        "description": "LangChain - LLM应用框架",
        "homepage": "https://www.langchain.com/",
        "tags": ["langchain", "llm", "ai", "chatbot"]
    },
    "openai": {
        "category": "ai-ml",
        "description": "OpenAI API - AI服务接口",
        "homepage": "https://openai.com/",
        "tags": ["openai", "ai", "api", "llm"]
    },
    "ollama": {
        "category": "ai-ml",
        "description": "Ollama - 本地LLM运行工具",
        "homepage": "https://ollama.com/",
        "tags": ["ollama", "llm", "local", "ai"]
    },
    # 版本控制
    "git-lfs": {
        "category": "version-control",
        "description": "Git LFS - 大文件存储",
        "homepage": "https://git-lfs.com/",
        "tags": ["git-lfs", "git", "large-files", "version-control"]
    },
    "dvc": {
        "category": "version-control",
        "description": "DVC - 数据版本控制",
        "homepage": "https://dvc.org/",
        "tags": ["dvc", "data-versioning", "mlops", "git"]
    },
    # 包管理
    "homebrew": {
        "category": "package-manager",
        "description": "Homebrew - macOS包管理器",
        "homepage": "https://brew.sh/",
        "tags": ["homebrew", "macos", "package-manager"]
    },
    "chocolatey": {
        "category": "package-manager",
        "description": "Chocolatey - Windows包管理器",
        "homepage": "https://chocolatey.org/",
        "tags": ["chocolatey", "windows", "package-manager"]
    },
    "scoop": {
        "category": "package-manager",
        "description": "Scoop - Windows命令行包管理器",
        "homepage": "https://scoop.sh/",
        "tags": ["scoop", "windows", "package-manager", "cli"]
    },
    # 云厂商
    "alibaba-cli": {
        "category": "cloud",
        "description": "Alibaba Cloud CLI - 阿里云命令行",
        "homepage": "https://www.alibabacloud.com/help/doc-detail/110343.htm",
        "tags": ["alibaba", "cloud", "cli", "aliyun"]
    },
    # 文档协作
    "notion": {
        "category": "productivity",
        "description": "Notion - 文档协作平台",
        "homepage": "https://www.notion.so/",
        "tags": ["notion", "productivity", "documentation", "collaboration"]
    },
    "slack": {
        "category": "productivity",
        "description": "Slack - 团队沟通工具",
        "homepage": "https://slack.com/",
        "tags": ["slack", "communication", "team", "collaboration"]
    },
    # 编辑器
    "neovim": {
        "category": "editor",
        "description": "Neovim - 现代化Vim编辑器",
        "homepage": "https://neovim.io/",
        "tags": ["neovim", "vim", "editor", "terminal"]
    },
    # 游戏开发
    "godot": {
        "category": "game-dev",
        "description": "Godot - 开源游戏引擎",
        "homepage": "https://godotengine.org/",
        "tags": ["godot", "game-engine", "open-source", "game-dev"]
    },
    "blender": {
        "category": "game-dev",
        "description": "Blender - 3D建模工具",
        "homepage": "https://www.blender.org/",
        "tags": ["blender", "3d", "modeling", "game-dev"]
    },
    # Web服务器
    "caddy": {
        "category": "networking",
        "description": "Caddy - 现代化Web服务器",
        "homepage": "https://caddyserver.com/",
        "tags": ["caddy", "web-server", "https", "automation"]
    },
    "apache": {
        "category": "networking",
        "description": "Apache HTTP Server - 老牌Web服务器",
        "homepage": "https://httpd.apache.org/",
        "tags": ["apache", "web-server", "http", "legacy"]
    },
    # 安全工具
    "snyk": {
        "category": "security",
        "description": "Snyk - 漏洞扫描工具",
        "homepage": "https://snyk.io/",
        "tags": ["snyk", "security", "vulnerability", "scanning"]
    },
    # 监控工具
    "datadog": {
        "category": "monitoring",
        "description": "Datadog - 云原生监控平台",
        "homepage": "https://www.datadoghq.com/",
        "tags": ["datadog", "monitoring", "cloud", "observability"]
    },
    "newrelic": {
        "category": "monitoring",
        "description": "New Relic - 应用性能监控",
        "homepage": "https://newrelic.com/",
        "tags": ["newrelic", "apm", "monitoring", "observability"]
    },
}

def generate_tool_yaml(tool_name, config):
    """生成工具定义YAML内容"""
    category = config["category"]
    path = f"tools/{category}/{tool_name}/tool.yaml"
    
    yaml_content = f"""# {tool_name.title()} - {config['description']}
name: {tool_name}
category: {category}
description: "{config['description']}"
homepage: "{config['homepage']}"

tags:
{chr(10).join([f'  - {tag}' for tag in config['tags']])}

supported_os:
  - linux
  - macos
  - windows

installation_sources:
  - type: official
    os: [all]
    description: "Official installation"
    priority: 1
    command: |
      # See {config['homepage']} for installation instructions

verify_commands:
  - "{tool_name} --version"

compatible_with: []
"""
    
    return path, yaml_content

def main():
    """主函数"""
    base_path = "/workspace/Global-Dev-Setup"
    count = 0
    
    for tool_name, config in MISSING_TOOLS.items():
        try:
            path, content = generate_tool_yaml(tool_name, config)
            full_path = os.path.join(base_path, path)
            
            # 创建目录
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # 写入文件
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            count += 1
            print(f"Created: {path}")
            
        except Exception as e:
            print(f"Error creating {tool_name}: {e}")
    
    print(f"\nTotal missing tools added: {count}")

if __name__ == "__main__":
    main()
