"""Text element tools for Streamlit MCP server."""

from ...utils.codegen import generate_text_element


def add_title(content: str, anchor: str | None = None, help_text: str | None = None) -> str:
    """Generate code for st.title()."""
    kwargs = {}
    if anchor:
        kwargs["anchor"] = anchor
    if help_text:
        kwargs["help"] = help_text
    return generate_text_element("title", content, kwargs)


def add_header(
    content: str,
    anchor: str | None = None,
    help_text: str | None = None,
    divider: bool | str = False,
) -> str:
    """Generate code for st.header()."""
    kwargs = {}
    if anchor:
        kwargs["anchor"] = anchor
    if help_text:
        kwargs["help"] = help_text
    if divider:
        kwargs["divider"] = divider
    return generate_text_element("header", content, kwargs)


def add_subheader(
    content: str,
    anchor: str | None = None,
    help_text: str | None = None,
    divider: bool | str = False,
) -> str:
    """Generate code for st.subheader()."""
    kwargs = {}
    if anchor:
        kwargs["anchor"] = anchor
    if help_text:
        kwargs["help"] = help_text
    if divider:
        kwargs["divider"] = divider
    return generate_text_element("subheader", content, kwargs)


def add_markdown(
    content: str, unsafe_allow_html: bool = False, help_text: str | None = None
) -> str:
    """Generate code for st.markdown()."""
    kwargs = {}
    if unsafe_allow_html:
        kwargs["unsafe_allow_html"] = unsafe_allow_html
    if help_text:
        kwargs["help"] = help_text
    return generate_text_element("markdown", content, kwargs)


def add_text(content: str, help_text: str | None = None) -> str:
    """Generate code for st.text()."""
    kwargs = {}
    if help_text:
        kwargs["help"] = help_text
    return generate_text_element("text", content, kwargs)


def add_caption(content: str, unsafe_allow_html: bool = False, help_text: str | None = None) -> str:
    """Generate code for st.caption()."""
    kwargs = {}
    if unsafe_allow_html:
        kwargs["unsafe_allow_html"] = unsafe_allow_html
    if help_text:
        kwargs["help"] = help_text
    return generate_text_element("caption", content, kwargs)


def add_code(code: str, language: str | None = None, line_numbers: bool = False) -> str:
    """Generate code for st.code()."""
    kwargs = {}
    if language:
        kwargs["language"] = language
    if line_numbers:
        kwargs["line_numbers"] = line_numbers

    # Use repr() for safe escaping instead of manual string replacement
    if kwargs:
        kwargs_items = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        return f'st.code({repr(code)}, {", ".join(kwargs_items)})'
    return f"st.code({repr(code)})"


def add_latex(content: str, help_text: str | None = None) -> str:
    """Generate code for st.latex()."""
    kwargs = {}
    if help_text:
        kwargs["help"] = help_text
    # Use repr() for safe escaping - it handles backslashes correctly
    if kwargs:
        kwargs_items = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        return f'st.latex({repr(content)}, {", ".join(kwargs_items)})'
    return f"st.latex({repr(content)})"


def add_divider() -> str:
    """Generate code for st.divider()."""
    return "st.divider()"


def add_html(html: str, help_text: str | None = None) -> str:
    """Generate code for st.html()."""
    kwargs = {}
    if help_text:
        kwargs["help"] = help_text
    # Use repr() for safe escaping instead of manual string replacement
    if kwargs:
        kwargs_items = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        return f'st.html({repr(html)}, {", ".join(kwargs_items)})'
    return f"st.html({repr(html)})"


def add_badge(label: str, icon: str | None = None) -> str:
    """Generate code for st.badge()."""
    if icon:
        return f'st.badge("{label}", icon="{icon}")'
    return f'st.badge("{label}")'


# Tool definitions for MCP server
TOOLS = [
    {
        "name": "add_title",
        "description": "Add a title to the Streamlit app using st.title()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The title text to display"},
                "anchor": {
                    "type": "string",
                    "description": "Optional anchor for linking to this title",
                },
                "help": {"type": "string", "description": "Optional tooltip text"},
            },
            "required": ["content"],
        },
    },
    {
        "name": "add_header",
        "description": "Add a header to the Streamlit app using st.header()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The header text to display"},
                "anchor": {
                    "type": "string",
                    "description": "Optional anchor for linking to this header",
                },
                "help": {"type": "string", "description": "Optional tooltip text"},
                "divider": {
                    "type": ["boolean", "string"],
                    "description": "Show divider below header. Can be True, False, or a color name",
                },
            },
            "required": ["content"],
        },
    },
    {
        "name": "add_subheader",
        "description": "Add a subheader to the Streamlit app using st.subheader()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The subheader text to display"},
                "anchor": {"type": "string", "description": "Optional anchor"},
                "help": {"type": "string", "description": "Optional tooltip text"},
                "divider": {
                    "type": ["boolean", "string"],
                    "description": "Show divider below subheader",
                },
            },
            "required": ["content"],
        },
    },
    {
        "name": "add_markdown",
        "description": "Add markdown text using st.markdown()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The markdown content to display"},
                "unsafe_allow_html": {"type": "boolean", "description": "Allow HTML in markdown"},
                "help": {"type": "string", "description": "Optional tooltip text"},
            },
            "required": ["content"],
        },
    },
    {
        "name": "add_text",
        "description": "Add plain text using st.text()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The text to display"},
                "help": {"type": "string", "description": "Optional tooltip text"},
            },
            "required": ["content"],
        },
    },
    {
        "name": "add_caption",
        "description": "Add caption text using st.caption()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The caption text to display"},
                "unsafe_allow_html": {"type": "boolean", "description": "Allow HTML in caption"},
                "help": {"type": "string", "description": "Optional tooltip text"},
            },
            "required": ["content"],
        },
    },
    {
        "name": "add_code",
        "description": "Display code with syntax highlighting using st.code()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "The code to display"},
                "language": {
                    "type": "string",
                    "description": "Programming language for syntax highlighting (e.g., 'python', 'javascript')",
                },
                "line_numbers": {"type": "boolean", "description": "Whether to show line numbers"},
            },
            "required": ["code"],
        },
    },
    {
        "name": "add_latex",
        "description": "Display LaTeX equations using st.latex()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The LaTeX equation to display"},
                "help": {"type": "string", "description": "Optional tooltip text"},
            },
            "required": ["content"],
        },
    },
    {
        "name": "add_divider",
        "description": "Add a horizontal divider line using st.divider()",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "add_html",
        "description": "Display raw HTML using st.html()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "html": {"type": "string", "description": "The HTML content to display"},
                "help": {"type": "string", "description": "Optional tooltip text"},
            },
            "required": ["html"],
        },
    },
    {
        "name": "add_badge",
        "description": "Add a badge using st.badge()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "The badge label text"},
                "icon": {"type": "string", "description": "Optional icon emoji or name"},
            },
            "required": ["label"],
        },
    },
]
