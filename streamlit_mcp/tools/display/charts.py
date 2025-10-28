"""Chart and visualization tools for Streamlit MCP server."""

from typing import List
from ...utils.codegen import generate_chart, format_kwargs


# Simple chart functions


def add_line_chart(
    data_variable: str = "data",
    x: str | None = None,
    y: str | List[str] | None = None,
    color: str | None = None,
    width: int | None = None,
    height: int | None = None,
    use_container_width: bool = True,
) -> str:
    """Generate code for st.line_chart()."""
    kwargs = {}
    if x:
        kwargs["x"] = x
    if y:
        kwargs["y"] = y
    if color:
        kwargs["color"] = color
    if width:
        kwargs["width"] = width
    if height:
        kwargs["height"] = height
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width

    return generate_chart("line_chart", data_variable, kwargs)


def add_bar_chart(
    data_variable: str = "data",
    x: str | None = None,
    y: str | List[str] | None = None,
    color: str | None = None,
    width: int | None = None,
    height: int | None = None,
    use_container_width: bool = True,
    horizontal: bool = False,
) -> str:
    """Generate code for st.bar_chart()."""
    kwargs = {}
    if x:
        kwargs["x"] = x
    if y:
        kwargs["y"] = y
    if color:
        kwargs["color"] = color
    if width:
        kwargs["width"] = width
    if height:
        kwargs["height"] = height
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width
    if horizontal:
        kwargs["horizontal"] = horizontal

    return generate_chart("bar_chart", data_variable, kwargs)


def add_area_chart(
    data_variable: str = "data",
    x: str | None = None,
    y: str | List[str] | None = None,
    color: str | None = None,
    width: int | None = None,
    height: int | None = None,
    use_container_width: bool = True,
) -> str:
    """Generate code for st.area_chart()."""
    kwargs = {}
    if x:
        kwargs["x"] = x
    if y:
        kwargs["y"] = y
    if color:
        kwargs["color"] = color
    if width:
        kwargs["width"] = width
    if height:
        kwargs["height"] = height
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width

    return generate_chart("area_chart", data_variable, kwargs)


def add_scatter_chart(
    data_variable: str = "data",
    x: str | None = None,
    y: str | None = None,
    color: str | None = None,
    size: str | None = None,
    width: int | None = None,
    height: int | None = None,
    use_container_width: bool = True,
) -> str:
    """Generate code for st.scatter_chart()."""
    kwargs = {}
    if x:
        kwargs["x"] = x
    if y:
        kwargs["y"] = y
    if color:
        kwargs["color"] = color
    if size:
        kwargs["size"] = size
    if width:
        kwargs["width"] = width
    if height:
        kwargs["height"] = height
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width

    return generate_chart("scatter_chart", data_variable, kwargs)


def add_map(
    data_variable: str = "data",
    latitude: str | None = None,
    longitude: str | None = None,
    color: str | None = None,
    size: str | None = None,
    zoom: int | None = None,
    use_container_width: bool = True,
) -> str:
    """Generate code for st.map() - scatter map visualization."""
    kwargs = {}
    if latitude:
        kwargs["latitude"] = latitude
    if longitude:
        kwargs["longitude"] = longitude
    if color:
        kwargs["color"] = color
    if size:
        kwargs["size"] = size
    if zoom:
        kwargs["zoom"] = zoom
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width

    return generate_chart("map", data_variable, kwargs)


# Advanced chart functions


def add_plotly_chart(
    figure_variable: str = "fig",
    use_container_width: bool = True,
    theme: str | None = None,
    key: str | None = None,
) -> str:
    """Generate code for st.plotly_chart()."""
    kwargs = {}
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width
    if theme:
        kwargs["theme"] = theme
    if key:
        kwargs["key"] = key

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f"st.plotly_chart({figure_variable}, {kwargs_str})"
    return f"st.plotly_chart({figure_variable})"


def add_altair_chart(
    chart_variable: str = "chart",
    use_container_width: bool = True,
    theme: str | None = None,
    key: str | None = None,
) -> str:
    """Generate code for st.altair_chart()."""
    kwargs = {}
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width
    if theme:
        kwargs["theme"] = theme
    if key:
        kwargs["key"] = key

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f"st.altair_chart({chart_variable}, {kwargs_str})"
    return f"st.altair_chart({chart_variable})"


def add_vega_lite_chart(
    data_variable: str = "data",
    spec_variable: str | None = None,
    use_container_width: bool = True,
    theme: str | None = None,
    key: str | None = None,
) -> str:
    """Generate code for st.vega_lite_chart()."""
    kwargs = {}
    if spec_variable:
        kwargs["spec"] = spec_variable
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width
    if theme:
        kwargs["theme"] = theme
    if key:
        kwargs["key"] = key

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f"st.vega_lite_chart({data_variable}, {kwargs_str})"
    return f"st.vega_lite_chart({data_variable})"


