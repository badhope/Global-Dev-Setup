# Contributing to Global-Dev-Setup

Thank you for your interest in contributing to Global-Dev-Setup! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Submission Guidelines](#submission-guidelines)
- [Style Guides](#style-guides)
- [Recognition](#recognition)

## Code of Conduct

By participating in this project, you agree to maintain a welcoming and respectful environment for everyone.

### Our Standards

- Be kind and courteous
- Respect differing viewpoints
- Focus on what is best for the community
- Show empathy towards others

### Our Responsibilities

Project maintainers are responsible for clarifying standards and willfairly and respectfully address issues and contributions.

## Ways to Contribute

### 🐛 Report Bugs

- Use GitHub Issues
- Include operating system and version
- Provide clear reproduction steps
- Include error messages and logs

### 💡 Suggest Features

- Open a GitHub Discussion first
- Explain the use case
- Provide examples
- Be open to feedback

### 📝 Improve Documentation

- Fix typos and grammar
- Add examples
- Improve clarity
- Translate to other languages

### 🔧 Add New Tools

- Follow the tool template
- Test on multiple platforms
- Include installation/uninstallation scripts
- Provide comprehensive documentation

### 🧪 Test & Review

- Test installation scripts
- Verify cross-platform compatibility
- Review pull requests
- Provide feedback

## Getting Started

### Prerequisites

- Git installed
- Text editor or IDE
- Basic command-line knowledge
- Enthusiasm! 🚀

### Fork the Repository

1. Click the "Fork" button on GitHub
2. Clone your fork:
```bash
git clone https://github.com/YOUR-USERNAME/Global-Dev-Setup.git
cd Global-Dev-Setup
```

3. Add upstream remote:
```bash
git remote add upstream https://github.com/badhope/Global-Dev-Setup.git
```

### Create a Branch

```bash
# For new tools
git checkout -b feature/add-new-tool

# For bug fixes
git checkout -b fix/issue-description

# For documentation
git checkout -b docs/improve-readme
```

## Development Process

### 1. Set Up Your Development Environment

```bash
# Install basic tools
./scripts/setup-basics.sh

# Verify setup
./scripts/test-environment.sh
```

### 2. Make Your Changes

- Follow the repository structure
- Use appropriate templates
- Test locally
- Keep changes focused

### 3. Write Tests (If Applicable)

```bash
# Run existing tests
./scripts/test-all.sh

# Add tests for new features
./scripts/add-test.sh
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: Add Python 3.11 installation support"
```

#### Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```
feat(databases): Add MongoDB installation support
fix(docker): Resolve permission issue on Linux
docs(readme): Update installation instructions
```

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Submit a Pull Request

1. Go to the original repository
2. Click "New Pull Request"
3. Select your branch
4. Fill in the template
5. Submit! 🎉

## Submission Guidelines

### Pull Request Checklist

- [ ] I have tested my changes locally
- [ ] My code follows the project's style
- [ ] I have updated documentation if needed
- [ ] My commit messages are clear
- [ ] I have added tests (if applicable)
- [ ] All tests pass

### Pull Request Template

```markdown
## Description
Brief description of changes

## Motivation
Why this change is needed

## Changes Made
- List of changes
- With bullet points

## Testing
How was this tested?

## Screenshots (If Applicable)
Add screenshots here

## Checklist
- [ ] Tested on Linux
- [ ] Tested on macOS
- [ ] Tested on Windows
- [ ] Documentation updated
- [ ] No breaking changes (or justified)
```

## Style Guides

### Documentation Style

- Use clear, concise language
- Include code examples
- Add headings and lists
- Keep formatting consistent

### Script Style

```bash
#!/usr/bin/env bash

# Comments in English
# Use 2-space indentation
# Quote variables
# Useerrexit for error handling

set -e

install_tool() {
    local version="$1"
    echo "Installing tool version: $version"
    # Installation logic here
}
```

### README Style

Each tool should have a README with:

1. **Title** - Tool name and emoji
2. **Description** - What it is
3. **Installation** - How to install
4. **Configuration** - Setup instructions
5. **Usage** - How to use
6. **Requirements** - Prerequisites
7. **Troubleshooting** - Common issues

## Recognition

Contributors will be:
- Listed in our CONTRIBUTORS.md file
- Mentioned in release notes
- Given credit in documentation
- Invited to contribute more! 🎉

## Questions?

- Open an issue
- Start a discussion
- Check existing issues
- Email maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Global-Dev-Setup!** 💖
