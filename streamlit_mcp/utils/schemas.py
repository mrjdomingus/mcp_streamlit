"""JSON schemas for MCP tool parameters."""

from typing import Any, Dict

# Text Elements Schemas
TEXT_ELEMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "content": {
            "type": "string",
            "description": "The text content to display"
        },
        "anchor": {
            "type": "string",
            "description": "Optional anchor for linking to this element"
        },
        "help": {
            "type": "string",
            "description": "Optional tooltip text"
        }
    },
    "required": ["content"]
}

CODE_ELEMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "code": {
            "type": "string",
            "description": "The code to display"
        },
        "language": {
            "type": "string",
            "description": "Programming language for syntax highlighting"
        },
        "line_numbers": {
            "type": "boolean",
            "description": "Whether to show line numbers"
        }
    },
    "required": ["code"]
}

# Widget Schemas
BUTTON_SCHEMA = {
    "type": "object",
    "properties": {
        "label": {
            "type": "string",
            "description": "Button label text"
        },
        "key": {
            "type": "string",
            "description": "Unique key for the widget"
        },
        "help": {
            "type": "string",
            "description": "Tooltip text"
        },
        "on_click": {
            "type": "string",
            "description": "Callback function name (as string)"
        },
        "disabled": {
            "type": "boolean",
            "description": "Whether button is disabled"
        },
        "type_": {
            "type": "string",
            "enum": ["primary", "secondary"],
            "description": "Button type/style"
        }
    },
    "required": ["label"]
}

SELECTBOX_SCHEMA = {
    "type": "object",
    "properties": {
        "label": {
            "type": "string",
            "description": "Widget label"
        },
        "options": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of options to choose from"
        },
        "index": {
            "type": "integer",
            "description": "Index of default selection"
        },
        "key": {
            "type": "string",
            "description": "Unique key for the widget"
        },
        "help": {
            "type": "string",
            "description": "Tooltip text"
        },
        "placeholder": {
            "type": "string",
            "description": "Placeholder text"
        }
    },
    "required": ["label", "options"]
}

SLIDER_SCHEMA = {
    "type": "object",
    "properties": {
        "label": {
            "type": "string",
            "description": "Widget label"
        },
        "min_value": {
            "type": "number",
            "description": "Minimum value"
        },
        "max_value": {
            "type": "number",
            "description": "Maximum value"
        },
        "value": {
            "type": "number",
            "description": "Default value"
        },
        "step": {
            "type": "number",
            "description": "Step size"
        },
        "format": {
            "type": "string",
            "description": "Display format string"
        },
        "key": {
            "type": "string",
            "description": "Unique key for the widget"
        }
    },
    "required": ["label"]
}

TEXT_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "label": {
            "type": "string",
            "description": "Widget label"
        },
        "value": {
            "type": "string",
            "description": "Default value"
        },
        "max_chars": {
            "type": "integer",
            "description": "Maximum number of characters"
        },
        "key": {
            "type": "string",
            "description": "Unique key for the widget"
        },
        "type_": {
            "type": "string",
            "enum": ["default", "password"],
            "description": "Input type"
        },
        "help": {
            "type": "string",
            "description": "Tooltip text"
        },
        "placeholder": {
            "type": "string",
            "description": "Placeholder text"
        }
    },
    "required": ["label"]
}

# Chart Schemas
CHART_SCHEMA = {
    "type": "object",
    "properties": {
        "data_variable": {
            "type": "string",
            "description": "Name of the variable containing the data (e.g., 'df', 'data')",
            "default": "data"
        },
        "x": {
            "type": "string",
            "description": "Column name for x-axis"
        },
        "y": {
            "type": ["string", "array"],
            "description": "Column name(s) for y-axis"
        },
        "color": {
            "type": "string",
            "description": "Column name for color grouping"
        },
        "size": {
            "type": "string",
            "description": "Column name for size"
        },
        "width": {
            "type": "integer",
            "description": "Chart width"
        },
        "height": {
            "type": "integer",
            "description": "Chart height"
        },
        "use_container_width": {
            "type": "boolean",
            "description": "Use full container width"
        }
    },
    "required": ["data_variable"]
}