def add_bokeh_chart(
    figure_variable: str = "fig", use_container_width: bool = True, key: str | None = None
) -> str:
    """Generate code for st.bokeh_chart()."""
    kwargs = {}
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width
    if key:
        kwargs["key"] = key

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f"st.bokeh_chart({figure_variable}, {kwargs_str})"
    return f"st.bokeh_chart({figure_variable})"


def add_pydeck_chart(
    deck_variable: str = "deck", use_container_width: bool = True, key: str | None = None
) -> str:
    """Generate code for st.pydeck_chart() - 3D map visualizations."""
    kwargs = {}
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width
    if key:
        kwargs["key"] = key

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f"st.pydeck_chart({deck_variable}, {kwargs_str})"
    return f"st.pydeck_chart({deck_variable})"


def add_graphviz_chart(
    graph_variable: str = "graph", use_container_width: bool = True, key: str | None = None
) -> str:
    """Generate code for st.graphviz_chart() - graph/network visualizations."""
    kwargs = {}
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width
    if key:
        kwargs["key"] = key

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f"st.graphviz_chart({graph_variable}, {kwargs_str})"
    return f"st.graphviz_chart({graph_variable})"


def add_pyplot(
    figure_variable: str = "fig",
    clear_figure: bool = True,
    use_container_width: bool = True,
    key: str | None = None,
) -> str:
    """Generate code for st.pyplot() - matplotlib figures."""
    kwargs = {}
    if not clear_figure:
        kwargs["clear_figure"] = clear_figure
    if not use_container_width:
        kwargs["use_container_width"] = use_container_width
    if key:
        kwargs["key"] = key

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f"st.pyplot({figure_variable}, {kwargs_str})"
    return f"st.pyplot({figure_variable})"


