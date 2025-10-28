"""Testing tools for Streamlit app testing and validation."""

import ast
import re
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional


def generate_test_for_app(app_code: str, test_focus: str = "comprehensive") -> str:
    """
    Generate pytest test code for a Streamlit app.

    Args:
        app_code: The Streamlit app code to generate tests for
        test_focus: Type of tests to generate
            - "comprehensive": Full test suite with all interactions
            - "smoke": Basic tests to verify app runs
            - "widgets": Focus on widget interactions
            - "state": Focus on session state management
            - "data": Focus on data loading and processing

    Returns:
        Generated pytest test code
    """
    # Analyze the app code
    analysis = _analyze_app_code(app_code)

    # Generate test code based on focus
    test_code_parts = []

    # Header
    test_code_parts.append(_generate_test_header())

    # Fixtures
    test_code_parts.append(_generate_test_fixtures(app_code))

    # Basic tests (always included)
    test_code_parts.append(_generate_basic_tests(analysis))

    if test_focus in ["comprehensive", "widgets"]:
        test_code_parts.append(_generate_widget_tests(analysis))

    if test_focus in ["comprehensive", "state"]:
        test_code_parts.append(_generate_state_tests(analysis))

    if test_focus in ["comprehensive", "data"]:
        test_code_parts.append(_generate_data_tests(analysis))

    return "\n\n".join(test_code_parts)


