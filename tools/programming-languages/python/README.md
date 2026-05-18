# 🐍 Python Development Environment

## 📖 Description

Complete Python development environment with:
- Python 3.11+ (latest stable)
- pip package manager
- virtualenv and venv
- Poetry (optional)
- Common packages

## 📋 Requirements

- Linux, macOS, or Windows with WSL
- 100MB disk space
- Internet connection

## 🚀 Installation

```bash
chmod +x install.sh
./install.sh
```

## ✅ Verification

```bash
python3 --version
pip3 --version
```

## 🔧 What Gets Installed

- Python 3.11/3.12
- pip (latest version)
- setuptools and wheel
- venv (built-in)
- Optional: Poetry, Pipenv

## 📝 Usage

### Create Virtual Environment

```bash
# Using venv
python3 -m venv myenv
source myenv/bin/activate

# Using Poetry (if installed)
poetry install
poetry shell
```

### Install Packages

```bash
pip install package-name
pip install -r requirements.txt
```

## 🔄 Updating

```bash
./install.sh
```

## 🗑️ Uninstalling

```bash
./uninstall.sh
```

## 📚 Resources

- [Python Official](https://www.python.org/)
- [pip Documentation](https://pip.pypa.io/)
- [Poetry Documentation](https://python-poetry.org/)
