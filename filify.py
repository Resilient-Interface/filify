#!/usr/bin/env python3
"""
Filify/Defilify - Bidirectional Project Converter

Convert between single specification file and full directory structure.

Usage:
    python filify.py defilify <spec_file> [output_dir]    # File → Directory
    python filify.py filify <project_dir> [output_file]   # Directory → File

File Format:
    # ==================== path/to/file.ext ====================
    file content here
    
    # ==================== another/file.py ====================
    more content here
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple


class ProjectConverter:
    def __init__(self):
        self.file_separator_pattern = re.compile(r'^# ={10,} (.+?) ={10,}$', re.MULTILINE)
    
    def defilify(self, spec_file: str, output_dir: str = ".") -> None:
        """Convert specification file to directory structure"""
        print(f"📖 Reading: {spec_file}")
        
        with open(spec_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        files = self._parse_spec_file(content)
        self._create_directory_structure(files, output_dir)
        
        print(f"✅ Created {len(files)} files in {output_dir}")
    
    def filify(self, project_dir: str, output_file: str = "project.spec") -> None:
        """Convert directory structure to specification file"""
        print(f"📁 Scanning: {project_dir}")
        
        files = self._scan_directory(project_dir)
        content = self._generate_spec_content(files)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Generated {output_file} with {len(files)} files")
    
    def _parse_spec_file(self, content: str) -> Dict[str, str]:
        """Parse specification file into file dictionary"""
        files = {}
        
        # Split by file separators
        sections = self.file_separator_pattern.split(content)
        
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                filepath = sections[i].strip()
                file_content = sections[i + 1].strip()
                
                # Clean triple quotes if present
                if file_content.startswith('"""') and file_content.endswith('"""'):
                    file_content = file_content[3:-3].strip()
                elif file_content.startswith("'''") and file_content.endswith("'''"):
                    file_content = file_content[3:-3].strip()
                
                files[filepath] = file_content
                print(f"  📄 Parsed: {filepath}")
        
        return files
    
    def _scan_directory(self, project_dir: str) -> Dict[str, str]:
        """Scan directory and return file dictionary"""
        files = {}
        project_path = Path(project_dir)
        
        # Skip patterns
        skip_patterns = {
            '__pycache__', '.git', '.env', 'venv', 'node_modules', 
            '.pytest_cache', '*.pyc', '*.log', '.DS_Store'
        }
        
        def should_skip(path: Path) -> bool:
            return any(
                pattern in str(path) or path.name.startswith('.') and path.name != '.env.example'
                for pattern in skip_patterns
            )
        
        for file_path in project_path.rglob('*'):
            if file_path.is_file() and not should_skip(file_path):
                try:
                    relative_path = file_path.relative_to(project_path)
                    
                    # Read file content
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        files[str(relative_path)] = content
                        print(f"  📄 Added: {relative_path}")
                    except UnicodeDecodeError:
                        print(f"  ⚠️  Skipped binary: {relative_path}")
                        
                except ValueError:
                    continue
        
        return files
    
    def _generate_spec_content(self, files: Dict[str, str]) -> str:
        """Generate specification file content"""
        content_parts = []
        
        # Sort files for consistent output
        sorted_files = sorted(files.items())
        
        for filepath, file_content in sorted_files:
            separator = f"# {'=' * 20} {filepath} {'=' * 20}"
            content_parts.append(separator)
            content_parts.append(file_content)
            content_parts.append("")  # Empty line between files
        
        return "\n".join(content_parts)
    
    def _create_directory_structure(self, files: Dict[str, str], output_dir: str) -> None:
        """Create directory structure from file dictionary"""
        base_path = Path(output_dir)
        
        for filepath, content in files.items():
            file_path = base_path / filepath
            
            # Create parent directories
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file content
            file_path.write_text(content, encoding='utf-8')
            print(f"  📄 Created: {filepath}")
            
            # Make shell scripts executable
            if filepath.endswith('.sh'):
                os.chmod(file_path, 0o755)


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python filify.py defilify <spec_file> [output_dir]")
        print("  python filify.py filify <project_dir> [output_file]")
        print()
        print("Examples:")
        print("  python filify.py defilify project.spec ./output")
        print("  python filify.py filify ./my-project project.spec")
        sys.exit(1)
    
    command = sys.argv[1]
    converter = ProjectConverter()
    
    try:
        if command == "defilify":
            spec_file = sys.argv[2]
            output_dir = sys.argv[3] if len(sys.argv) > 3 else "."
            
            if not os.path.exists(spec_file):
                print(f"❌ Specification file not found: {spec_file}")
                sys.exit(1)
            
            converter.defilify(spec_file, output_dir)
            
        elif command == "filify":
            project_dir = sys.argv[2]
            output_file = sys.argv[3] if len(sys.argv) > 3 else "project.spec"
            
            if not os.path.exists(project_dir):
                print(f"❌ Project directory not found: {project_dir}")
                sys.exit(1)
            
            converter.filify(project_dir, output_file)
            
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'filify' or 'defilify'")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()