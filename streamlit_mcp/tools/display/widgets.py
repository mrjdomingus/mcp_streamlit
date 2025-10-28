"""Input widget tools for Streamlit MCP server."""

from typing import Any, List
from ...utils.codegen import generate_widget, format_kwargs


def add_button(
    label: str,
    key: str | None = None,
    help_text: str | None = None,
    disabled: bool = False,
    type_: str = "secondary",
) -> str:
    """Generate code for st.button()."""
    kwargs = {}
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    if disabled:
        kwargs["disabled"] = disabled
    if type_ != "secondary":
        kwargs["type"] = type_
    return generate_widget("button", label, kwargs)


def add_checkbox(
    label: str,
    value: bool = False,
    key: str | None = None,
    help_text: str | None = None,
    disabled: bool = False,
) -> str:
    """Generate code for st.checkbox()."""
    kwargs = {}
    if value:
        kwargs["value"] = value
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    if disabled:
        kwargs["disabled"] = disabled
    return generate_widget("checkbox", label, kwargs)


def add_toggle(
    label: str,
    value: bool = False,
    key: str | None = None,
    help_text: str | None = None,
    disabled: bool = False,
) -> str:
    """Generate code for st.toggle()."""
    kwargs = {}
    if value:
        kwargs["value"] = value
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    if disabled:
        kwargs["disabled"] = disabled
    return generate_widget("toggle", label, kwargs)


def add_radio(
    label: str,
    options: List[str],
    index: int = 0,
    key: str | None = None,
    help_text: str | None = None,
    horizontal: bool = False,
) -> str:
    """Generate code for st.radio()."""
    kwargs = {"options": options}
    if index != 0:
        kwargs["index"] = index
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    if horizontal:
        kwargs["horizontal"] = horizontal
    return generate_widget("radio", label, kwargs)


def add_selectbox(
    label: str,
    options: List[str],
    index: int = 0,
    key: str | None = None,
    help_text: str | None = None,
    placeholder: str | None = None,
) -> str:
    """Generate code for st.selectbox()."""
    kwargs = {"options": options}
    if index != 0:
        kwargs["index"] = index
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    if placeholder:
        kwargs["placeholder"] = placeholder
    return generate_widget("selectbox", label, kwargs)


def add_multiselect(
    label: str,
    options: List[str],
    default: List[str] | None = None,
    key: str | None = None,
    help_text: str | None = None,
    placeholder: str | None = None,
    max_selections: int | None = None,
) -> str:
    """Generate code for st.multiselect()."""
    kwargs = {"options": options}
    if default:
        kwargs["default"] = default
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    if placeholder:
        kwargs["placeholder"] = placeholder
    if max_selections:
        kwargs["max_selections"] = max_selections
    return generate_widget("multiselect", label, kwargs)


def add_slider(
    label: str,
    min_value: float = 0.0,
    max_value: float = 100.0,
    value: float | None = None,
    step: float | None = None,
    format_str: str | None = None,
    key: str | None = None,
    help_text: str | None = None,
) -> str:
    """Generate code for st.slider()."""
    kwargs = {}
    if min_value != 0.0:
        kwargs["min_value"] = min_value
    if max_value != 100.0:
        kwargs["max_value"] = max_value
    if value is not None:
        kwargs["value"] = value
    if step is not None:
        kwargs["step"] = step
    if format_str:
        kwargs["format"] = format_str
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    return generate_widget("slider", label, kwargs)


def add_select_slider(
    label: str,
    options: List[Any],
    value: Any | None = None,
    key: str | None = None,
    help_text: str | None = None,
) -> str:
    """Generate code for st.select_slider()."""
    kwargs = {"options": options}
    if value is not None:
        kwargs["value"] = value
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    return generate_widget("select_slider", label, kwargs)


def add_text_input(
    label: str,
    value: str = "",
    max_chars: int | None = None,
    key: str | None = None,
    type_: str = "default",
    help_text: str | None = None,
    placeholder: str | None = None,
) -> str:
    """Generate code for st.text_input()."""
    kwargs = {}
    if value:
        kwargs["value"] = value
    if max_chars:
        kwargs["max_chars"] = max_chars
    if key:
        kwargs["key"] = key
    if type_ != "default":
        kwargs["type"] = type_
    if help_text:
        kwargs["help"] = help_text
    if placeholder:
        kwargs["placeholder"] = placeholder
    return generate_widget("text_input", label, kwargs)


