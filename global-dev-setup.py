#!/usr/bin/env python3
"""
Global-Dev-Setup - Main Entry Point
Universal Developer Environment Toolkit
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.cli.cli import main

if __name__ == '__main__':
    sys.exit(main())
