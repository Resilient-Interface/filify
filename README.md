# Filify/Defilify

Bidirectional converter between single specification files and full directory structures.

## Description

**Defilify**: Convert a single specification file into a complete project directory structure with all files and folders.

**Filify**: Convert an existing project directory back into a single specification file for easy sharing, version control, or documentation.

## Usage

```bash
# Convert spec file to directory structure
python filify.py defilify <spec_file> [output_dir]

# Convert directory structure to spec file  
python filify.py filify <project_dir> [output_file]
```

## Examples

```bash
# Create project from specification
python filify.py defilify my-project.spec ./output

# Convert existing project to spec file
python filify.py filify ./my-webapp project.spec

# Use custom output locations
python filify.py defilify app.spec ./builds/v1.0
python filify.py filify ./src backup-$(date +%Y%m%d).spec
```

## File Format

The specification file uses a simple delimiter format:

```
# ==================== path/to/file.ext ====================
file content goes here
can be multiple lines
preserves formatting

# ==================== another/directory/file.py ====================
def hello():
    print("Hello World")

if __name__ == "__main__":
    hello()

# ==================== config/settings.json ====================
{
  "api_key": "your-key-here",
  "debug": true,
  "ports": [8000, 8080]
}

# ==================== static/style.css ====================
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
}
```

## File Format Rules

- **Delimiter**: `# ==================== filepath ====================`
- **Path**: Relative path from project root (forward slashes)
- **Content**: Everything between delimiters becomes file content
- **Encoding**: UTF-8 text files only (binary files skipped during filify)
- **Permissions**: Shell scripts (`.sh`) automatically made executable

## Features

### Defilify (Spec → Directory)
- Creates complete directory structure
- Preserves file content exactly
- Auto-creates missing parent directories
- Sets executable permissions for shell scripts

### Filify (Directory → Spec)
- Scans entire project recursively
- Skips common ignore patterns (`.git`, `__pycache__`, `node_modules`, etc.)
- Handles text files only (skips binaries)
- Maintains consistent file ordering

### Automatic Skipping
The following are automatically excluded during filify:
- Hidden files (except `.env.example`)
- Cache directories (`__pycache__`, `.pytest_cache`)
- Version control (`.git`)
- Dependencies (`node_modules`, `venv`)
- Build artifacts
- Log files

## Workflow Examples

### Project Development
```bash
# Start with specification
python filify.py defilify webapp.spec ./dev

# Work on project normally
cd dev
# ... edit files in IDE ...

# Convert back to spec for sharing
python filify.py filify ./dev webapp-updated.spec
```

### Version Control
```bash
# Before major changes
python filify.py filify ./project backup-pre-refactor.spec

# After changes  
python filify.py filify ./project current-state.spec

# Compare versions
diff backup-pre-refactor.spec current-state.spec
```

### Distribution
```bash
# Package entire project as single file
python filify.py filify ./my-app distribution.spec

# Recipient creates project
python filify.py defilify distribution.spec ./my-app
```

## Error Handling

- Missing input files/directories: Clear error message and exit
- Binary files during filify: Skipped with warning
- Permission issues: Reported but processing continues
- Invalid file paths: Sanitized and created safely

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)
