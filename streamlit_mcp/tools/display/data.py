"""Data display tools for Streamlit MCP server."""

from typing import Any, Dict, List, Optional
from ...utils.codegen import generate_widget, format_kwargs


def add_dataframe(
    data_variable: str = "data",
    width: int | None = None,
    height: int | None = None,
    use_container_width: bool = True,
    hide_index: bool | None = None,
    column_order: List[str] | None = None,
    column_config: Dict[str, Any] | None = None
) -> str:
    """Generate code for st.dataframe()."""
    kwargs = {}
    if width:
        kwargs["width"] = width
    if height:
        kwargs["height"] = height
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width
    if hide_index is not None:
        kwargs["hide_index"] = hide_index
    if column_order:
        kwargs["column_order"] = column_order
    if column_config:
        kwargs["column_config"] = column_config

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'st.dataframe({data_variable}, {kwargs_str})'
    return f'st.dataframe({data_variable})'


def add_data_editor(
    data_variable: str = "data",
    width: int | None = None,
    height: int | None = None,
    use_container_width: bool = True,
    hide_index: bool | None = None,
    column_order: List[str] | None = None,
    column_config: Dict[str, Any] | None = None,
    num_rows: str = "fixed",
    disabled: bool | List[str] = False,
    key: str | None = None
) -> str:
    """Generate code for st.data_editor()."""
    kwargs = {}
    if width:
        kwargs["width"] = width
    if height:
        kwargs["height"] = height
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width
    if hide_index is not None:
        kwargs["hide_index"] = hide_index
    if column_order:
        kwargs["column_order"] = column_order
    if column_config:
        kwargs["column_config"] = column_config
    if num_rows != "fixed":
        kwargs["num_rows"] = num_rows
    if disabled:
        kwargs["disabled"] = disabled
    if key:
        kwargs["key"] = key

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'edited_data = st.data_editor({data_variable}, {kwargs_str})'
    return f'edited_data = st.data_editor({data_variable})'


def add_table(data_variable: str = "data") -> str:
    """Generate code for st.table()."""
    return f'st.table({data_variable})'


def add_metric(
    label: str,
    value: str | int | float,
    delta: str | int | float | None = None,
    delta_color: str = "normal",
    help_text: str | None = None,
    label_visibility: str = "visible"
) -> str:
    """Generate code for st.metric()."""
    kwargs = {}
    if delta is not None:
        kwargs["delta"] = delta
    if delta_color != "normal":
        kwargs["delta_color"] = delta_color
    if help_text:
        kwargs["help"] = help_text
    if label_visibility != "visible":
        kwargs["label_visibility"] = label_visibility

    # Format value appropriately
    if isinstance(value, str):
        value_str = f'"{value}"'
    else:
        value_str = str(value)

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'st.metric("{label}", {value_str}, {kwargs_str})'
    return f'st.metric("{label}", {value_str})'


def add_json(
    data_variable: str = "data",
    expanded: bool = True
) -> str:
    """Generate code for st.json()."""
    if not expanded:
        return f'st.json({data_variable}, expanded=False)'
    return f'st.json({data_variable})'


def add_column_config(
    column_name: str,
    config_type: str = "TextColumn",
    label: str | None = None,
    width: str | None = None,
    help_text: str | None = None,
    disabled: bool = False,
    required: bool = False,
    **extra_kwargs
) -> str:
    """
    Generate column configuration code for st.dataframe or st.data_editor.

    Common config_type values:
    - TextColumn, NumberColumn, CheckboxColumn, SelectboxColumn
    - LinkColumn, ImageColumn, LineChartColumn, BarChartColumn
    - ListColumn, DateColumn, TimeColumn, DatetimeColumn
    - ProgressColumn
    """
    config_parts = []

    if label:
        config_parts.append(f'label="{label}"')
    if width:
        config_parts.append(f'width="{width}"')
    if help_text:
        config_parts.append(f'help="{help_text}"')
    if disabled:
        config_parts.append(f'disabled={disabled}')
    if required:
        config_parts.append(f'required={required}')

    # Add any extra kwargs specific to the column type
    for key, value in extra_kwargs.items():
        if isinstance(value, str):
            config_parts.append(f'{key}="{value}"')
        else:
            config_parts.append(f'{key}={value}')

    config_str = ", ".join(config_parts)

    if config_str:
        return f'"{column_name}": st.column_config.{config_type}({config_str})'
    return f'"{column_name}": st.column_config.{config_type}()'


