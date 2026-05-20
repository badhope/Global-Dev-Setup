#!/usr/bin/env python3
# Global-Dev-Setup - Privacy and Security Checker
# Scans repository for potential privacy leaks and sensitive information

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Whitelist of known safe dummy passwords and examples
SAFE_PASSWORD_EXAMPLES = {
    'mysecretpassword', 'secret', 'password', '123456', 'your_secure_password',
    'changeit', 'test', 'demo', 'example', 'dummy'
}

# Patterns to detect potentially sensitive information
SENSITIVE_PATTERNS = [
    # API Keys and Tokens
    (r'api[_-]?key[=:]\s*["\']?[a-zA-Z0-9_\-]{16,}["\']?', 'API Key'),
    (r'secret[_-]?key[=:]\s*["\']?[a-zA-Z0-9_\-]{16,}["\']?', 'Secret Key'),
    (r'access[_-]?token[=:]\s*["\']?[a-zA-Z0-9_\-]{16,}["\']?', 'Access Token'),
    (r'auth[_-]?token[=:]\s*["\']?[a-zA-Z0-9_\-]{16,}["\']?', 'Auth Token'),
    (r'private[_-]?key[=:]\s*["\']?[a-zA-Z0-9_\-\/\+=]{20,}["\']?', 'Private Key'),
    (r'session[_-]?token[=:]\s*["\']?[a-zA-Z0-9_\-]{16,}["\']?', 'Session Token'),
    
    # Passwords (with safe password filtering)
    (r'password[=:]\s*["\']?[^"\'\s]{4,}["\']?', 'Password'),
    (r'pass[=:]\s*["\']?[^"\'\s]{4,}["\']?', 'Password'),
    (r'passwd[=:]\s*["\']?[^"\'\s]{4,}["\']?', 'Password'),
    
    # Cloud provider credentials
    (r'AWS[_-]?ACCESS[_-]?KEY[_-]?ID[=:]\s*["\']?[A-Z0-9]{16,}["\']?', 'AWS Access Key'),
    (r'AWS[_-]?SECRET[_-]?ACCESS[_-]?KEY[=:]\s*["\']?[A-Za-z0-9/+=]{40,}["\']?', 'AWS Secret Key'),
    (r'AZURE[_-]?SUBSCRIPTION[_-]?ID[=:]\s*["\']?[a-zA-Z0-9_\-]{36}["\']?', 'Azure Subscription ID'),
    
    # Private keys
    (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----', 'Private Key'),
    (r'-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----', 'OpenSSH Private Key'),
    (r'-----BEGIN\s+PGP\s+PRIVATE\s+KEY\s+BLOCK-----', 'PGP Private Key'),
    
    # Personal information
    (r'email[=:]\s*["\']?[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}["\']?', 'Email'),
]

# Files to skip scanning (documentation files and patterns)
DOCS_FILES = ['docs/', 'README', 'TEMPLATES_GUIDE', 'RULES']

# Safe files that should never be tracked
SAFE_FILES = [
    '.git',
    '.env',
    '.env.local',
    '.env.*.local',
    '.gitconfig',
    '.git-credentials',
    '.netrc',
    '.ssh',
    '.aws',
    '.gcp',
    '.azure',
]

# File extensions to check
CHECK_EXTENSIONS = [
    '.py', '.js', '.ts', '.json', '.yaml', '.yml',
    '.sh', '.bash', '.zsh', '.ps1', '.env',
    '.txt', '.md', '.rst',
]

# Files to skip
SKIP_FILES = [
    '.gitignore',
    'node_modules',
    '__pycache__',
    '.pytest_cache',
    '.venv',
    'venv',
    'env',
    'dist',
    'build',
    'target',
    '.DS_Store',
    'Thumbs.db',
    'package-lock.json',
    'yarn.lock',
]

class PrivacyChecker:
    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir)
        self.issues: List[Dict] = []
        self.safe: List[str] = []
        
    def check_file(self, file_path):
        issues = []
        
        # Skip documentation files
        for doc_file in DOCS_FILES:
            if doc_file in str(file_path):
                return issues
                
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            for pattern, pattern_name in SENSITIVE_PATTERNS:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    match_str = match.group()
                    
                    # Filter out safe dummy passwords
                    if pattern_name == 'Password':
                        is_safe = False
                        for safe_pwd in SAFE_PASSWORD_EXAMPLES:
                            if safe_pwd in match_str.lower():
                                is_safe = True
                                break
                        if is_safe:
                            continue
                    
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append({
                        'file': str(file_path),
                        'line': line_num,
                        'type': pattern_name,
                        'match': match_str[:100] + '...' if len(match_str) > 100 else match_str,
                    })
                    
        except Exception as e:
            print(f"  {Colors.YELLOW}⚠️ Could not read {file_path}: {e}{Colors.END}")
            
        return issues
        
    def check_tree(self):
        print(f"\n{Colors.BOLD}🔍 Scanning repository for privacy issues...{Colors.END}\n")
        
        for item in self.root_dir.rglob('*'):
            if item.is_dir():
                continue
                
            # Skip .git directory entirely
            if '.git' in str(item.parts):
                continue
                
            # Skip ignored files
            skip = False
            for skip_item in SKIP_FILES:
                if skip_item in str(item):
                    skip = True
                    break
            if skip:
                continue
                
            # Check file extension
            has_extension = False
            for ext in CHECK_EXTENSIONS:
                if str(item).endswith(ext):
                    has_extension = True
                    break
                    
            # Check if filename indicates potential risk
            filename = item.name
            for safe_item in SAFE_FILES:
                if filename == safe_item or safe_item in str(item):
                    self.issues.append({
                        'file': str(item),
                        'line': 0,
                        'type': 'Potential Secret File',
                        'match': filename,
                    })
                    
            # Check content if it's a code file
            if has_extension:
                file_issues = self.check_file(item)
                self.issues.extend(file_issues)
                
    def report(self):
        print(f"\n{Colors.BOLD}📋 PRIVACY AND SECURITY REPORT{Colors.END}\n")
        
        if not self.issues:
            print(f"{Colors.GREEN}✅ No privacy or security issues found!{Colors.END}")
            return True
            
        print(f"{Colors.RED}❌ Found {len(self.issues)} potential issues:{Colors.END}\n")
        
        for i, issue in enumerate(self.issues, 1):
            print(f"{Colors.YELLOW}{i}. {issue['type']}{Colors.END}")
            print(f"   File: {issue['file']}")
            if issue['line'] > 0:
                print(f"   Line: {issue['line']}")
            print(f"   Match: {issue['match']}")
            print()
            
        print(f"{Colors.YELLOW}⚠️  Please review and remove any sensitive information!{Colors.END}")
        return False
        
    def cleanup_suggestions(self):
        print(f"\n{Colors.BOLD}🧹 SUGGESTED CLEANUP STEPS{Colors.END}\n")
        
        print("1. Remove any sensitive files and add them to .gitignore")
        print("2. Rotate any credentials that may have been exposed")
        print("3. Review git history for previous exposures")
        print("4. Notify any affected parties if necessary")
        print("5. Enable 2FA on all relevant accounts")
        print()

def main():
    print(f"\n{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}║       GLOBAL-DEV-SETUP PRIVACY & SECURITY CHECKER              ║{Colors.END}")
    print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════╝{Colors.END}")
    
    checker = PrivacyChecker()
    checker.check_tree()
    is_clean = checker.report()
    
    if not is_clean:
        checker.cleanup_suggestions()
        sys.exit(1)
    else:
        print(f"{Colors.GREEN}✅ Repository is clean! No sensitive information detected.{Colors.END}")
        sys.exit(0)

if __name__ == "__main__":
    main()