# Layout Schemas
COLUMNS_SCHEMA = {
    "type": "object",
    "properties": {
        "spec": {
            "type": "array",
            "items": {"type": "number"},
            "description": "Column widths as array of numbers or ratios"
        },
        "gap": {
            "type": "string",
            "enum": ["small", "medium", "large"],
            "description": "Gap between columns"
        }
    },
    "required": ["spec"]
}

TABS_SCHEMA = {
    "type": "object",
    "properties": {
        "labels": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Tab labels"
        }
    },
    "required": ["labels"]
}

EXPANDER_SCHEMA = {
    "type": "object",
    "properties": {
        "label": {
            "type": "string",
            "description": "Expander label"
        },
        "expanded": {
            "type": "boolean",
            "description": "Whether initially expanded"
        }
    },
    "required": ["label"]
}

# Page Planning Schema
PAGE_PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "description": {
            "type": "string",
            "description": "Description of what the page should do/display"
        },
        "page_type": {
            "type": "string",
            "enum": ["dashboard", "data_explorer", "chat", "form", "report", "custom"],
            "description": "Type of page to create"
        },
        "features": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "data_upload", "data_filtering", "charts", "metrics",
                    "user_input", "file_download", "chat_interface",
                    "authentication", "multi_step_form", "real_time_updates"
                ]
            },
            "description": "List of features the page should include"
        },
        "data_source": {
            "type": "string",
            "enum": ["upload", "api", "database", "example", "none"],
            "description": "Where data comes from"
        },
        "layout_preference": {
            "type": "string",
            "enum": ["wide", "centered", "sidebar"],
            "description": "Preferred layout style"
        }
    },
    "required": ["description", "page_type"]
}

# Configuration Schemas
PAGE_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "page_title": {
            "type": "string",
            "description": "Browser tab title"
        },
        "page_icon": {
            "type": "string",
            "description": "Emoji or URL for favicon"
        },
        "layout": {
            "type": "string",
            "enum": ["centered", "wide"],
            "description": "Page layout"
        },
        "initial_sidebar_state": {
            "type": "string",
            "enum": ["auto", "expanded", "collapsed"],
            "description": "Initial sidebar state"
        },
        "menu_items": {
            "type": "object",
            "description": "Custom menu items"
        }
    }
}

# State Management Schemas
SESSION_STATE_SCHEMA = {
    "type": "object",
    "properties": {
        "variable_name": {
            "type": "string",
            "description": "Name of the session state variable"
        },
        "initial_value": {
            "description": "Initial value (can be any type)"
        },
        "description": {
            "type": "string",
            "description": "Description of what this state variable stores"
        }
    },
    "required": ["variable_name"]
}

CACHE_SCHEMA = {
    "type": "object",
    "properties": {
        "function_name": {
            "type": "string",
            "description": "Name of the function to cache"
        },
        "cache_type": {
            "type": "string",
            "enum": ["cache_data", "cache_resource"],
            "description": "Type of caching to use"
        },
        "ttl": {
            "type": "number",
            "description": "Time to live in seconds"
        },
        "max_entries": {
            "type": "integer",
            "description": "Maximum number of cached entries"
        }
    },
    "required": ["function_name", "cache_type"]
}

# Data Display Schemas
DATAFRAME_SCHEMA = {
    "type": "object",
    "properties": {
        "data_variable": {
            "type": "string",
            "description": "Name of the variable containing the DataFrame",
            "default": "df"
        },
        "width": {
            "type": "integer",
            "description": "Width in pixels"
        },
        "height": {
            "type": "integer",
            "description": "Height in pixels"
        },
        "use_container_width": {
            "type": "boolean",
            "description": "Use full container width"
        },
        "hide_index": {
            "type": "boolean",
            "description": "Hide the index column"
        },
        "column_order": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Order of columns to display"
        },
        "column_config": {
            "type": "object",
            "description": "Column configuration dictionary"
        }
    },
    "required": ["data_variable"]
}

METRIC_SCHEMA = {
    "type": "object",
    "properties": {
        "label": {
            "type": "string",
            "description": "Metric label"
        },
        "value": {
            "type": ["string", "number"],
            "description": "Metric value"
        },
        "delta": {
            "type": ["string", "number"],
            "description": "Change from previous value"
        },
        "delta_color": {
            "type": "string",
            "enum": ["normal", "inverse", "off"],
            "description": "How to color the delta"
        },
        "help": {
            "type": "string",
            "description": "Tooltip text"
        }
    },
    "required": ["label", "value"]
}
