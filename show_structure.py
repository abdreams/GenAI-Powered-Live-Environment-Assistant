#!/usr/bin/env python3
"""
Project Structure Visualizer
Shows the complete file tree of the project
"""

import os
from pathlib import Path

def print_tree(directory, prefix="", ignore_dirs={'.git', '__pycache__', '.venv', 'venv', '.vscode'}):
    """Print directory tree structure"""
    entries = sorted(Path(directory).iterdir(), key=lambda x: (not x.is_dir(), x.name))
    entries = [e for e in entries if e.name not in ignore_dirs and not e.name.startswith('.')]
    
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        current_prefix = "└── " if is_last else "├── "
        print(f"{prefix}{current_prefix}{entry.name}")
        
        if entry.is_dir():
            extension = "    " if is_last else "│   "
            print_tree(entry, prefix + extension, ignore_dirs)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("GenAI-Powered Live Environment Assistant")
    print("Project Structure")
    print("="*60 + "\n")
    
    project_root = Path(__file__).parent
    print(f"📁 {project_root.name}/")
    print_tree(project_root)
    
    print("\n" + "="*60)
    print("Key Files:")
    print("="*60)
    print("📄 app.py                  - Main Streamlit application")
    print("📄 requirements.txt        - Python dependencies")
    print("📄 setup.sh                - Setup script")
    print("📄 run.sh                  - Run script")
    print("📄 README.md               - Project documentation")
    print("📄 QUICKSTART.md           - Quick start guide")
    print("📄 PROJECT_SUMMARY.md      - Complete project summary")
    print("📄 DEMO_SCRIPT.md          - Presentation guide")
    print("\n" + "="*60)
