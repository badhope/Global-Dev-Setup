# Frequently Asked Questions (FAQ)

Common questions about Global-Dev-Setup.

## 📋 Table of Contents

- [General](#general)
- [Installation](#installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## General

### What is Global-Dev-Setup?

Global-Dev-Setup is a comprehensive toolkit that provides quick installation scripts and guides for 100+ development tools, including programming languages, databases, DevOps tools, editors, and productivity software.

### Why should I use it?

- **Saves Time** - One-command installation instead of manual setup
- **Organized** - All tools in one place, categorized
- **Cross-Platform** - Works on Linux, macOS, and Windows
- **Community Driven** - Open source and community supported
- **Well Documented** - Comprehensive guides and examples

### Is it free?

Yes! Global-Dev-Setup is completely free and open source under the MIT License.

### Which operating systems are supported?

- **Linux** - Ubuntu, Debian, Fedora, Arch, CentOS, and more
- **macOS** - Both Apple Silicon (M1/M2) and Intel
- **Windows** - Windows 10/11 with WSL2 recommended

## Installation

### How do I install all tools at once?

**Linux/macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/badhope/Global-Dev-Setup/main/scripts/install-all.sh | bash
```

**Windows:**
```powershell
irm https://raw.githubusercontent.com/badhope/Global-Dev-Setup/main/scripts/install-all.ps1 | iex
```

### How do I install specific tools?

```bash
# Clone the repository
git clone https://github.com/badhope/Global-Dev-Setup.git
cd Global-Dev-Setup

# Navigate to the tool
cd tools/programming-languages/python

# Run installation
chmod +x install.sh
./install.sh
```

### Do I need root/sudo access?

Most installations require root/sudo access for system-wide installation. If you don't have sudo access, you can install tools in your home directory by manually modifying installation paths.

### How much disk space do I need?

- **Minimal installation**: 5GB
- **Standard installation**: 15GB
- **Full installation**: 30GB+

### Can I install on Windows without WSL?

Yes, but we recommend using WSL2 for the best experience. Many tools work better in a Linux environment.

## Usage

### How do I keep tools updated?

```bash
# Update all tools
./scripts/update-all.sh

# Update specific tool
cd tools/[category]/[tool]
git pull
./install.sh
```

### Can I customize installations?

Yes! Each tool directory contains:
- `install.sh` - Main installation script
- `config/` - Configuration files
- `README.md` - Tool-specific documentation

### How do I uninstall tools?

```bash
cd tools/[category]/[tool]
chmod +x uninstall.sh
./uninstall.sh
```

### Are there any prerequisites?

For most installations:
- Git
- Curl/wget
- Basic command-line knowledge
- Internet connection

## Troubleshooting

### Installation fails with "Permission denied"

```bash
chmod +x install.sh
# or
sudo ./install.sh
```

### Command not found after installation

1. Restart your terminal
2. Check if the tool is in your PATH
3. Add to PATH if needed:
```bash
export PATH="$PATH:/path/to/tool/bin"
```

### Installation takes too long

- Check your internet connection
- Some tools download large packages
- Use a faster mirror if available

### Tools conflict with existing installations

- Use version managers (nvm, pyenv, rbenv, etc.)
- Install in separate directories
- Use containers (Docker) for isolated environments

### macOS shows security warning

Go to **System Preferences → Security & Privacy → General** and click "Allow" for the blocked application.

### Linux shows package manager errors

Update your package manager first:
```bash
# Ubuntu/Debian
sudo apt update

# Fedora
sudo dnf update

# Arch
sudo pacman -Syu
```

## Contributing

### How can I contribute?

1. Fork the repository
2. Create a feature branch
3. Add new tools or improve documentation
4. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

### Can I add new tools?

Absolutely! We welcome contributions. Please ensure:
- Tools are well-tested
- Installation scripts are cross-platform
- Documentation is complete

### I found a bug, what should I do?

Please open an issue on GitHub with:
- Operating system
- Steps to reproduce
- Error messages
- Expected vs actual behavior

### How do I report a security issue?

**Do NOT** open a public issue. Email us directly or use GitHub's private vulnerability reporting.

## Performance

### Why is installation slow?

- Large tool downloads (Docker images, SDKs)
- Network speed
- System resources
- Package compilation

### Can I speed up installation?

- Use parallel downloads
- Use faster mirrors
- Install only what you need
- Use pre-built binaries when available

## Maintenance

### How often are tools updated?

- Tool scripts: As needed
- Core repository: Weekly checks
- Critical updates: Immediate

### Who maintains this project?

This is a community-driven project maintained by volunteers. Contributions are welcome!

### How can I support the project?

- ⭐ Star the repository
- 🐛 Report bugs
- 📝 Improve documentation
- 🔧 Submit pull requests
- 📢 Share with others

## Still have questions?

- Open an issue on GitHub
- Check existing issues
- Join discussions
- Read tool-specific documentation

---

**Last Updated**: May 2026