# Tool definitions for MCP server
TOOLS = [
    {
        "name": "add_line_chart",
        "description": "Display a line chart using st.line_chart(). Simple charts for time series and trends.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_variable": {
                    "type": "string",
                    "description": "Name of the DataFrame variable containing chart data",
                    "default": "data",
                },
                "x": {"type": "string", "description": "Column name for x-axis"},
                "y": {
                    "type": ["string", "array"],
                    "description": "Column name(s) for y-axis (single or multiple)",
                },
                "color": {"type": "string", "description": "Column name for color encoding"},
                "width": {"type": "integer", "description": "Chart width in pixels"},
                "height": {"type": "integer", "description": "Chart height in pixels"},
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: true)",
                    "default": True,
                },
            },
            "required": ["data_variable"],
        },
    },
    {
        "name": "add_bar_chart",
        "description": "Display a bar chart using st.bar_chart(). Great for comparing categories.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_variable": {
                    "type": "string",
                    "description": "Name of the DataFrame variable containing chart data",
                    "default": "data",
                },
                "x": {"type": "string", "description": "Column name for x-axis"},
                "y": {"type": ["string", "array"], "description": "Column name(s) for y-axis"},
                "color": {"type": "string", "description": "Column name for color encoding"},
                "width": {"type": "integer", "description": "Chart width in pixels"},
                "height": {"type": "integer", "description": "Chart height in pixels"},
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: true)",
                    "default": True,
                },
                "horizontal": {
                    "type": "boolean",
                    "description": "Display horizontal bars (default: false)",
                    "default": False,
                },
            },
            "required": ["data_variable"],
        },
    },
    {
        "name": "add_area_chart",
        "description": "Display an area chart using st.area_chart(). Shows cumulative trends over time.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_variable": {
                    "type": "string",
                    "description": "Name of the DataFrame variable containing chart data",
                    "default": "data",
                },
                "x": {"type": "string", "description": "Column name for x-axis"},
                "y": {"type": ["string", "array"], "description": "Column name(s) for y-axis"},
                "color": {"type": "string", "description": "Column name for color encoding"},
                "width": {"type": "integer", "description": "Chart width in pixels"},
                "height": {"type": "integer", "description": "Chart height in pixels"},
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: true)",
                    "default": True,
                },
            },
            "required": ["data_variable"],
        },
    },
    {
        "name": "add_scatter_chart",
        "description": "Display a scatter plot using st.scatter_chart(). Shows relationship between variables.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_variable": {
                    "type": "string",
                    "description": "Name of the DataFrame variable containing chart data",
                    "default": "data",
                },
                "x": {"type": "string", "description": "Column name for x-axis"},
                "y": {"type": "string", "description": "Column name for y-axis"},
                "color": {"type": "string", "description": "Column name for color encoding"},
                "size": {"type": "string", "description": "Column name for point size"},
                "width": {"type": "integer", "description": "Chart width in pixels"},
                "height": {"type": "integer", "description": "Chart height in pixels"},
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: true)",
                    "default": True,
                },
            },
            "required": ["data_variable"],
        },
    },
    {
        "name": "add_map",
        "description": "Display a scatter map using st.map(). Shows geographical data points on a map.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_variable": {
                    "type": "string",
                    "description": "Name of the DataFrame variable with lat/lon columns",
                    "default": "data",
                },
                "latitude": {
                    "type": "string",
                    "description": "Column name for latitude (default: 'latitude' or 'lat')",
                },
                "longitude": {
                    "type": "string",
                    "description": "Column name for longitude (default: 'longitude' or 'lon')",
                },
                "color": {"type": "string", "description": "Column name for color encoding"},
                "size": {"type": "string", "description": "Column name for point size"},
                "zoom": {"type": "integer", "description": "Initial zoom level"},
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: true)",
                    "default": True,
                },
            },
            "required": ["data_variable"],
        },
    },
    {
        "name": "add_plotly_chart",
        "description": "Display a Plotly chart using st.plotly_chart(). Supports interactive Plotly figures.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "figure_variable": {
                    "type": "string",
                    "description": "Name of the Plotly figure variable",
                    "default": "fig",
                },
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: true)",
                    "default": True,
                },
                "theme": {
                    "type": "string",
                    "enum": ["streamlit", "None"],
                    "description": "Theme to use (default: 'streamlit')",
                },
                "key": {"type": "string", "description": "Unique key for the widget"},
            },
            "required": ["figure_variable"],
        },
    },
    {
        "name": "add_altair_chart",
        "description": "Display an Altair chart using st.altair_chart(). Supports declarative Altair visualizations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "chart_variable": {
                    "type": "string",
                    "description": "Name of the Altair chart variable",
                    "default": "chart",
                },
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: true)",
                    "default": True,
                },
                "theme": {
                    "type": "string",
                    "enum": ["streamlit", "None"],
                    "description": "Theme to use (default: 'streamlit')",
                },
                "key": {"type": "string", "description": "Unique key for the widget"},
            },
            "required": ["chart_variable"],
        },
    },
    {
        "name": "add_vega_lite_chart",
        "description": "Display a Vega-Lite chart using st.vega_lite_chart(). Declarative grammar of graphics.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data_variable": {
                    "type": "string",
                    "description": "Name of the data variable",
                    "default": "data",
                },
                "spec_variable": {
                    "type": "string",
                    "description": "Name of the Vega-Lite spec variable (optional)",
                },
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: true)",
                    "default": True,
                },
                "theme": {
                    "type": "string",
                    "enum": ["streamlit", "None"],
                    "description": "Theme to use (default: 'streamlit')",
                },
                "key": {"type": "string", "description": "Unique key for the widget"},
            },
            "required": ["data_variable"],
        },
    },
    {
        "name": "add_bokeh_chart",
        "description": "Display a Bokeh chart using st.bokeh_chart(). Supports interactive Bokeh visualizations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "figure_variable": {
                    "type": "string",
                    "description": "Name of the Bokeh figure variable",
                    "default": "fig",
                },
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: true)",
                    "default": True,
                },
                "key": {"type": "string", "description": "Unique key for the widget"},
            },
            "required": ["figure_variable"],
        },
    },
    {
        "name": "add_pydeck_chart",
        "description": "Display a PyDeck chart using st.pydeck_chart(). 3D map visualizations with deck.gl.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "deck_variable": {
                    "type": "string",
                    "description": "Name of the PyDeck deck variable",
                    "default": "deck",
                },
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: true)",
                    "default": True,
                },
                "key": {"type": "string", "description": "Unique key for the widget"},
            },
            "required": ["deck_variable"],
        },
    },
    {
        "name": "add_graphviz_chart",
        "description": "Display a Graphviz chart using st.graphviz_chart(). Graph and network visualizations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "graph_variable": {
                    "type": "string",
                    "description": "Name of the Graphviz graph variable",
                    "default": "graph",
                },
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: true)",
                    "default": True,
                },
                "key": {"type": "string", "description": "Unique key for the widget"},
            },
            "required": ["graph_variable"],
        },
    },
    {
        "name": "add_pyplot",
        "description": "Display a Matplotlib figure using st.pyplot(). Classic Python plotting library.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "figure_variable": {
                    "type": "string",
                    "description": "Name of the Matplotlib figure variable",
                    "default": "fig",
                },
                "clear_figure": {
                    "type": "boolean",
                    "description": "Clear figure after rendering (default: true)",
                    "default": True,
                },
                "use_container_width": {
                    "type": "boolean",
                    "description": "Use container width (default: true)",
                    "default": True,
                },
                "key": {"type": "string", "description": "Unique key for the widget"},
            },
            "required": ["figure_variable"],
        },
    },
]
