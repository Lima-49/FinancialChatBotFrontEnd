"""
Automated Code Review for Controle Financeiro Project
Validates architecture and code quality, then comments on PR
"""

import os
import re
import ast
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict


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


def check_model_violations(file_path: str, content: str) -> None:
    """Check for violations in models/"""
    if "models/" not in file_path:
        return
    
    # Check for streamlit imports
    if "import streamlit" in content or "from streamlit" in content:
        CRITICAL_VIOLATIONS.append(
            f"**{file_path}**: Models must NOT import streamlit"
        )
    
    # Check for database imports
    if "import sqlite3" in content or "from sqlite3" in content:
        CRITICAL_VIOLATIONS.append(
            f"**{file_path}**: Models must NOT import sqlite3 or database libraries"
        )
    
    # Check for controller imports
    if "import controllers" in content or "from controllers" in content:
        CRITICAL_VIOLATIONS.append(
            f"**{file_path}**: Models must NOT import controllers"
        )
    
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Skip Enum classes
                bases = [b.id if isinstance(b, ast.Name) else None for b in node.bases]
                if "Enum" in bases:
                    continue
                
                # Check Model suffix
                if not node.name.endswith("Model"):
                    CRITICAL_VIOLATIONS.append(
                        f"**{file_path}**: Class '{node.name}' should end with 'Model' suffix"
                    )
                
                # Check for required methods
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                if "from_dict" not in methods:
                    CRITICAL_VIOLATIONS.append(
                        f"**{file_path}**: Class '{node.name}' missing from_dict() method"
                    )
                if "to_dict" not in methods:
                    CRITICAL_VIOLATIONS.append(
                        f"**{file_path}**: Class '{node.name}' missing to_dict() method"
                    )
    except SyntaxError:
        pass


def check_controller_violations(file_path: str, content: str) -> None:
    """Check for violations in controllers"""
    if "_controller.py" not in file_path:
        return
    
    # Check for streamlit imports
    if "import streamlit" in content or "from streamlit" in content:
        CRITICAL_VIOLATIONS.append(
            f"**{file_path}**: Controllers must NOT import streamlit"
        )
    
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check Controller suffix
                if not node.name.endswith("Controller"):
                    CRITICAL_VIOLATIONS.append(
                        f"**{file_path}**: Class '{node.name}' should end with 'Controller' suffix"
                    )
                
                # Check for required methods
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                required = ["save", "list_all"]
                for method in required:
                    if method not in methods:
                        CRITICAL_VIOLATIONS.append(
                            f"**{file_path}**: Controller missing {method}() method"
                        )
    except SyntaxError:
        pass


def check_page_violations(file_path: str, content: str) -> None:
    """Check for violations in pages"""
    if "_controller.py" in file_path or "models/" in file_path:
        return
    
    if "pages/" not in file_path or not file_path.endswith(".py"):
        return
    
    # Check for direct database imports
    if "import sqlite3" in content or "from sqlite3" in content:
        CRITICAL_VIOLATIONS.append(
            f"**{file_path}**: Pages must NOT import sqlite3. Use controllers instead"
        )


def check_naming_conventions(file_path: str, content: str) -> None:
    """Check for naming convention violations"""
    try:
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            # Check function names (should be snake_case)
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_') and node.name not in ['__init__']:
                    if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                        QUALITY_ISSUES.append(
                            f"**{file_path}:{node.lineno}**: Function '{node.name}' should use snake_case"
                        )
            
            # Check class names (should be PascalCase)
            if isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    QUALITY_ISSUES.append(
                        f"**{file_path}:{node.lineno}**: Class '{node.name}' should use PascalCase"
                    )
    except SyntaxError:
        pass


def check_code_quality(file_path: str, content: str) -> None:
    """Check for general code quality issues"""
    
    # Check for hardcoded paths
    if re.search(r'["\']([A-Z]:\\|/home/|/Users/)', content):
        QUALITY_ISSUES.append(
            f"**{file_path}**: Contains hardcoded absolute paths. Use relative paths instead"
        )
    
    # Check for empty except blocks
    if re.search(r'except.*:\s*pass', content):
        QUALITY_ISSUES.append(
            f"**{file_path}**: Contains empty except block. Add proper error handling"
        )
    
    # Check for magic numbers
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if re.search(r'[=\(\[\,]\s*\d{2,}(?!\d)\s*[,\)\]\:]', line) and 'import' not in line:
            SUGGESTIONS.append(
                f"**{file_path}:{i}**: Consider extracting magic number to a named constant"
            )


