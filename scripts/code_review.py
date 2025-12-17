"""
Automated Code Review for Controle Financeiro Project
"""

import os
import re
import ast
import subprocess
from pathlib import Path
from typing import List, Dict

CRITICAL_VIOLATIONS = []
QUALITY_ISSUES = []
SUGGESTIONS = []


def get_changed_files() -> List[str]:
    """Get list of changed Python files in the PR"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return [f for f in result.stdout.strip().split('\n') if f.endswith('.py')]
    except Exception as e:
        print(f"Error getting changed files: {e}")
        return []


def check_controller_violations(file_path: str, content: str) -> None:
    """Check for violations in controllers"""
    if "_controller.py" not in file_path:
        return
    
    if "import streamlit" in content or "from streamlit" in content:
        CRITICAL_VIOLATIONS.append(
            f"**{file_path}**: Controllers must NOT import streamlit"
        )
    
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not node.name.endswith("Controller"):
                    CRITICAL_VIOLATIONS.append(
                        f"**{file_path}**: Class '{node.name}' should end with 'Controller' suffix"
                    )
                
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                required = ["save", "list_all", "_init_table", "delete"]
                for method in required:
                    if method not in methods:
                        CRITICAL_VIOLATIONS.append(
                            f"**{file_path}**: Controller missing {method}() method"
                        )
    except SyntaxError:
        pass


def check_model_violations(file_path: str, content: str) -> None:
    """Check for violations in models/"""
    if "models/" not in file_path:
        return
    
    if "import streamlit" in content or "from streamlit" in content:
        CRITICAL_VIOLATIONS.append(
            f"**{file_path}**: Models must NOT import streamlit"
        )
    
    if "import sqlite3" in content or "from sqlite3" in content:
        CRITICAL_VIOLATIONS.append(
            f"**{file_path}**: Models must NOT import sqlite3 or database libraries"
        )


def check_page_violations(file_path: str, content: str) -> None:
    """Check for violations in pages"""
    if "_controller.py" in file_path or "models/" in file_path:
        return
    
    if "pages/" not in file_path or not file_path.endswith(".py"):
        return
    
    if "import sqlite3" in content or "from sqlite3" in content:
        CRITICAL_VIOLATIONS.append(
            f"**{file_path}**: Pages must NOT import sqlite3. Use controllers instead"
        )


def main() -> None:
    print("🔍 Starting code review...\n")
    
    changed_files = get_changed_files()
    print(f"Found {len(changed_files)} changed Python files\n")
    
    for file_path in changed_files:
        if not os.path.exists(file_path):
            continue
        
        print(f"Reviewing {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        check_model_violations(file_path, content)
        check_controller_violations(file_path, content)
        check_page_violations(file_path, content)
    
    print("\n" + "="*60)
    print("Review Summary:")
    print(f"  Critical Violations: {len(CRITICAL_VIOLATIONS)}")
    print("="*60 + "\n")
    
    if CRITICAL_VIOLATIONS:
        print("❌ Issues found:")
        for v in CRITICAL_VIOLATIONS:
            print(f"  {v}")
        exit(1)
    else:
        print("✅ Review passed!")
        exit(0)


if __name__ == "__main__":
    main()