def add_text_area(
    label: str,
    value: str = "",
    height: int | None = None,
    max_chars: int | None = None,
    key: str | None = None,
    help_text: str | None = None,
    placeholder: str | None = None,
) -> str:
    """Generate code for st.text_area()."""
    kwargs = {}
    if value:
        kwargs["value"] = value
    if height:
        kwargs["height"] = height
    if max_chars:
        kwargs["max_chars"] = max_chars
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    if placeholder:
        kwargs["placeholder"] = placeholder
    return generate_widget("text_area", label, kwargs)


def add_number_input(
    label: str,
    min_value: float | None = None,
    max_value: float | None = None,
    value: float | None = None,
    step: float | None = None,
    format_str: str | None = None,
    key: str | None = None,
    help_text: str | None = None,
) -> str:
    """Generate code for st.number_input()."""
    kwargs = {}
    if min_value is not None:
        kwargs["min_value"] = min_value
    if max_value is not None:
        kwargs["max_value"] = max_value
    if value is not None:
        kwargs["value"] = value
    if step is not None:
        kwargs["step"] = step
    if format_str:
        kwargs["format"] = format_str
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    return generate_widget("number_input", label, kwargs)


def add_date_input(
    label: str,
    value: str | None = None,
    min_value: str | None = None,
    max_value: str | None = None,
    key: str | None = None,
    help_text: str | None = None,
) -> str:
    """Generate code for st.date_input()."""
    kwargs = {}
    if value:
        kwargs["value"] = f"datetime.date.fromisoformat('{value}')"
    if min_value:
        kwargs["min_value"] = f"datetime.date.fromisoformat('{min_value}')"
    if max_value:
        kwargs["max_value"] = f"datetime.date.fromisoformat('{max_value}')"
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text

    # Need to add datetime import
    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'st.date_input("{label}", {kwargs_str})'
    return f'st.date_input("{label}")'


def add_time_input(
    label: str,
    value: str | None = None,
    key: str | None = None,
    help_text: str | None = None,
    step: int | None = None,
) -> str:
    """Generate code for st.time_input()."""
    kwargs = {}
    if value:
        kwargs["value"] = f"datetime.time.fromisoformat('{value}')"
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    if step:
        kwargs["step"] = step

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'st.time_input("{label}", {kwargs_str})'
    return f'st.time_input("{label}")'


def add_file_uploader(
    label: str,
    type_: List[str] | None = None,
    accept_multiple_files: bool = False,
    key: str | None = None,
    help_text: str | None = None,
) -> str:
    """Generate code for st.file_uploader()."""
    kwargs = {}
    if type_:
        kwargs["type"] = type_
    if accept_multiple_files:
        kwargs["accept_multiple_files"] = accept_multiple_files
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    return generate_widget("file_uploader", label, kwargs)


def add_camera_input(label: str, key: str | None = None, help_text: str | None = None) -> str:
    """Generate code for st.camera_input()."""
    kwargs = {}
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    return generate_widget("camera_input", label, kwargs)


def add_color_picker(
    label: str, value: str = "#000000", key: str | None = None, help_text: str | None = None
) -> str:
    """Generate code for st.color_picker()."""
    kwargs = {}
    if value != "#000000":
        kwargs["value"] = value
    if key:
        kwargs["key"] = key
    if help_text:
        kwargs["help"] = help_text
    return generate_widget("color_picker", label, kwargs)


