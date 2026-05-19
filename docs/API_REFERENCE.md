# API Reference

Complete API documentation for the Global-Dev-Setup registry.

## 📚 Registry API

### ToolRegistry Class

Main class for interacting with the tool registry.

#### Initialization

```python
from registry import ToolRegistry

# Initialize with auto region detection
registry = ToolRegistry()

# Initialize with specific region
registry = ToolRegistry(preferred_region='cn')

# Initialize without auto detection
registry = ToolRegistry(auto_detect_region=False, preferred_region='global')
```

#### Region Management

```python
# Set region
registry.set_region('cn')  # China mirrors
registry.set_region('global')  # Official sources

# Get current region
region = registry.get_region()
print(region.value)  # 'cn' or 'global'
```

### Tool Query Methods

#### list_tools()

Get list of all available tool names.

```python
tools = registry.list_tools()
# Returns: ['docker', 'python', 'git', ...]
```

#### list_categories()

Get list of all tool categories.

```python
categories = registry.list_categories()
# Returns: ['programming-language', 'database', 'devops', ...]
```

#### get_tool(tool_name)

Get detailed information about a specific tool.

```python
tool = registry.get_tool('docker')
# Returns: {name, category, description, installation_sources, ...}
```

#### search_tools(keyword)

Search tools by keyword in name, description, or tags.

```python
results = registry.search_tools('python')
# Returns: [{name, category, description, ...}, ...]
```

#### get_tools_by_category(category)

Get all tools in a specific category.

```python
tools = registry.get_tools_by_category('database')
# Returns: [{name, category, description, ...}, ...]
```

### Version Management

#### get_tool_versions(tool_name)

Get available versions for a tool.

```python
versions = registry.get_tool_versions('python')
# Returns: [ToolVersion(version='3.12', aliases=['3.12', 'latest'], ...), ...]
```

#### get_default_version(tool_name)

Get the default version for a tool.

```python
version = registry.get_default_version('python')
# Returns: ToolVersion or None
```

#### get_download_url(tool_name, version=None, os='linux', region=None)

Get download URL for a specific tool version and region.

```python
# Get default version URL
url = registry.get_download_url('python', os='linux')

# Get specific version URL
url = registry.get_download_url('python', version='3.11', os='linux')

# Get URL with CN mirror
url = registry.get_download_url('python', region='cn', os='linux')
```

### Installation Commands

#### get_installation_command(tool_name, os_type='linux', region=None, version=None)

Get the best installation command for a tool.

```python
# Get Linux installation command
cmd = registry.get_installation_command('docker', 'linux')

# Get with CN mirrors
cmd = registry.get_installation_command('docker', 'linux', 'cn')

# Get with specific version
cmd = registry.get_installation_command('python', 'linux', version='3.11')
```

#### generate_install_script(tool_names, os_type='linux', region=None, auto_fallback=True)

Generate a complete installation script.

```python
# Generate script for multiple tools
script = registry.generate_install_script(['git', 'python', 'docker'], 'linux')

# Save to file
with open('install.sh', 'w') as f:
    f.write(script)
```

### Template Methods

#### list_templates()

Get list of all templates.

```python
templates = registry.list_templates()
# Returns: ['fullstack-developer', 'ai-ml-developer', ...]
```

#### get_template(template_name)

Get detailed template information.

```python
template = registry.get_template('ai-ml-developer')
# Returns: {name, description, required_tools, ...}
```

#### get_template_tools(template_name)

Get all tools included in a template.

```python
tools = registry.get_template_tools('ai-ml-developer')
# Returns: [{tool: {...}, type: 'required', version: '3.11+'}, ...]
```

### Mirror Management

#### get_mirrors_for_package_manager(pm_type, region=None)

Get mirrors for a package manager.

```python
mirrors = registry.get_mirrors_for_package_manager('pip', 'cn')
# Returns: [MirrorInfo(url='...', name='Tsinghua', priority=1), ...]
```

#### get_best_mirror(pm_type, region=None)

Get the best (highest priority) mirror for a package manager.

