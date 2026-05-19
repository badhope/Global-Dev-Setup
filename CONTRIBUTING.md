# Contributing to Global-Dev-Setup

Thank you for your interest in contributing to Global-Dev-Setup!

## 🎯 How to Contribute

There are several ways to contribute:

1. **Add New Tools** - Expand the tool registry
2. **Create Templates** - Add new environment templates
3. **Improve Documentation** - Enhance guides and examples
4. **Fix Issues** - Report and fix bugs
5. **Add Mirror Sources** - Improve download sources for different regions

## 📝 Adding New Tools

### Step 1: Create Tool Directory

Create a directory for your tool:

```bash
mkdir -p tools/[category]/[tool-name]
```

Examples:
- `tools/programming-languages/rust`
- `tools/databases/postgresql`
- `tools/devops/kubernetes`

### Step 2: Create Tool Definition

Create a `tool.yaml` file following the format in [docs/TOOLS_GUIDE.md](docs/TOOLS_GUIDE.md).

Example:
```yaml
name: rust
category: programming-language
description: "Rust - Blazingly fast and memory-safe programming language"
homepage: "https://www.rust-lang.org/"
documentation: "https://doc.rust-lang.org/"
license: "MIT/Apache 2.0"
author: "Rust Project"

tags:
  - rust
  - systems-programming
  - memory-safe
  - high-performance

supported_os:
  - linux
  - macos
  - windows

installation_sources:
  - type: curl
    os: [linux, macos]
    description: "Rustup installer (recommended)"
    priority: 1
    command: |
      curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
      source "$HOME/.cargo/env"

verify_commands:
  - "rustc --version"
  - "cargo --version"

compatible_with:
  - docker
  - vscode
```

### Step 3: Test Your Definition

```bash
python registry.py --tool rust
```

### Step 4: Export Updated Registry

```bash
python registry.py --export
```

## 📋 Creating Environment Templates

### Step 1: Create Template File

Create a YAML file in `environment-templates/`:

```bash
# Example: environment-templates/new-developer.yaml
```

### Step 2: Define Template

Follow the format in [docs/TEMPLATES_GUIDE.md](docs/TEMPLATES_GUIDE.md).

```yaml
name: new-developer
description: "Environment for new developers"
category: development
recommended_for:
  - "Beginner developers"
  - "Learning programming"

required_tools:
  - name: git
    version: "2.30+"
  - name: python3
    version: "3.11+"

recommended_tools:
  - name: vscode
    version: "1.80+"

installation_phases:
  phase_1:
    name: "Foundation"
    tools: [git, python3]
    description: "Install basic tools"

post_install_steps:
  - "python3 --version"
  - "git --version"
```

### Step 3: Test Template

```bash
python registry.py --template new-developer
python registry.py --list-templates
```

## 🔧 Improving Documentation

### Documentation Files

- `README.md` - Main documentation (English)
- `README_zh.md` - Chinese documentation
- `docs/TOOLS_GUIDE.md` - Tool definition guide
- `docs/TEMPLATES_GUIDE.md` - Template creation guide
- `docs/API_REFERENCE.md` - API documentation

### Guidelines

1. **English Primary** - Use English for all code and comments
2. **Chinese Translation** - Add Chinese versions in README_zh.md
3. **Clear Examples** - Include working examples
4. **Update Both Languages** - Keep English and Chinese in sync

## 🐛 Reporting Issues

### Before Creating an Issue

1. Search existing issues
2. Verify the issue with latest version
3. Check if tool definition needs update

### Creating an Issue

Use the issue template and include:
- Tool name and version
- Operating system
- Expected behavior
- Actual behavior
- Error messages

## 🔄 Pull Request Process

### 1. Fork the Repository

```bash
git clone https://github.com/badhope/Global-Dev-Setup.git
cd Global-Dev-Setup
```

### 2. Create a Branch

```bash
git checkout -b feature/new-tool
```

### 3. Make Your Changes

- Add tool definitions
- Create templates
- Update documentation
- Fix issues

### 4. Test Your Changes

```bash
# Test registry
python registry.py --export
python registry.py --tool your-new-tool

# Test template
python registry.py --template your-new-template
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "Add new-tool for new-developer category"
```

### 6. Push and Create PR

```bash
git push origin feature/new-tool
```

Then create a Pull Request on GitHub.

## 📋 Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Add new tool
- [ ] Add new template
- [ ] Update existing tool
- [ ] Update documentation
- [ ] Bug fix

## Testing
How did you test your changes?

## Checklist
- [ ] Tool definition follows format
- [ ] Template follows format
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Registry exported
```

## 🏷️ Tool Naming Conventions

- Use lowercase names
- Use hyphens for multi-word names (e.g., `postgresql`, `vscode`)
- Match directory structure to tool name
- Use official names when possible

## 📂 Category Structure

Use existing categories when possible:
- `programming-language`
- `web-framework`
- `database`
- `devops`
- `security`
- `monitoring`
- `networking`
- `testing`
- `ai-ml`
- `big-data`
- `terminal`
- `system`

Create new categories only when necessary.

## 🌐 Mirror Source Guidelines

When adding mirror sources:

1. **Verify mirrors work** - Test before adding
2. **Prioritize by region** - CN mirrors for Chinese users
3. **Include official source** - Always have fallback
4. **Document in mirrors_config.yaml** - Keep organized

## ✅ Quality Standards

### Tool Definitions Must Include

- ✅ `name` - Tool name
- ✅ `category` - Category
- ✅ `description` - Short description
- ✅ `homepage` - Official website
- ✅ `tags` - Searchable tags
- ✅ `supported_os` - OS compatibility
- ✅ `installation_sources` - Installation methods
- ✅ `verify_commands` - Installation verification

### Templates Must Include

- ✅ `name` - Template name
- ✅ `description` - What it's for
- ✅ `recommended_for` - Target audience
- ✅ `required_tools` - Essential tools
- ✅ `recommended_tools` - Suggested tools
- ✅ `installation_phases` - Logical phases

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/badhope/Global-Dev-Setup/issues)
- **Discussions**: [GitHub Discussions](https://github.com/badhope/Global-Dev-Setup/discussions)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Global-Dev-Setup! 🎉
