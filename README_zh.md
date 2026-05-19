# Global-Dev-Setup

> **通用开发者环境配置注册表**
> 为外部AI智能体提供的开发工具和环境模板查询系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Tools Count](https://img.shields.io/badge/tools-187+-green.svg)](tools/)
[![Templates](https://img.shields.io/badge/templates-19-blue.svg)](environment-templates/)

[English](README.md) | [中文](README_zh.md)

---

## 🎯 仓库定位

这个仓库是**数据源**，供外部AI智能体查询和安装开发环境。它本身不是AI智能体应用。

**外部智能体可以通过此仓库实现：**

1. **查询工具注册表** - 获取可用工具的详细信息
2. **搜索工具** - 按关键词或类别查找工具
3. **获取环境模板** - 访问预配置的开发环境
4. **获取安装命令** - 获取支持镜像源的操作系统安装指令
5. **生成安装脚本** - 为选定工具创建自动化安装脚本

---

## ✨ 核心特性

- 📚 **187+ 开发工具** - 全面覆盖所有IT领域
- 🔍 **智能搜索** - 按关键词、类别或标签搜索
- 🌐 **镜像源支持** - 为中国用户优化的下载源
- 🤖 **智能体API** - REST API和CLI接口供外部智能体集成
- 📋 **环境模板** - 19个预配置的开发环境
- 💻 **多平台支持** - Linux、macOS、Windows
- 📤 **数据导出** - 导出注册表为JSON供离线使用

---

## 📂 目录结构

```
Global-Dev-Setup/
├── README.md                    # 主文档（英文）
├── README_zh.md                # 主文档（中文）
├── CONTRIBUTING.md             # 贡献指南
├── LICENSE                     # MIT许可证
├── mirrors_config.yaml         # 镜像源配置
├── registry.py                 # 核心工具注册表模块
├── api.py                      # REST API服务
├── agent_helper.py             # 智能体集成辅助工具
├── index.html                  # Web可视化界面
├── tool_registry.json          # 导出的注册表数据
├── generate_tools.py           # 工具定义生成器
├── tools/                      # 工具定义（187+工具）
│   ├── programming-languages/  # Python、JavaScript、Go、Rust等
│   ├── web-frameworks/         # React、Vue、Angular、Next.js等
│   ├── databases/              # PostgreSQL、MySQL、MongoDB等
│   ├── devops/                # Docker、Kubernetes、Terraform等
│   ├── security/              # 安全和漏洞扫描工具
│   ├── monitoring/            # 可观测性和监控工具
│   ├── networking/            # Web服务器和代理
│   ├── testing/              # 测试框架
│   ├── ai-ml/               # 机器学习和AI工具
│   ├── big-data/            # 大数据处理工具
│   ├── messaging/           # 消息队列
│   ├── terminal/            # 终端工具
│   ├── system/              # 系统工具
│   └── ...
├── environment-templates/       # 环境模板（19个模板）
│   ├── fullstack-developer.yaml
│   ├── ai-ml-developer.yaml
│   ├── devops-engineer.yaml
│   └── ...
└── docs/                      # 附加文档
    ├── TOOLS_GUIDE.md
    ├── TEMPLATES_GUIDE.md
    └── API_REFERENCE.md
```

---

## 🚀 快速开始

### 外部智能体使用

```bash
# 克隆仓库
git clone https://github.com/badhope/Global-Dev-Setup.git
cd Global-Dev-Setup

# 列出所有工具
python registry.py --list-tools

# 搜索工具
python registry.py --search database

# 获取工具详情
python registry.py --tool docker

# 获取安装命令
python registry.py --install-cmd python --region cn

# 导出注册表为JSON
python registry.py --export
```

### 手动安装

```bash
# Linux/macOS
chmod +x install.sh
./install.sh

# Windows
install.bat
```

---

## 🔌 智能体API使用

### Python API

```python
from registry import ToolRegistry

# 初始化注册表
registry = ToolRegistry()

# 查询工具
tools = registry.list_tools()
tool = registry.get_tool("docker")

# 搜索
results = registry.search_tools("python")

# 获取安装命令
cmd = registry.get_installation_command("docker", os_type="linux")

# 导出为JSON
registry.export_to_json("my_registry.json")
```

### REST API

```bash
# 启动API服务
python api.py

# 查询接口
curl http://localhost:8000/tools
curl http://localhost:8000/templates
curl http://localhost:8000/tools/docker
```

---

## 📚 工具分类

| 分类 | 示例 | 工具数 |
|------|------|--------|
| **编程语言** | Python、JavaScript、Go、Rust | 25+ |
| **Web框架** | React、Vue、Angular、Next.js | 15+ |
| **数据库** | PostgreSQL、MySQL、MongoDB | 18+ |
| **DevOps** | Docker、Kubernetes、Terraform | 25+ |
| **安全工具** | SonarQube、Vault、OWASP ZAP | 10+ |
| **监控工具** | Prometheus、Grafana、ELK | 12+ |
| **网络工具** | Nginx、Traefik、Kong | 10+ |
| **测试工具** | Cypress、Playwright、Selenium | 10+ |
| **AI/ML** | PyTorch、TensorFlow、LangChain | 15+ |
| **大数据** | Spark、Hadoop、Kafka | 10+ |
| **终端工具** | tmux、fzf、ripgrep | 10+ |
| **系统工具** | htop、btop、neofetch | 10+ |

**总计：187+ 工具，覆盖60+ 分类**

---

## 📋 环境模板

### Web开发
- `fullstack-developer` - 全栈Web开发
- `frontend-developer` - 前端开发
- `backend-developer` - 后端开发

### AI与机器学习
- `ai-ml-developer` - AI/ML开发
- `ai-agent-developer` - AI Agent开发
- `ml-engineer` - 机器学习工程
- `data-science` - 数据科学环境

### 大数据与数据工程
- `big-data-engineer` - 大数据工程
- `data-engineering` - 数据管道开发

### DevOps与云原生
- `devops-engineer` - DevOps工程
- `cloud-native-developer` - 云原生开发
- `sysadmin` - 系统管理

### 专业领域
- `mobile-developer` - 移动应用开发
- `game-developer` - 游戏开发
- `blockchain-developer` - 区块链开发
- `iot-developer` - 物联网开发
- `embedded-developer` - 嵌入式系统
- `security-engineer` - 安全工程
- `qa-engineer` - QA与测试

### 语言专属
- `python-developer` - Python专精
- `java-developer` - Java专精
- `go-developer` - Go专精
- `rust-developer` - Rust专精

---

## 🌐 镜像源配置

仓库为中国用户优化了以下镜像源：

### 包管理器
- **pip**: 清华、豆瓣、阿里云
- **npm**: npmmirror、阿里云
- **Docker**: 中科大、网易、腾讯云
- **Go**: GOPROXY.CN、阿里云
- **Maven**: 阿里云、清华

### 工具下载
- **Python**: 华为云、清华
- **Node.js**: npmmirror、清华
- **Go**: 阿里云、Go官方CDN

### AI/ML模型
- **HuggingFace**: hf-mirror.com、ModelScope

配置文件：[mirrors_config.yaml](mirrors_config.yaml)

---

## 📖 文档

- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南
- [docs/TOOLS_GUIDE.md](docs/TOOLS_GUIDE.md) - 工具定义格式指南
- [docs/TEMPLATES_GUIDE.md](docs/TEMPLATES_GUIDE.md) - 模板创建指南
- [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - API参考文档
- [README.md](README.md) - 英文文档

---

## 🤝 贡献

欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

### 添加新工具

1. 创建目录：`tools/[category]/[tool-name]/`
2. 按照 [docs/TOOLS_GUIDE.md](docs/TOOLS_GUIDE.md) 中的格式创建 `tool.yaml`
3. 运行 `python registry.py --export` 更新注册表

### 添加新模板

1. 创建文件：`environment-templates/[template-name].yaml`
2. 按照 [docs/TEMPLATES_GUIDE.md](docs/TEMPLATES_GUIDE.md) 中的格式编写
3. 更新 `core/engine/smart_recommender.py` 中的模板映射

---

## 📄 许可证

MIT许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- 灵感来源于对标准化开发环境配置的需求
- 为外部AI智能体高效发现和安装工具而构建
- 欢迎社区贡献！

---

## 📞 支持

- **问题反馈**: [GitHub Issues](https://github.com/badhope/Global-Dev-Setup/issues)
- **讨论区**: [GitHub Discussions](https://github.com/badhope/Global-Dev-Setup/discussions)

---

**语言**: [English](README.md) | [中文](README_zh.md)
