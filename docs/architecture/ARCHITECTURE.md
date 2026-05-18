# Global-Dev-Setup Architecture

## Overview

Global-Dev-Setup is a modular, extensible system for managing development tools and environments.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (CLI)                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Install   │  │   Uninstall  │  │    Update    │       │
│  │   Command   │  │   Command    │  │   Command    │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                  │                │
│         └────────────────┴──────────────────┘                │
│                          │                                   │
│                   ┌──────▼──────┐                           │
│                   │   Command   │                           │
│                   │  Dispatcher │                           │
│                   └──────┬──────┘                           │
│                          │                                   │
├──────────────────────────┼──────────────────────────────────┤
│                          │                                   │
│  ┌───────────────────────▼────────────────────────┐        │
│  │               Core Engine                       │        │
│  │  ┌─────────────┐  ┌────────────┐  ┌────────┐ │        │
│  │  │  Dependency │  │   Tool     │  │ Verify │ │        │
│  │  │  Resolver   │  │  Installer │  │ Module │ │        │
│  │  └─────────────┘  └────────────┘  └────────┘ │        │
│  └───────────────────────┬───────────────────────┘        │
│                          │                                   │
│  ┌───────────────────────▼───────────────────────┐        │
│  │           Installation Sources                 │        │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌───────┐ │        │
│  │  │  apt   │ │  brew  │ │  pip   │ │ curl  │ │        │
│  │  └────────┘ └────────┘ └────────┘ └───────┘ │        │
│  └───────────────────────────────────────────────┘        │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                    Configuration Layer                        │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │  App Config     │  │  Tool Config    │                  │
│  │  Manager       │  │  Loader         │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                      Data Models                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     Tool     │  │  Dependency  │  │    Source    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Component Description

### 1. CLI Layer (User Interface)

**File**: `core/cli/cli.py`

**Responsibilities**:
- Parse command-line arguments
- Display information to users
- Route commands to appropriate handlers
- Format output with colors and formatting

**Components**:
- `CLI` class - Main interface
- `Colors` class - Terminal color codes
- Command handlers (install, uninstall, update, list, etc.)

### 2. Core Engine

**File**: `core/engine/engine.py`

**Responsibilities**:
- Orchestrate tool installation
- Manage dependencies
- Execute installation scripts
- Track installed tools
- Handle errors and rollback

**Components**:
- `ToolEngine` - Main orchestrator
- `DependencyResolver` - Handles dependencies
- `InstallationResult` - Result data class

### 3. Configuration System

**File**: `core/config/config.py`

**Responsibilities**:
- Load and save application configuration
- Manage installation profiles
- Track installed tools database
- Handle tool-specific configurations

**Components**:
- `ConfigManager` - Main config handler
- `AppConfig` - Application settings
- `ToolConfigLoader` - Tool config loader

### 4. Data Models

**File**: `core/models/models.py`

**Responsibilities**:
- Define core data structures
- Validate data integrity
- Serialize/deserialize data

**Components**:
- `Tool` - Tool definition
- `Dependency` - Dependency model
- `InstallationSource` - Installation source
- `SystemInfo` - System information
- Enums: `ToolStatus`, `ToolCategory`, `OSType`

### 5. Utility Layer

**Files**:
- `core/utils/exceptions.py` - Custom exceptions
- `core/utils/logger.py` - Logging system

**Responsibilities**:
- Provide error handling
- Log operations and errors
- Format messages

## Data Flow

### Installation Flow

```
User Command
    ↓
CLI Parser
    ↓
ToolEngine.install_tool()
    ↓
DependencyResolver.resolve()
    ↓
Install Dependencies (if any)
    ↓
Install Tool
    ↓
Verify Installation
    ↓
Register in Database
    ↓
Return Result
```

### Dependency Resolution Flow

```
Tool Definition
    ↓
Extract Dependencies
    ↓
Check Installed
    ↓
Install Missing
    ↓
Validate All
    ↓
Proceed/Abort
```

## Module Structure

```
core/
├── __init__.py
├── cli/
│   ├── __init__.py
│   └── cli.py
├── config/
│   ├── __init__.py
│   └── config.py
├── engine/
│   ├── __init__.py
│   └── engine.py
├── models/
│   ├── __init__.py
│   └── models.py
└── utils/
    ├── __init__.py
    ├── exceptions.py
    └── logger.py
```

## Extension Points

### 1. Installation Sources

New installation sources can be added by extending the `_install_from_source` method:

```python
def _install_custom_source(self, tool: Tool, source: InstallationSource):
    # Custom installation logic
    pass
```

### 2. Plugins

The plugin system allows extending functionality:

```python
# Install hooks
engine.install_hooks.append(my_hook_function)

# Uninstall hooks
engine.uninstall_hooks.append(my_hook_function)
```

### 3. Configuration

Custom configuration options can be added to `AppConfig`:

```python
@dataclass
class AppConfig:
    # ... existing fields ...
    my_custom_option: str = "default"
```

## Error Handling

The system uses a hierarchical exception structure:

```
GlobalDevSetupException (base)
├── InstallationError
├── DependencyError
├── ConfigurationError
├── ToolNotFoundError
└── ... (more specific errors)
```

All exceptions are caught and handled appropriately at each layer.

## Logging

The logging system provides:
- Console output (INFO level)
- File output (DEBUG level)
- Configurable log levels
- Automatic log rotation

## Configuration Files

### Main Configuration
`~/.config/global-dev-setup/config.json`

### Profiles
`~/.config/global-dev-setup/profiles.json`

### Installed Tools
`~/.config/global-dev-setup/installed.json`

### Logs
`~/.cache/global-dev-setup/`

## Thread Safety

The `ToolEngine` is designed to be thread-safe:
- No shared mutable state
- Configuration is read-only after initialization
- Thread-safe logging

## Performance Considerations

1. **Parallel Installation**: Batch installations can run in parallel
2. **Caching**: Tool configurations are cached
3. **Lazy Loading**: Tools are loaded on-demand
4. **Concurrent Execution**: Thread pool for batch operations

## Testing Strategy

Tests are organized in `tests/`:
- Unit tests for individual components
- Integration tests for workflows
- Mock external dependencies

## Security Considerations

1. **No arbitrary code execution**: Only predefined installation methods
2. **Input validation**: All user inputs are validated
3. **Path safety**: Paths are expanded and validated
4. **Permission checks**: File operations check permissions

## Future Enhancements

1. **GUI Interface**: Web or desktop GUI
2. **Remote Profiles**: Cloud-based installation profiles
3. **Rollback System**: Automatic rollback on failures
4. **Integrity Verification**: Checksum validation
5. **Repository System**: User-contributed tool collections