def format_review_comment() -> str:
    """Format the review as a GitHub comment"""
    
    comment = "## 🤖 AI Code Review - Controle Financeiro\n\n"
    
    # Architecture Compliance
    if CRITICAL_VIOLATIONS:
        comment += "### ❌ Critical Architecture Violations\n\n"
        comment += "These issues must be fixed before merge:\n\n"
        for violation in CRITICAL_VIOLATIONS[:10]:
            comment += f"- {violation}\n"
        if len(CRITICAL_VIOLATIONS) > 10:
            comment += f"- ... and {len(CRITICAL_VIOLATIONS) - 10} more\n"
        comment += "\n"
    else:
        comment += "### ✅ Architecture Compliance\n\n"
        comment += "- Models: Pure data classes (no streamlit, controllers, or DB imports) ✓\n"
        comment += "- Controllers: Business logic only (no streamlit imports) ✓\n"
        comment += "- Pages: UI layer (using controllers for DB access) ✓\n"
        comment += "- Naming: Models end with 'Model', Controllers end with 'Controller' ✓\n\n"
    
    # Quality Issues
    if QUALITY_ISSUES:
        comment += "### ⚠️ Code Quality Issues\n\n"
        comment += "Consider these improvements:\n\n"
        for issue in QUALITY_ISSUES[:10]:
            comment += f"- {issue}\n"
        if len(QUALITY_ISSUES) > 10:
            comment += f"- ... and {len(QUALITY_ISSUES) - 10} more\n"
        comment += "\n"
    
    # Suggestions
    if SUGGESTIONS:
        comment += "### 💡 Optional Suggestions\n\n"
        for suggestion in SUGGESTIONS[:5]:
            comment += f"- {suggestion}\n"
        if len(SUGGESTIONS) > 5:
            comment += f"- ... and {len(SUGGESTIONS) - 5} more\n"
        comment += "\n"
    
    # Summary
    comment += "---\n\n"
    if not CRITICAL_VIOLATIONS:
        comment += "### ✨ Summary\n\n"
        comment += "✅ **This PR is ready to merge!**\n\n"
        comment += "Your code follows the Controle Financeiro architecture standards:\n"
        comment += "- Proper layer separation (Models → Controllers → Pages)\n"
        comment += "- Correct naming conventions\n"
        comment += "- Clean code practices\n\n"
    else:
        comment += "### ⛔ Summary\n\n"
        comment += f"Please fix **{len(CRITICAL_VIOLATIONS)} critical issue(s)** before merging.\n\n"
    
    comment += "*Automated review by GitHub Actions*"
    
    return comment


def post_comment_to_pr(comment: str) -> None:
    """Post review comment to PR"""
    pr_number = os.getenv("PR_NUMBER")
    repo_owner = os.getenv("REPO_OWNER")
    repo_name = os.getenv("REPO_NAME")
    token = os.getenv("GITHUB_TOKEN")
    
    if not all([pr_number, repo_owner, repo_name, token]):
        print("Warning: Cannot post comment - missing environment variables")
        return
    
    try:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
        
        import urllib.request
        import json
        
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        
        data = json.dumps({"body": comment}).encode()
        
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            if response.status == 201:
                print("✅ Comment posted successfully")
            else:
                print(f"Warning: Unexpected response status {response.status}")
    except Exception as e:
        print(f"Error posting comment: {e}")


def main() -> None:
    """Main review function"""
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
        check_naming_conventions(file_path, content)
        check_code_quality(file_path, content)
    
    print("\n" + "="*60)
    print("Review Summary:")
    print(f"  Critical Violations: {len(CRITICAL_VIOLATIONS)}")
    print(f"  Quality Issues: {len(QUALITY_ISSUES)}")
    print(f"  Suggestions: {len(SUGGESTIONS)}")
    print("="*60 + "\n")
    
    # Format and post comment
    comment = format_review_comment()
    print("Generated comment:")
    print(comment)
    print("\nPosting to PR...")
    post_comment_to_pr(comment)
    
    # Exit with error if critical violations found
    if CRITICAL_VIOLATIONS:
        print("\n❌ Review failed due to critical violations")
        exit(1)
    else:
        print("\n✅ Review passed!")
        exit(0)


if __name__ == "__main__":
    main()

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