# Tool definitions for MCP server
TOOLS = [
    {
        "name": "add_dataframe",
        "description": "Display an interactive dataframe using st.dataframe(). Supports sorting, searching, and column configuration.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_variable": {
                    "type": "string",
                    "description": "Name of the DataFrame or data variable to display",
                    "default": "data"
                },
                "width": {
                    "type": "integer",
                    "description": "Width in pixels (optional)"
                },
                "height": {
                    "type": "integer",
                    "description": "Height in pixels (optional)"
                },
                "use_container_width": {
                    "type": "boolean",
                    "description": "Whether to use container width (default: true)",
                    "default": True
                },
                "hide_index": {
                    "type": "boolean",
                    "description": "Whether to hide the index column"
                },
                "column_order": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of column names in desired order"
                },
                "column_config": {
                    "type": "object",
                    "description": "Column configuration dictionary"
                }
            },
            "required": ["data_variable"]
        }
    },
    {
        "name": "add_data_editor",
        "description": "Display an editable data table using st.data_editor(). Users can edit cells, add/delete rows.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_variable": {
                    "type": "string",
                    "description": "Name of the DataFrame or data variable to edit",
                    "default": "data"
                },
                "width": {
                    "type": "integer",
                    "description": "Width in pixels (optional)"
                },
                "height": {
                    "type": "integer",
                    "description": "Height in pixels (optional)"
                },
                "use_container_width": {
                    "type": "boolean",
                    "description": "Whether to use container width (default: true)",
                    "default": True
                },
                "hide_index": {
                    "type": "boolean",
                    "description": "Whether to hide the index column"
                },
                "column_order": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of column names in desired order"
                },
                "column_config": {
                    "type": "object",
                    "description": "Column configuration dictionary"
                },
                "num_rows": {
                    "type": "string",
                    "enum": ["fixed", "dynamic"],
                    "description": "Whether users can add/delete rows (default: 'fixed')",
                    "default": "fixed"
                },
                "disabled": {
                    "type": ["boolean", "array"],
                    "description": "Disable editing (true/false or list of column names)",
                    "default": False
                },
                "key": {
                    "type": "string",
                    "description": "Unique key for the widget"
                }
            },
            "required": ["data_variable"]
        }
    },
    {
        "name": "add_table",
        "description": "Display a static table using st.table(). Unlike dataframe, this is not interactive.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_variable": {
                    "type": "string",
                    "description": "Name of the DataFrame or data variable to display",
                    "default": "data"
                }
            },
            "required": ["data_variable"]
        }
    },
    {
        "name": "add_metric",
        "description": "Display a metric card with optional delta using st.metric(). Great for KPIs and dashboards.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {
                    "type": "string",
                    "description": "The metric label"
                },
                "value": {
                    "type": ["string", "number"],
                    "description": "The metric value to display"
                },
                "delta": {
                    "type": ["string", "number"],
                    "description": "Optional change/delta to show (e.g., '+12%', -5)"
                },
                "delta_color": {
                    "type": "string",
                    "enum": ["normal", "inverse", "off"],
                    "description": "Color behavior for delta (default: 'normal')",
                    "default": "normal"
                },
                "help": {
                    "type": "string",
                    "description": "Optional tooltip text"
                },
                "label_visibility": {
                    "type": "string",
                    "enum": ["visible", "hidden", "collapsed"],
                    "description": "Label visibility (default: 'visible')",
                    "default": "visible"
                }
            },
            "required": ["label", "value"]
        }
    },
    {
        "name": "add_json",
        "description": "Display JSON data in an expandable tree view using st.json().",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_variable": {
                    "type": "string",
                    "description": "Name of the dict or JSON variable to display",
                    "default": "data"
                },
                "expanded": {
                    "type": "boolean",
                    "description": "Whether to expand all nodes by default (default: true)",
                    "default": True
                }
            },
            "required": ["data_variable"]
        }
    },
    {
        "name": "add_column_config",
        "description": "Generate column configuration for st.dataframe or st.data_editor. Supports various column types like Text, Number, Checkbox, Link, Image, etc.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "column_name": {
                    "type": "string",
                    "description": "Name of the column to configure"
                },
                "config_type": {
                    "type": "string",
                    "description": "Column type (TextColumn, NumberColumn, CheckboxColumn, SelectboxColumn, LinkColumn, ImageColumn, etc.)",
                    "default": "TextColumn"
                },
                "label": {
                    "type": "string",
                    "description": "Display label for the column"
                },
                "width": {
                    "type": "string",
                    "description": "Column width (e.g., 'small', 'medium', 'large', or pixels)"
                },
                "help": {
                    "type": "string",
                    "description": "Tooltip text for the column header"
                },
                "disabled": {
                    "type": "boolean",
                    "description": "Whether to disable editing for this column",
                    "default": False
                },
                "required": {
                    "type": "boolean",
                    "description": "Whether this column is required (for data_editor)",
                    "default": False
                }
            },
            "required": ["column_name"]
        }
    }
]
