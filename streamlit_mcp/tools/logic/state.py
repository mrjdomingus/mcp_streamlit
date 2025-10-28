"""State management tools for Streamlit MCP server.

This module provides tools for managing session state:
- Initialize state variables
- Get/set state values
- Clear state
- State patterns and best practices
"""

from typing import Any, Dict, List, Optional

from ...utils.codegen import format_kwargs


def init_session_state(var_name: str, initial_value: Any = None,
                       value_type: str = "any") -> str:
    """Generate code to initialize a session state variable.

    Args:
        var_name: Variable name in session state
        initial_value: Initial value (None, string, number, list, dict)
        value_type: Type hint - 'any', 'string', 'number', 'list', 'dict', 'boolean'

    Returns:
        str: Generated Streamlit code
    """
    if initial_value is None:
        if value_type == "list":
            init_val = "[]"
        elif value_type == "dict":
            init_val = "{}"
        elif value_type == "number":
            init_val = "0"
        elif value_type == "boolean":
            init_val = "False"
        elif value_type == "string":
            init_val = '""'
        else:
            init_val = "None"
    elif isinstance(initial_value, str):
        init_val = f'"{initial_value}"'
    elif isinstance(initial_value, (list, dict)):
        init_val = str(initial_value)
    else:
        init_val = str(initial_value)

    return f'''# Initialize session state variable
if "{var_name}" not in st.session_state:
    st.session_state.{var_name} = {init_val}'''


def get_session_state(var_name: str, default_value: Any = None) -> str:
    """Generate code to get a session state variable value.

    Args:
        var_name: Variable name in session state
        default_value: Default value if variable doesn't exist

    Returns:
        str: Generated Streamlit code
    """
    if default_value is None:
        return f'''# Get session state variable
value = st.session_state.get("{var_name}", None)'''
    elif isinstance(default_value, str):
        return f'''# Get session state variable
value = st.session_state.get("{var_name}", "{default_value}")'''
    else:
        return f'''# Get session state variable
value = st.session_state.get("{var_name}", {default_value})'''


def set_session_state(var_name: str, value: Any = None) -> str:
    """Generate code to set a session state variable value.

    Args:
        var_name: Variable name in session state
        value: Value to set (if None, generates example)

    Returns:
        str: Generated Streamlit code
    """
    if value is None:
        return f'''# Set session state variable
st.session_state.{var_name} = "new_value"  # Replace with actual value'''
    elif isinstance(value, str):
        return f'''# Set session state variable
st.session_state.{var_name} = "{value}"'''
    elif isinstance(value, (list, dict)):
        return f'''# Set session state variable
st.session_state.{var_name} = {value}'''
    else:
        return f'''# Set session state variable
st.session_state.{var_name} = {value}'''


def clear_session_state(specific_keys: List[str] | None = None) -> str:
    """Generate code to clear session state variables.

    Args:
        specific_keys: Specific keys to clear (if None, clears all)

    Returns:
        str: Generated Streamlit code
    """
    if specific_keys:
        lines = ["# Clear specific session state variables"]
        for key in specific_keys:
            lines.append(f'if "{key}" in st.session_state:')
            lines.append(f'    del st.session_state.{key}')
        return "\n".join(lines)
    else:
        return '''# Clear all session state
for key in list(st.session_state.keys()):
    del st.session_state[key]

# Or to clear all at once:
# st.session_state.clear()'''


def manage_state_pattern(pattern: str = "counter") -> str:
    """Generate code for common session state patterns.

    Args:
        pattern: Pattern name - 'counter', 'toggle', 'list', 'form_data', 'chat_history'

    Returns:
        str: Generated Streamlit code with pattern implementation
    """
    if pattern == "counter":
        return '''# Counter pattern
if "count" not in st.session_state:
    st.session_state.count = 0

st.write(f"Count: {st.session_state.count}")

if st.button("Increment"):
    st.session_state.count += 1
    st.rerun()'''

    elif pattern == "toggle":
        return '''# Toggle pattern
if "show_details" not in st.session_state:
    st.session_state.show_details = False

if st.button("Toggle Details"):
    st.session_state.show_details = not st.session_state.show_details
    st.rerun()

if st.session_state.show_details:
    st.write("Here are the details...")'''

    elif pattern == "list":
        return '''# List management pattern
if "items" not in st.session_state:
    st.session_state.items = []

new_item = st.text_input("Add item")
if st.button("Add") and new_item:
    st.session_state.items.append(new_item)
    st.rerun()

for i, item in enumerate(st.session_state.items):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(item)
    with col2:
        if st.button("Remove", key=f"remove_{i}"):
            st.session_state.items.pop(i)
            st.rerun()'''

    elif pattern == "form_data":
        return '''# Form data pattern
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

with st.form("user_form"):
    name = st.text_input("Name", value=st.session_state.form_data.get("name", ""))
    email = st.text_input("Email", value=st.session_state.form_data.get("email", ""))

    if st.form_submit_button("Save"):
        st.session_state.form_data = {"name": name, "email": email}
        st.success("Form saved!")'''

    elif pattern == "chat_history":
        return '''# Chat history pattern
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Your message"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Add assistant response
    response = f"Echo: {prompt}"
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()'''

    else:
        return '''# Custom state pattern
if "custom_state" not in st.session_state:
    st.session_state.custom_state = {}

# Your custom state logic here'''


# MCP tool definitions
TOOLS = [
    {
        "name": "init_session_state",
        "description": "Initialize a session state variable (st.session_state). Use to create persistent variables across reruns. Essential for counters, toggles, user data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "var_name": {
                    "type": "string",
                    "description": "Variable name in session state (e.g., 'counter', 'user_data', 'is_logged_in')"
                },
                "initial_value": {
                    "description": "Initial value - can be string, number, list, dict, boolean, or null"
                },
                "value_type": {
                    "type": "string",
                    "description": "Type hint for the variable",
                    "enum": ["any", "string", "number", "list", "dict", "boolean"],
                    "default": "any"
                }
            },
            "required": ["var_name"]
        }
    },
    {
        "name": "get_session_state",
        "description": "Get a session state variable value (st.session_state.get). Read persistent data from session state with optional default value.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "var_name": {
                    "type": "string",
                    "description": "Variable name in session state"
                },
                "default_value": {
                    "description": "Default value if variable doesn't exist"
                }
            },
            "required": ["var_name"]
        }
    },
    {
        "name": "set_session_state",
        "description": "Set a session state variable value (st.session_state.var = value). Update persistent data in session state.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "var_name": {
                    "type": "string",
                    "description": "Variable name in session state"
                },
                "value": {
                    "description": "Value to set - can be string, number, list, dict, boolean, or null"
                }
            },
            "required": ["var_name"]
        }
    },
    {
        "name": "clear_session_state",
        "description": "Clear session state variables (del st.session_state.key). Remove specific variables or clear all state. Use for logout, reset functionality.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "specific_keys": {
                    "type": "array",
                    "description": "Specific keys to clear (if not provided, generates code to clear all)",
                    "items": {"type": "string"}
                }
            }
        }
    },
    {
        "name": "manage_state_pattern",
        "description": "Generate common session state patterns. Pre-built implementations for counter, toggle, list, form data, chat history. Use for quick state setup.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "State pattern to generate",
                    "enum": ["counter", "toggle", "list", "form_data", "chat_history"],
                    "default": "counter"
                }
            }
        }
    }
]