# Continued in next part due to length...
TOOLS = [
    {
        "name": "add_button",
        "description": "Add a button using st.button()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "Button label text"},
                "key": {"type": "string", "description": "Unique key for the widget"},
                "help": {"type": "string", "description": "Tooltip text"},
                "disabled": {"type": "boolean", "description": "Whether button is disabled"},
                "type": {
                    "type": "string",
                    "enum": ["primary", "secondary"],
                    "description": "Button type",
                },
            },
            "required": ["label"],
        },
    },
    {
        "name": "add_checkbox",
        "description": "Add a checkbox using st.checkbox()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "Checkbox label"},
                "value": {"type": "boolean", "description": "Initial checked state"},
                "key": {"type": "string", "description": "Unique key"},
                "help": {"type": "string", "description": "Tooltip text"},
                "disabled": {"type": "boolean", "description": "Whether checkbox is disabled"},
            },
            "required": ["label"],
        },
    },
    {
        "name": "add_toggle",
        "description": "Add a toggle switch using st.toggle()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "Toggle label"},
                "value": {"type": "boolean", "description": "Initial state"},
                "key": {"type": "string", "description": "Unique key"},
                "help": {"type": "string", "description": "Tooltip text"},
                "disabled": {"type": "boolean", "description": "Whether toggle is disabled"},
            },
            "required": ["label"],
        },
    },
    {
        "name": "add_radio",
        "description": "Add radio buttons using st.radio()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "Radio group label"},
                "options": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of options",
                },
                "index": {"type": "integer", "description": "Index of default selection"},
                "key": {"type": "string", "description": "Unique key"},
                "help": {"type": "string", "description": "Tooltip text"},
                "horizontal": {"type": "boolean", "description": "Display options horizontally"},
            },
            "required": ["label", "options"],
        },
    },
    {
        "name": "add_selectbox",
        "description": "Add a dropdown selectbox using st.selectbox()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "Selectbox label"},
                "options": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of options",
                },
                "index": {"type": "integer", "description": "Index of default selection"},
                "key": {"type": "string", "description": "Unique key"},
                "help": {"type": "string", "description": "Tooltip text"},
                "placeholder": {"type": "string", "description": "Placeholder text"},
            },
            "required": ["label", "options"],
        },
    },
    {
        "name": "add_multiselect",
        "description": "Add a multi-select widget using st.multiselect()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "Multiselect label"},
                "options": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of options",
                },
                "default": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Default selections",
                },
                "key": {"type": "string", "description": "Unique key"},
                "help": {"type": "string", "description": "Tooltip text"},
                "placeholder": {"type": "string", "description": "Placeholder text"},
                "max_selections": {
                    "type": "integer",
                    "description": "Maximum number of selections",
                },
            },
            "required": ["label", "options"],
        },
    },
    {
        "name": "add_slider",
        "description": "Add a slider using st.slider()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "Slider label"},
                "min_value": {"type": "number", "description": "Minimum value"},
                "max_value": {"type": "number", "description": "Maximum value"},
                "value": {"type": "number", "description": "Default value"},
                "step": {"type": "number", "description": "Step size"},
                "format": {"type": "string", "description": "Display format"},
                "key": {"type": "string", "description": "Unique key"},
                "help": {"type": "string", "description": "Tooltip text"},
            },
            "required": ["label"],
        },
    },
    {
        "name": "add_text_input",
        "description": "Add a text input using st.text_input()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "Input label"},
                "value": {"type": "string", "description": "Default value"},
                "max_chars": {"type": "integer", "description": "Maximum characters"},
                "key": {"type": "string", "description": "Unique key"},
                "type": {
                    "type": "string",
                    "enum": ["default", "password"],
                    "description": "Input type",
                },
                "help": {"type": "string", "description": "Tooltip text"},
                "placeholder": {"type": "string", "description": "Placeholder text"},
            },
            "required": ["label"],
        },
    },
    {
        "name": "add_number_input",
        "description": "Add a number input using st.number_input()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "Input label"},
                "min_value": {"type": "number", "description": "Minimum value"},
                "max_value": {"type": "number", "description": "Maximum value"},
                "value": {"type": "number", "description": "Default value"},
                "step": {"type": "number", "description": "Step size"},
                "format": {"type": "string", "description": "Display format"},
                "key": {"type": "string", "description": "Unique key"},
                "help": {"type": "string", "description": "Tooltip text"},
            },
            "required": ["label"],
        },
    },
    {
        "name": "add_file_uploader",
        "description": "Add a file uploader using st.file_uploader()",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "Uploader label"},
                "type": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Accepted file types",
                },
                "accept_multiple_files": {"type": "boolean", "description": "Allow multiple files"},
                "key": {"type": "string", "description": "Unique key"},
                "help": {"type": "string", "description": "Tooltip text"},
            },
            "required": ["label"],
        },
    },
]
