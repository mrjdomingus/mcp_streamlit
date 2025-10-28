"""Status element tools for Streamlit MCP server.

This module provides tools for displaying status indicators and feedback elements:
- Progress bars and spinners
- Toast notifications
- Success/error/warning/info messages
- Celebration effects (balloons, snow)
"""


from ...utils.codegen import format_kwargs


def add_progress(value: float = 0.0, text: str | None = None) -> str:
    """Generate code for st.progress() - display a progress bar.

    Args:
        value: Progress value between 0.0 and 1.0 (default: 0.0)
        text: Optional text to display above the progress bar

    Returns:
        str: Generated Streamlit code
    """
    if text:
        return f'st.progress({value}, text="{text}")'
    return f"st.progress({value})"


def add_spinner(text: str = "In progress...") -> str:
    """Generate code for st.spinner() - display a spinner during execution.

    Args:
        text: Text to display next to spinner (default: "In progress...")

    Returns:
        str: Generated Streamlit code with context manager
    """
    return f"""with st.spinner("{text}"):
    # Your long-running operation here
    pass"""


def add_status(label: str = "Running...", state: str = "running", expanded: bool = False) -> str:
    """Generate code for st.status() - display an expandable status container.

    Args:
        label: Label text for the status (default: "Running...")
        state: Status state - 'running', 'complete', or 'error' (default: 'running')
        expanded: Whether to show expanded by default (default: False)

    Returns:
        str: Generated Streamlit code with context manager
    """
    kwargs = {}
    if state != "running":
        kwargs["state"] = state
    if expanded:
        kwargs["expanded"] = expanded

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f"""with st.status("{label}", {kwargs_str}):
    st.write("Operation in progress...")
    # Add status updates here"""
    return f"""with st.status("{label}"):
    st.write("Operation in progress...")
    # Add status updates here"""


def add_toast(body: str, icon: str | None = None) -> str:
    """Generate code for st.toast() - display a brief notification message.

    Args:
        body: Text content of the toast message
        icon: Optional emoji icon (e.g., "🎉", "✅", "❌")

    Returns:
        str: Generated Streamlit code
    """
    if icon:
        return f'st.toast("{body}", icon="{icon}")'
    return f'st.toast("{body}")'


def add_success(body: str, icon: str | None = None) -> str:
    """Generate code for st.success() - display a success message.

    Args:
        body: Success message text
        icon: Optional emoji icon (default: ✅)

    Returns:
        str: Generated Streamlit code
    """
    kwargs = {}
    if icon:
        kwargs["icon"] = icon

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'st.success("{body}", {kwargs_str})'
    return f'st.success("{body}")'


def add_error(body: str, icon: str | None = None) -> str:
    """Generate code for st.error() - display an error message.

    Args:
        body: Error message text
        icon: Optional emoji icon (default: 🚨)

    Returns:
        str: Generated Streamlit code
    """
    kwargs = {}
    if icon:
        kwargs["icon"] = icon

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'st.error("{body}", {kwargs_str})'
    return f'st.error("{body}")'


def add_warning(body: str, icon: str | None = None) -> str:
    """Generate code for st.warning() - display a warning message.

    Args:
        body: Warning message text
        icon: Optional emoji icon (default: ⚠️)

    Returns:
        str: Generated Streamlit code
    """
    kwargs = {}
    if icon:
        kwargs["icon"] = icon

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'st.warning("{body}", {kwargs_str})'
    return f'st.warning("{body}")'


def add_info(body: str, icon: str | None = None) -> str:
    """Generate code for st.info() - display an info message.

    Args:
        body: Info message text
        icon: Optional emoji icon (default: ℹ️)

    Returns:
        str: Generated Streamlit code
    """
    kwargs = {}
    if icon:
        kwargs["icon"] = icon

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'st.info("{body}", {kwargs_str})'
    return f'st.info("{body}")'


def add_balloons() -> str:
    """Generate code for st.balloons() - display a balloon animation.

    Returns:
        str: Generated Streamlit code
    """
    return "st.balloons()"


def add_snow() -> str:
    """Generate code for st.snow() - display a snow animation.

    Returns:
        str: Generated Streamlit code
    """
    return "st.snow()"


# MCP tool definitions
TOOLS = [
    {
        "name": "add_progress",
        "description": "Add a progress bar to show completion percentage (st.progress). Use for long-running operations to show progress from 0.0 to 1.0.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "number",
                    "description": "Progress value between 0.0 (0%) and 1.0 (100%)",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.0,
                },
                "text": {
                    "type": "string",
                    "description": "Optional text to display above the progress bar",
                },
            },
        },
    },
    {
        "name": "add_spinner",
        "description": "Add a spinner animation for loading states (st.spinner). Use as a context manager to show spinner during long-running operations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to display next to the spinner",
                    "default": "In progress...",
                }
            },
        },
    },
    {
        "name": "add_status",
        "description": "Add an expandable status container (st.status). Use to show detailed progress of multi-step operations with running/complete/error states.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {
                    "type": "string",
                    "description": "Label text for the status container",
                    "default": "Running...",
                },
                "state": {
                    "type": "string",
                    "description": "Status state: 'running' (animated), 'complete' (checkmark), or 'error' (X mark)",
                    "enum": ["running", "complete", "error"],
                    "default": "running",
                },
                "expanded": {
                    "type": "boolean",
                    "description": "Whether to show the status expanded by default",
                    "default": False,
                },
            },
        },
    },
    {
        "name": "add_toast",
        "description": "Add a brief toast notification (st.toast). Use for quick, temporary feedback messages that auto-dismiss.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body": {"type": "string", "description": "Text content of the toast message"},
                "icon": {
                    "type": "string",
                    "description": "Optional emoji icon (e.g., '🎉', '✅', '❌')",
                },
            },
            "required": ["body"],
        },
    },
    {
        "name": "add_success",
        "description": "Add a success message box (st.success). Use to display positive feedback, confirmations, and successful completions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body": {"type": "string", "description": "Success message text"},
                "icon": {"type": "string", "description": "Optional emoji icon (default: ✅)"},
            },
            "required": ["body"],
        },
    },
    {
        "name": "add_error",
        "description": "Add an error message box (st.error). Use to display error messages, failures, and critical issues.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body": {"type": "string", "description": "Error message text"},
                "icon": {"type": "string", "description": "Optional emoji icon (default: 🚨)"},
            },
            "required": ["body"],
        },
    },
    {
        "name": "add_warning",
        "description": "Add a warning message box (st.warning). Use to display warnings, cautions, and important notices.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body": {"type": "string", "description": "Warning message text"},
                "icon": {"type": "string", "description": "Optional emoji icon (default: ⚠️)"},
            },
            "required": ["body"],
        },
    },
    {
        "name": "add_info",
        "description": "Add an info message box (st.info). Use to display informational messages, tips, and helpful notes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body": {"type": "string", "description": "Info message text"},
                "icon": {"type": "string", "description": "Optional emoji icon (default: ℹ️)"},
            },
            "required": ["body"],
        },
    },
    {
        "name": "add_balloons",
        "description": "Add a balloon celebration animation (st.balloons). Use to celebrate user achievements, milestones, or successful completions.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "add_snow",
        "description": "Add a snow animation (st.snow). Use for seasonal effects or celebrations.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]
