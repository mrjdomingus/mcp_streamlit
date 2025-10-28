"""Execution flow tools for Streamlit MCP server.

This module provides tools for controlling app execution:
- Fragments for partial reruns
- Rerun control
- Execution stopping
- Form submission
"""

from typing import Any, Dict, List, Optional

from ...utils.codegen import format_kwargs


def add_fragment(run_every: float | None = None) -> str:
    """Generate code for st.fragment() - partial rerun decorator.

    Args:
        run_every: Auto-rerun interval in seconds (optional)

    Returns:
        str: Generated Streamlit code with decorator
    """
    kwargs = {}
    if run_every:
        kwargs["run_every"] = run_every

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'''# Fragment decorator for partial reruns
@st.fragment({kwargs_str})
def my_fragment():
    # This function reruns independently
    st.write("Fragment content")
    if st.button("Rerun Fragment"):
        st.rerun(scope="fragment")

my_fragment()'''
    return '''# Fragment decorator for partial reruns
@st.fragment
def my_fragment():
    # This function reruns independently
    st.write("Fragment content")
    if st.button("Rerun Fragment"):
        st.rerun(scope="fragment")

my_fragment()'''


def add_rerun(scope: str = "app") -> str:
    """Generate code for st.rerun() - trigger an app rerun.

    Args:
        scope: Rerun scope - 'app' (full rerun) or 'fragment' (fragment only)

    Returns:
        str: Generated Streamlit code
    """
    if scope == "fragment":
        return '''# Rerun only the current fragment
st.rerun(scope="fragment")'''
    else:
        return '''# Rerun the entire app
st.rerun()'''


def add_stop() -> str:
    """Generate code for st.stop() - stop execution.

    Returns:
        str: Generated Streamlit code
    """
    return '''# Stop execution here
# Nothing below this will run
st.stop()'''


def add_form_submit_button(label: str = "Submit", help: str | None = None,
                           disabled: bool = False, type: str = "secondary",
                           use_container_width: bool = False,
                           on_click: str | None = None) -> str:
    """Generate code for st.form_submit_button() - form submission button.

    Args:
        label: Button text (default: "Submit")
        help: Tooltip text
        disabled: Whether button is disabled
        type: Button type - 'primary' or 'secondary'
        use_container_width: Expand to container width
        on_click: Callback function name

    Returns:
        str: Generated Streamlit code
    """
    kwargs = {}
    if help:
        kwargs["help"] = help
    if disabled:
        kwargs["disabled"] = disabled
    if type != "secondary":
        kwargs["type"] = type
    if use_container_width:
        kwargs["use_container_width"] = use_container_width
    if on_click:
        kwargs["on_click"] = on_click

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'''# Form submit button (must be inside st.form)
submitted = st.form_submit_button("{label}", {kwargs_str})
if submitted:
    st.write("Form submitted!")'''
    return f'''# Form submit button (must be inside st.form)
submitted = st.form_submit_button("{label}")
if submitted:
    st.write("Form submitted!")'''


def control_execution_flow(pattern: str = "conditional_stop") -> str:
    """Generate code for common execution flow patterns.

    Args:
        pattern: Pattern name - 'conditional_stop', 'early_return', 'progressive_render', 'form_flow'

    Returns:
        str: Generated Streamlit code with pattern
    """
    if pattern == "conditional_stop":
        return '''# Conditional stop - halt execution based on condition
if not st.session_state.get("is_authenticated", False):
    st.error("Please log in to continue")
    st.stop()

# Continue with authenticated content
st.write("Welcome! You are logged in.")'''

    elif pattern == "early_return":
        return '''# Early return pattern - stop if data not ready
uploaded_file = st.file_uploader("Upload CSV")
if not uploaded_file:
    st.info("Please upload a file to continue")
    st.stop()

# Process file
import pandas as pd
data = pd.read_csv(uploaded_file)
st.dataframe(data)'''

    elif pattern == "progressive_render":
        return '''# Progressive rendering with fragments
@st.fragment
def render_section_1():
    st.header("Section 1")
    st.write("Fast loading section")
    if st.button("Refresh Section 1"):
        st.rerun(scope="fragment")

@st.fragment(run_every=5)
def render_live_data():
    st.header("Live Data")
    import datetime
    st.write(f"Updated at: {datetime.datetime.now()}")

render_section_1()
render_live_data()

st.header("Section 2")
st.write("This doesn't rerun when fragments update")'''

    elif pattern == "form_flow":
        return '''# Multi-step form flow
if "step" not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    st.header("Step 1: Personal Info")
    with st.form("step1"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        if st.form_submit_button("Next"):
            st.session_state.name = name
            st.session_state.email = email
            st.session_state.step = 2
            st.rerun()

elif st.session_state.step == 2:
    st.header("Step 2: Preferences")
    with st.form("step2"):
        st.write(f"Name: {st.session_state.name}")
        preference = st.selectbox("Preference", ["A", "B", "C"])
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Back"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.form_submit_button("Submit"):
                st.session_state.preference = preference
                st.session_state.step = 3
                st.rerun()

else:
    st.success("Form completed!")
    st.write(f"Name: {st.session_state.name}")
    st.write(f"Email: {st.session_state.email}")
    st.write(f"Preference: {st.session_state.preference}")'''

    else:
        return '''# Custom execution flow
# Your custom logic here
pass'''


# MCP tool definitions
TOOLS = [
    {
        "name": "add_fragment",
        "description": "Add a fragment decorator (@st.fragment). Enables partial reruns for better performance. Use for sections that update independently from main app.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "run_every": {
                    "type": "number",
                    "description": "Auto-rerun interval in seconds (e.g., 5 for updates every 5 seconds)"
                }
            }
        }
    },
    {
        "name": "add_rerun",
        "description": "Add a rerun command (st.rerun). Triggers app to rerun immediately. Use after state changes, form submissions, data updates.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {
                    "type": "string",
                    "description": "Rerun scope - 'app' for full rerun, 'fragment' for current fragment only",
                    "enum": ["app", "fragment"],
                    "default": "app"
                }
            }
        }
    },
    {
        "name": "add_stop",
        "description": "Add a stop command (st.stop). Halts execution immediately. Use for conditional rendering, authentication checks, early returns.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "add_form_submit_button",
        "description": "Add a form submit button (st.form_submit_button). Must be used inside st.form. Batches widget interactions for better performance.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {
                    "type": "string",
                    "description": "Button text",
                    "default": "Submit"
                },
                "help": {
                    "type": "string",
                    "description": "Tooltip text shown on hover"
                },
                "disabled": {
                    "type": "boolean",
                    "description": "Whether button is disabled",
                    "default": False
                },
                "type": {
                    "type": "string",
                    "description": "Button visual style",
                    "enum": ["primary", "secondary"],
                    "default": "secondary"
                },
                "use_container_width": {
                    "type": "boolean",
                    "description": "Whether to expand button to container width",
                    "default": False
                },
                "on_click": {
                    "type": "string",
                    "description": "Callback function name to call when clicked"
                }
            }
        }
    },
    {
        "name": "control_execution_flow",
        "description": "Generate common execution flow patterns. Pre-built implementations for conditional stop, early return, progressive render, multi-step forms.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Execution pattern to generate",
                    "enum": ["conditional_stop", "early_return", "progressive_render", "form_flow"],
                    "default": "conditional_stop"
                }
            }
        }
    }
]