def run_app_test(test_code: str, app_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Execute pytest tests and return results.

    Args:
        test_code: The pytest test code to run
        app_code: Optional app code (if not loading from file)

    Returns:
        Dictionary with test results:
        {
            "success": bool,
            "passed": int,
            "failed": int,
            "errors": List[str],
            "output": str,
            "duration": float
        }
    """
    # Create temporary directory for test execution
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Write test file
        test_file = tmppath / "test_app.py"
        test_file.write_text(test_code)

        # Write app file if provided
        if app_code:
            app_file = tmppath / "app.py"
            app_file.write_text(app_code)

        # Run pytest
        try:
            result = subprocess.run(
                ["pytest", str(test_file), "-v", "--tb=short", "--no-header"],
                cwd=str(tmppath),
                capture_output=True,
                text=True,
                timeout=30
            )

            # Parse pytest output
            output = result.stdout + result.stderr
            passed, failed, errors = _parse_pytest_output(output)

            return {
                "success": result.returncode == 0,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "output": output,
                "exit_code": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "passed": 0,
                "failed": 0,
                "errors": ["Test execution timeout after 30 seconds"],
                "output": "Timeout",
                "exit_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "passed": 0,
                "failed": 0,
                "errors": [str(e)],
                "output": "",
                "exit_code": -1
            }


def validate_app_code(app_code: str) -> Dict[str, Any]:
    """
    Quick validation of Streamlit app code without running full tests.

    Args:
        app_code: The Streamlit app code to validate

    Returns:
        Dictionary with validation results:
        {
            "valid": bool,
            "issues": List[Dict],
            "warnings": List[str],
            "suggestions": List[str]
        }
    """
    issues = []
    warnings = []
    suggestions = []

    # Check if code is valid Python
    try:
        tree = ast.parse(app_code)
    except SyntaxError as e:
        issues.append({
            "type": "syntax_error",
            "message": str(e),
            "line": e.lineno
        })
        return {
            "valid": False,
            "issues": issues,
            "warnings": warnings,
            "suggestions": suggestions
        }

    # Analyze AST
    analysis = _analyze_app_code(app_code)

    # Check for common issues

    # 1. Missing streamlit import
    if not analysis["has_streamlit_import"]:
        issues.append({
            "type": "missing_import",
            "message": "Missing 'import streamlit as st'",
            "severity": "error"
        })

    # 2. Check for widget usage without key
    if analysis["widgets_without_keys"]:
        warnings.append(
            f"Found {len(analysis['widgets_without_keys'])} widgets without keys. "
            "Consider adding keys for better state management."
        )

    # 3. Check for caching usage
    if analysis["has_data_loading"] and not analysis["uses_caching"]:
        suggestions.append(
            "Consider using @st.cache_data or @st.cache_resource for data loading functions"
        )

    # 4. Check for session state usage
    if analysis["uses_session_state"] and not analysis["has_state_initialization"]:
        warnings.append(
            "Session state is used but may not be properly initialized. "
            "Consider checking if keys exist before accessing."
        )

    # 5. Check for form usage
    if len(analysis["widgets"]) > 3 and not analysis["uses_forms"]:
        suggestions.append(
            "App has multiple input widgets. Consider using st.form() to batch submissions."
        )

    # 6. Check for proper error handling
    if analysis["has_file_operations"] and not analysis["has_error_handling"]:
        suggestions.append(
            "Add try-except blocks for file operations to handle errors gracefully"
        )

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "suggestions": suggestions,
        "analysis": {
            "widget_count": len(analysis["widgets"]),
            "uses_caching": analysis["uses_caching"],
            "uses_session_state": analysis["uses_session_state"],
            "uses_forms": analysis["uses_forms"]
        }
    }


def suggest_test_cases(app_code: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Suggest test cases based on app functionality.

    Args:
        app_code: The Streamlit app code to analyze

    Returns:
        Dictionary of test case suggestions by category
    """
    analysis = _analyze_app_code(app_code)
    suggestions = {
        "basic": [],
        "widget_interactions": [],
        "edge_cases": [],
        "state_management": [],
        "data_validation": []
    }

    # Basic tests
    suggestions["basic"].append({
        "name": "test_app_loads",
        "description": "Verify app loads without errors",
        "priority": "high"
    })

    if analysis["has_title"]:
        suggestions["basic"].append({
            "name": "test_title_present",
            "description": "Verify title is displayed correctly",
            "priority": "medium"
        })

    # Widget interaction tests
    for widget in analysis["widgets"]:
        widget_type = widget["type"]

        if widget_type == "button":
            suggestions["widget_interactions"].append({
                "name": f"test_{widget.get('key', 'button')}_click",
                "description": f"Test button click and resulting behavior",
                "priority": "high"
            })

        elif widget_type in ["text_input", "number_input"]:
            suggestions["widget_interactions"].append({
                "name": f"test_{widget.get('key', widget_type)}_input",
                "description": f"Test {widget_type} with valid input",
                "priority": "high"
            })
            suggestions["edge_cases"].append({
                "name": f"test_{widget.get('key', widget_type)}_empty",
                "description": f"Test {widget_type} with empty input",
                "priority": "medium"
            })

        elif widget_type == "file_uploader":
            suggestions["widget_interactions"].append({
                "name": "test_file_upload",
                "description": "Test file upload with valid file",
                "priority": "high"
            })
            suggestions["edge_cases"].append({
                "name": "test_invalid_file_upload",
                "description": "Test file upload with invalid file type",
                "priority": "medium"
            })

        elif widget_type in ["selectbox", "radio"]:
            suggestions["widget_interactions"].append({
                "name": f"test_{widget.get('key', widget_type)}_selection",
                "description": f"Test selecting different options",
                "priority": "medium"
            })

    # Session state tests
    if analysis["uses_session_state"]:
        suggestions["state_management"].append({
            "name": "test_session_state_initialization",
            "description": "Verify session state is properly initialized",
            "priority": "high"
        })
        suggestions["state_management"].append({
            "name": "test_session_state_persistence",
            "description": "Verify state persists across reruns",
            "priority": "high"
        })

    # Data validation tests
    if analysis["has_data_loading"]:
        suggestions["data_validation"].append({
            "name": "test_data_loading",
            "description": "Verify data loads correctly",
            "priority": "high"
        })

        if analysis["uses_caching"]:
            suggestions["data_validation"].append({
                "name": "test_caching_behavior",
                "description": "Verify caching works correctly",
                "priority": "medium"
            })

    return suggestions


def create_test_fixture(fixture_type: str, fixture_name: str = "app") -> str:
    """
    Generate pytest fixture code for testing.

    Args:
        fixture_type: Type of fixture to create
            - "basic_app": Basic AppTest fixture
            - "app_with_state": AppTest with session state setup
            - "app_with_secrets": AppTest with secrets configuration
            - "mock_data": Mock data fixture
            - "mock_api": Mock API response fixture
        fixture_name: Name for the fixture

    Returns:
        Generated fixture code
    """
    fixtures = {
        "basic_app": f'''@pytest.fixture
def {fixture_name}():
    """Create AppTest instance."""
    at = AppTest.from_file("app.py")
    at.run()
    return at''',

        "app_with_state": f'''@pytest.fixture
def {fixture_name}():
    """Create AppTest instance with session state."""
    at = AppTest.from_file("app.py")
    # Initialize session state
    at.session_state["user_id"] = "test_user"
    at.session_state["authenticated"] = True
    at.run()
    return at''',

        "app_with_secrets": f'''@pytest.fixture
def {fixture_name}():
    """Create AppTest instance with secrets."""
    at = AppTest.from_file("app.py")
    # Set test secrets
    at.secrets["api_key"] = "test-api-key-123"
    at.secrets["db_password"] = "test-password"
    at.run()
    return at''',

        "mock_data": f'''@pytest.fixture
def {fixture_name}():
    """Create mock DataFrame for testing."""
    import pandas as pd
    return pd.DataFrame({{
        "name": ["Alice", "Bob", "Charlie"],
        "age": [30, 25, 35],
        "score": [85.5, 92.0, 78.5]
    }})''',

        "mock_api": f'''@pytest.fixture
def {fixture_name}():
    """Create mock API response."""
    from unittest.mock import MagicMock
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {{
        "status": "success",
        "data": [{{"id": 1, "value": "test"}}]
    }}
    return mock_response'''
    }

    fixture_code = fixtures.get(fixture_type)
    if not fixture_code:
        available = ", ".join(fixtures.keys())
        return f"# Unknown fixture type. Available: {available}"

    return fixture_code


# Helper functions

def _analyze_app_code(code: str) -> Dict[str, Any]:
    """Analyze Streamlit app code structure."""
    analysis = {
        "has_streamlit_import": False,
        "has_title": False,
        "widgets": [],
        "widgets_without_keys": [],
        "uses_session_state": False,
        "has_state_initialization": False,
        "uses_forms": False,
        "uses_caching": False,
        "has_data_loading": False,
        "has_file_operations": False,
        "has_error_handling": False,
        "functions": []
    }

    try:
        tree = ast.parse(code)
    except:
        return analysis

    # Check imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if 'streamlit' in alias.name:
                    analysis["has_streamlit_import"] = True

        elif isinstance(node, ast.ImportFrom):
            if node.module and 'streamlit' in node.module:
                analysis["has_streamlit_import"] = True

    # Analyze code content
    code_lower = code.lower()

    # Check for widgets
    widget_patterns = [
        (r'st\.button\([^)]*\)', 'button'),
        (r'st\.text_input\([^)]*\)', 'text_input'),
        (r'st\.number_input\([^)]*\)', 'number_input'),
        (r'st\.checkbox\([^)]*\)', 'checkbox'),
        (r'st\.radio\([^)]*\)', 'radio'),
        (r'st\.selectbox\([^)]*\)', 'selectbox'),
        (r'st\.multiselect\([^)]*\)', 'multiselect'),
        (r'st\.slider\([^)]*\)', 'slider'),
        (r'st\.file_uploader\([^)]*\)', 'file_uploader'),
    ]

    for pattern, widget_type in widget_patterns:
        matches = re.finditer(pattern, code)
        for match in matches:
            widget_code = match.group(0)
            has_key = 'key=' in widget_code
            analysis["widgets"].append({
                "type": widget_type,
                "code": widget_code,
                "has_key": has_key
            })
            if not has_key:
                analysis["widgets_without_keys"].append(widget_type)

    # Check for title
    if 'st.title(' in code:
        analysis["has_title"] = True

    # Check for session state
    if 'st.session_state' in code or 'session_state' in code_lower:
        analysis["uses_session_state"] = True

    # Check for state initialization
    if 'if ' in code and 'session_state' in code:
        analysis["has_state_initialization"] = True

    # Check for forms
    if 'st.form(' in code or 'with st.form' in code:
        analysis["uses_forms"] = True

    # Check for caching
    if '@st.cache_data' in code or '@st.cache_resource' in code:
        analysis["uses_caching"] = True

    # Check for data loading
    data_loading_keywords = ['read_csv', 'read_excel', 'read_json', 'read_sql', 'DataFrame']
    if any(keyword in code for keyword in data_loading_keywords):
        analysis["has_data_loading"] = True

    # Check for file operations
    if 'open(' in code or 'Path(' in code or 'file' in code_lower:
        analysis["has_file_operations"] = True

    # Check for error handling
    if 'try:' in code and 'except' in code:
        analysis["has_error_handling"] = True

    return analysis


def _generate_test_header() -> str:
    """Generate test file header."""
    return '''"""Tests for Streamlit app."""
import pytest
from streamlit.testing.v1 import AppTest
import pandas as pd
from pathlib import Path'''


def _generate_test_fixtures(app_code: str) -> str:
    """Generate test fixtures."""
    return '''
@pytest.fixture
def app():
    """Create AppTest instance."""
    at = AppTest.from_string("""
''' + app_code + '''
""")
    at.run()
    return at'''


def _generate_basic_tests(analysis: Dict[str, Any]) -> str:
    """Generate basic smoke tests."""
    tests = []

    tests.append('''
class TestBasicFunctionality:
    """Test basic app functionality."""

    def test_app_loads(self, app):
        """Test app loads without errors."""
        assert not app.exception''')

    if analysis["has_title"]:
        tests.append('''

    def test_title_present(self, app):
        """Test title is displayed."""
        assert len(app.title) > 0''')

    return "\n".join(tests)


def _generate_widget_tests(analysis: Dict[str, Any]) -> str:
    """Generate widget interaction tests."""
    if not analysis["widgets"]:
        return ""

    tests = ['''

class TestWidgetInteractions:
    """Test widget interactions."""''']

    widget_types_seen = set()

    for widget in analysis["widgets"]:
        widget_type = widget["type"]
        if widget_type in widget_types_seen:
            continue
        widget_types_seen.add(widget_type)

        if widget_type == "button":
            tests.append('''

    def test_button_click(self, app):
        """Test button click."""
        app.button[0].click().run()
        assert not app.exception''')

        elif widget_type == "text_input":
            tests.append('''

    def test_text_input(self, app):
        """Test text input."""
        app.text_input[0].input("test").run()
        assert not app.exception''')

        elif widget_type == "checkbox":
            tests.append('''

    def test_checkbox(self, app):
        """Test checkbox."""
        app.checkbox[0].check().run()
        assert app.checkbox[0].value''')

    return "\n".join(tests)


def _generate_state_tests(analysis: Dict[str, Any]) -> str:
    """Generate session state tests."""
    if not analysis["uses_session_state"]:
        return ""

    return '''

class TestSessionState:
    """Test session state management."""

    def test_session_state_access(self, app):
        """Test session state is accessible."""
        # Session state should be accessible
        assert hasattr(app, 'session_state')'''


def _generate_data_tests(analysis: Dict[str, Any]) -> str:
    """Generate data loading tests."""
    if not analysis["has_data_loading"]:
        return ""

    return '''

class TestDataHandling:
    """Test data loading and processing."""

    def test_data_present(self, app):
        """Test data is loaded."""
        # Verify app doesn't crash with data operations
        assert not app.exception'''


def _parse_pytest_output(output: str) -> tuple:
    """Parse pytest output to extract test results."""
    passed = 0
    failed = 0
    errors = []

    # Count passed/failed tests
    passed_match = re.search(r'(\d+) passed', output)
    if passed_match:
        passed = int(passed_match.group(1))

    failed_match = re.search(r'(\d+) failed', output)
    if failed_match:
        failed = int(failed_match.group(1))

    # Extract error messages
    error_pattern = r'FAILED.*?::(.*?) - (.*?)(?:\n|$)'
    for match in re.finditer(error_pattern, output):
        test_name = match.group(1)
        error_msg = match.group(2)
        errors.append(f"{test_name}: {error_msg}")

    return passed, failed, errors


# Tool definitions for MCP server
TOOLS = [
    {
        "name": "generate_test_for_app",
        "description": "Generate pytest test code for a Streamlit app based on its code and desired test focus",
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_code": {
                    "type": "string",
                    "description": "The Streamlit app code to generate tests for"
                },
                "test_focus": {
                    "type": "string",
                    "enum": ["comprehensive", "smoke", "widgets", "state", "data"],
                    "description": "Type of tests: comprehensive (all), smoke (basic), widgets, state, or data",
                    "default": "comprehensive"
                }
            },
            "required": ["app_code"]
        }
    },
    {
        "name": "run_app_test",
        "description": "Execute pytest tests and return results. Runs tests in isolated environment.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "test_code": {
                    "type": "string",
                    "description": "The pytest test code to execute"
                },
                "app_code": {
                    "type": "string",
                    "description": "Optional: The app code if not loading from file"
                }
            },
            "required": ["test_code"]
        }
    },
    {
        "name": "validate_app_code",
        "description": "Quick validation of Streamlit app code without running full tests. Checks syntax, imports, and common issues.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_code": {
                    "type": "string",
                    "description": "The Streamlit app code to validate"
                }
            },
            "required": ["app_code"]
        }
    },
    {
        "name": "suggest_test_cases",
        "description": "Analyze app code and suggest test cases to write based on functionality",
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_code": {
                    "type": "string",
                    "description": "The Streamlit app code to analyze"
                }
            },
            "required": ["app_code"]
        }
    },
    {
        "name": "create_test_fixture",
        "description": "Generate pytest fixture code for common testing scenarios",
        "inputSchema": {
            "type": "object",
            "properties": {
                "fixture_type": {
                    "type": "string",
                    "enum": ["basic_app", "app_with_state", "app_with_secrets", "mock_data", "mock_api"],
                    "description": "Type of fixture to create"
                },
                "fixture_name": {
                    "type": "string",
                    "description": "Name for the fixture (default: 'app')",
                    "default": "app"
                }
            },
            "required": ["fixture_type"]
        }
    }
]
