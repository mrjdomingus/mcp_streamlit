"""Layout and container tools for Streamlit MCP server."""

from typing import Any, Dict, List, Optional
from ...utils.codegen import format_kwargs


def add_columns(
    num_columns: int = 2,
    gap: str = "small",
    vertical_alignment: str = "top"
) -> str:
    """Generate code for st.columns() - side-by-side layout."""
    spec = [1] * num_columns  # Equal width columns
    kwargs = {}
    if gap != "small":
        kwargs["gap"] = gap
    if vertical_alignment != "top":
        kwargs["vertical_alignment"] = vertical_alignment

    kwargs_str = format_kwargs(kwargs)

    # Generate column variable names
    col_vars = ", ".join([f"col{i+1}" for i in range(num_columns)])

    if kwargs_str:
        return f'{col_vars} = st.columns({spec}, {kwargs_str})'
    return f'{col_vars} = st.columns({spec})'


def add_tabs(tab_labels: List[str]) -> str:
    """Generate code for st.tabs() - tabbed interface."""
    labels_str = str(tab_labels)
    tab_vars = ", ".join([f"tab{i+1}" for i in range(len(tab_labels))])
    return f'{tab_vars} = st.tabs({labels_str})'


def add_expander(
    label: str,
    expanded: bool = False,
    icon: str | None = None
) -> str:
    """Generate code for st.expander() - collapsible section."""
    kwargs = {}
    if expanded:
        kwargs["expanded"] = expanded
    if icon:
        kwargs["icon"] = icon

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'with st.expander("{label}", {kwargs_str}):\n    # Add content here\n    pass'
    return f'with st.expander("{label}"):\n    # Add content here\n    pass'


def add_container(
    height: int | None = None,
    border: bool = False,
    key: str | None = None
) -> str:
    """Generate code for st.container() - grouping container."""
    kwargs = {}
    if height:
        kwargs["height"] = height
    if border:
        kwargs["border"] = border
    if key:
        kwargs["key"] = key

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'with st.container({kwargs_str}):\n    # Add content here\n    pass'
    return f'with st.container():\n    # Add content here\n    pass'


def add_sidebar() -> str:
    """Generate code for st.sidebar - sidebar container."""
    return '''with st.sidebar:
    # Add sidebar content here
    pass'''


def add_popover(
    label: str,
    help_text: str | None = None,
    disabled: bool = False,
    use_container_width: bool = False
) -> str:
    """Generate code for st.popover() - popover dialog."""
    kwargs = {}
    if help_text:
        kwargs["help"] = help_text
    if disabled:
        kwargs["disabled"] = disabled
    if use_container_width:
        kwargs["use_container_width"] = use_container_width

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'with st.popover("{label}", {kwargs_str}):\n    # Add popover content here\n    pass'
    return f'with st.popover("{label}"):\n    # Add popover content here\n    pass'


def add_dialog(
    title: str,
    width: str = "small"
) -> str:
    """Generate code for @st.dialog decorator - modal dialog."""
    return f'''@st.dialog("{title}", width="{width}")
def dialog_function():
    # Add dialog content here
    pass'''


def add_empty() -> str:
    """Generate code for st.empty() - placeholder container."""
    return '''placeholder = st.empty()
# Use placeholder.text(), placeholder.dataframe(), etc. to update content'''


def add_form(
    key: str,
    clear_on_submit: bool = False,
    enter_to_submit: bool = True,
    border: bool = True
) -> str:
    """Generate code for st.form() - form container."""
    kwargs = {"key": key}
    if clear_on_submit:
        kwargs["clear_on_submit"] = clear_on_submit
    if not enter_to_submit:
        kwargs["enter_to_submit"] = enter_to_submit
    if not border:
        kwargs["border"] = border

    kwargs_str = format_kwargs(kwargs)
    return f'''with st.form({kwargs_str}):
    # Add form fields here

    # Form must have a submit button
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success("Form submitted!")'''


# Tool definitions for MCP server
TOOLS = [
    {
        "name": "add_columns",
        "description": "Create side-by-side columns using st.columns(). Enables multi-column layouts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "num_columns": {
                    "type": "integer",
                    "description": "Number of columns to create (default: 2)",
                    "default": 2,
                    "minimum": 2,
                    "maximum": 10
                },
                "gap": {
                    "type": "string",
                    "enum": ["small", "medium", "large"],
                    "description": "Gap between columns (default: 'small')",
                    "default": "small"
                },
                "vertical_alignment": {
                    "type": "string",
                    "enum": ["top", "center", "bottom"],
                    "description": "Vertical alignment of column content (default: 'top')",
                    "default": "top"
                }
            }
        }
    },
    {
        "name": "add_tabs",
        "description": "Create a tabbed interface using st.tabs(). Organize content into tabs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tab_labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of tab labels",
                    "minItems": 2
                }
            },
            "required": ["tab_labels"]
        }
    },
    {
        "name": "add_expander",
        "description": "Create a collapsible section using st.expander(). Great for hiding detailed content.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {
                    "type": "string",
                    "description": "Label for the expander"
                },
                "expanded": {
                    "type": "boolean",
                    "description": "Whether to start expanded (default: false)",
                    "default": False
                },
                "icon": {
                    "type": "string",
                    "description": "Optional icon (emoji or icon name)"
                }
            },
            "required": ["label"]
        }
    },
    {
        "name": "add_container",
        "description": "Create a container using st.container(). Groups elements together, optionally with scrolling.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "height": {
                    "type": "integer",
                    "description": "Fixed height in pixels (enables scrolling)"
                },
                "border": {
                    "type": "boolean",
                    "description": "Show border around container (default: false)",
                    "default": False
                },
                "key": {
                    "type": "string",
                    "description": "Unique key for the container"
                }
            }
        }
    },
    {
        "name": "add_sidebar",
        "description": "Add content to the sidebar using st.sidebar. Creates a collapsible sidebar.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "add_popover",
        "description": "Create a popover dialog using st.popover(). Shows content in a floating popover.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {
                    "type": "string",
                    "description": "Button label for the popover trigger"
                },
                "help": {
                    "type": "string",
                    "description": "Optional tooltip text"
                },
                "disabled": {
                    "type": "boolean",
                    "description": "Whether the popover is disabled (default: false)",
                    "default": False
                },
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: false)",
                    "default": False
                }
            },
            "required": ["label"]
        }
    },
    {
        "name": "add_dialog",
        "description": "Create a modal dialog using @st.dialog decorator. Shows content in a centered modal.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Dialog title"
                },
                "width": {
                    "type": "string",
                    "enum": ["small", "large"],
                    "description": "Dialog width (default: 'small')",
                    "default": "small"
                }
            },
            "required": ["title"]
        }
    },
    {
        "name": "add_empty",
        "description": "Create a placeholder container using st.empty(). Can be updated dynamically.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "add_form",
        "description": "Create a form using st.form(). Batches widget interactions until submit button is clicked.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "Unique key for the form"
                },
                "clear_on_submit": {
                    "type": "boolean",
                    "description": "Clear form after submission (default: false)",
                    "default": False
                },
                "enter_to_submit": {
                    "type": "boolean",
                    "description": "Submit on Enter key (default: true)",
                    "default": True
                },
                "border": {
                    "type": "boolean",
                    "description": "Show border around form (default: true)",
                    "default": True
                }
            },
            "required": ["key"]
        }
    }
]
