"""Pytest configuration and shared fixtures for Streamlit MCP Server tests.

This module provides:
- Path setup to ensure imports work correctly
- Shared fixtures for tests
- Common test utilities
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