```python
mirror = registry.get_best_mirror('npm', 'cn')
# Returns: MirrorInfo or None
```

#### find_fastest_mirror(pm_type, region=None)

Test and find the fastest mirror.

```python
mirror = registry.find_fastest_mirror('pip')
# Returns: MirrorInfo or None
```

### Export Methods

#### export_to_json(output_file='tool_registry.json')

Export the entire registry to JSON.

```python
registry.export_to_json('my_registry.json')
```

---

## 🌐 REST API

### Starting the API Server

```bash
python api.py
# Server runs on http://localhost:8000
```

### Endpoints

#### GET /

API information and available endpoints.

```bash
curl http://localhost:8000/
```

#### GET /tools

List all available tools.

```bash
curl http://localhost:8000/tools
```

#### GET /tools/{tool_name}

Get detailed information about a specific tool.

```bash
curl http://localhost:8000/tools/docker
```

#### GET /categories

List all tool categories.

```bash
curl http://localhost:8000/categories
```

#### GET /tools/category/{category}

Get all tools in a specific category.

```bash
curl http://localhost:8000/tools/category/database
```

#### GET /templates

List all environment templates.

```bash
curl http://localhost:8000/templates
```

#### GET /templates/{template_name}

Get detailed template information.

```bash
curl http://localhost:8000/templates/ai-ml-developer
```

#### GET /templates/{template_name}/tools

Get all tools in a template.

```bash
curl http://localhost:8000/templates/ai-ml-developer/tools
```

#### GET /search/{keyword}

Search tools by keyword.

```bash
curl http://localhost:8000/search/python
```

#### POST /recommend

Get tool recommendations based on requirements.

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"category": "ai-ml", "os": "linux"}'
```

#### GET /install-command/{tool_name}

Get installation command for a tool.

```bash
curl "http://localhost:8000/install-command/docker?os=linux"
```

#### GET /generate-script

Generate installation script for specified tools.

```bash
curl "http://localhost:8000/generate-script?tools=git,docker,python&os=linux"
```

---

## 🔧 Agent Helper

Simple helper for external agents to query the registry.

### AgentHelper Class

```python
from agent_helper import AgentHelper

helper = AgentHelper()
```

#### Basic Queries

```python
# List all tools
print(helper.list_tools())

# List categories
print(helper.list_categories())

# List templates
print(helper.list_templates())
```

#### Tool Information

```python
# Get tool details
info = helper.get_tool_info('docker')
print(info)

# Search tools
results = helper.search_tools('python')
print(results)

# Get tools by category
tools = helper.get_tools_by_category('database')
print(tools)
```

#### Recommendations

```python
# Get recommendations
recs = helper.get_recommendations('ai-ml')
print(recs)

# Get installation command
cmd = helper.get_install_command('docker')
print(cmd)
```

#### Export

```python
# Export entire registry
json_data = helper.export_registry()
print(json_data)
```

---

## 📋 Command Line Interface

### List Tools

```bash
python registry.py --list-tools
```

### List Categories

```bash
python registry.py --list-categories
```

### List Templates

```bash
python registry.py --list-templates
```

### Get Tool Details

```bash
python registry.py --tool docker
```

### Get Template Details

```bash
python registry.py --template ai-ml-developer
```

### Search Tools

```bash
python registry.py --search python
```

### Get Tools by Category

```bash
python registry.py --category database
```

### Get Installation Command

```bash
python registry.py --install-cmd docker --region cn --os linux
```

### Get Tool Versions

```bash
python registry.py --list-versions python
```

### Test Mirrors

```bash
python registry.py --test-mirrors pip
```

### Generate Install Script

```bash
python registry.py --gen-script git,docker,python --os linux
```

### Export Registry

```bash
python registry.py --export
```

### Set Region

```bash
python registry.py --region cn
```

---

## 📚 See Also

- [TOOLS_GUIDE.md](./TOOLS_GUIDE.md) - Tool definition format
- [TEMPLATES_GUIDE.md](./TEMPLATES_GUIDE.md) - Template creation guide
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
