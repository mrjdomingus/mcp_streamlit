"""Navigation tools for Streamlit MCP server.

This module provides tools for multi-page app navigation and URL parameters:
- Modern st.navigation() API
- Page links
- Page switching
- Query parameters
"""

from typing import List

from ...utils.codegen import format_kwargs


def add_navigation(pages: List[str], position: str = "sidebar") -> str:
    """Generate code for st.navigation() - modern navigation with page objects.

    Args:
        pages: List of page names or file paths
        position: Navigation position - 'sidebar' or 'hidden' (default: 'sidebar')

    Returns:
        str: Generated Streamlit code
    """
    # Generate page objects
    page_objects = []
    for i, page in enumerate(pages):
        var_name = f"page{i+1}"
        # Check if it's a file path
        if "/" in page or page.endswith(".py"):
            page_objects.append(f'{var_name} = st.Page("{page}")')
        else:
            # Assume it's a page name, create a simple page
            page_objects.append(
                f'{var_name} = st.Page("{page.lower().replace(" ", "_")}.py", title="{page}")'
            )

    page_vars = ", ".join([f"page{i+1}" for i in range(len(pages))])

    kwargs = {}
    if position != "sidebar":
        kwargs["position"] = position

    kwargs_str = format_kwargs(kwargs)
    code = "\n".join(page_objects)
    code += "\n\n"
    if kwargs_str:
        code += f"pg = st.navigation([{page_vars}], {kwargs_str})\n"
    else:
        code += f"pg = st.navigation([{page_vars}])\n"
    code += "pg.run()"

    return code


def add_page_link(
    page: str, label: str | None = None, icon: str | None = None, disabled: bool = False
) -> str:
    """Generate code for st.page_link() - create a link to another page.

    Args:
        page: Page path or name to link to
        label: Link text (default: page name)
        icon: Optional emoji icon
        disabled: Whether link is disabled (default: False)

    Returns:
        str: Generated Streamlit code
    """
    kwargs = {}
    if label:
        kwargs["label"] = label
    if icon:
        kwargs["icon"] = icon
    if disabled:
        kwargs["disabled"] = disabled

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'st.page_link("{page}", {kwargs_str})'
    return f'st.page_link("{page}")'


def switch_page(page: str) -> str:
    """Generate code for st.switch_page() - programmatically switch to another page.

    Args:
        page: Page path to switch to (e.g., "pages/settings.py")

    Returns:
        str: Generated Streamlit code
    """
    return f'st.switch_page("{page}")'


def get_query_params() -> str:
    """Generate code for st.query_params - read URL query parameters.

    Returns:
        str: Generated Streamlit code with example usage
    """
    return """# Get query parameters from URL
params = st.query_params

# Access individual parameters
# Example: ?user=john&page=2
user = params.get("user", "guest")
page_num = params.get("page", "1")

st.write(f"User: {user}, Page: {page_num}")"""


def set_query_params(**params) -> str:
    """Generate code for st.query_params update - set URL query parameters.

    Args:
        **params: Key-value pairs for query parameters

    Returns:
        str: Generated Streamlit code
    """
    if params:
        # Generate code with specific parameters
        params_str = ", ".join([f'{k}="{v}"' for k, v in params.items()])
        return f'''# Set query parameters in URL
st.query_params.update({{{params_str}}})

# Or set individual parameters:
# st.query_params["key"] = "value"'''
    else:
        # Generate generic example
        return """# Set query parameters in URL
st.query_params.update({"user": "john", "page": "2"})

# Or set individual parameters:
st.query_params["key"] = "value"

# Clear all parameters:
st.query_params.clear()"""


# MCP tool definitions
TOOLS = [
    {
        "name": "add_navigation",
        "description": "Add modern navigation (st.navigation). Creates a multi-page app with page objects. Use for apps with sidebar navigation, dynamic page routing.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pages": {
                    "type": "array",
                    "description": "List of page names or file paths (e.g., ['Home', 'Settings'] or ['pages/home.py', 'pages/settings.py'])",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
                "position": {
                    "type": "string",
                    "description": "Navigation position",
                    "enum": ["sidebar", "hidden"],
                    "default": "sidebar",
                },
            },
            "required": ["pages"],
        },
    },
    {
        "name": "add_page_link",
        "description": "Add a page link (st.page_link). Creates a clickable link to navigate between pages. Use for custom navigation, menu items, quick links.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page": {
                    "type": "string",
                    "description": "Page path to link to (e.g., 'pages/settings.py' or 'settings.py')",
                },
                "label": {
                    "type": "string",
                    "description": "Link text (default: derived from page name)",
                },
                "icon": {"type": "string", "description": "Optional emoji icon"},
                "disabled": {
                    "type": "boolean",
                    "description": "Whether the link is disabled",
                    "default": False,
                },
            },
            "required": ["page"],
        },
    },
    {
        "name": "switch_page",
        "description": "Switch to another page programmatically (st.switch_page). Use for conditional navigation, redirects after actions, automatic page routing.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page": {
                    "type": "string",
                    "description": "Page path to switch to (e.g., 'pages/settings.py')",
                }
            },
            "required": ["page"],
        },
    },
    {
        "name": "get_query_params",
        "description": "Get URL query parameters (st.query_params). Read parameters from the URL for deep linking, state sharing, tracking. Use for shareable links, page state.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "set_query_params",
        "description": "Set URL query parameters (st.query_params.update). Update the URL with parameters for deep linking, state sharing. Use for shareable app states, tracking.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "description": "Key-value pairs for query parameters (e.g., {'user': 'john', 'page': '2'})",
                    "additionalProperties": {"type": "string"},
                }
            },
        },
    },
]
