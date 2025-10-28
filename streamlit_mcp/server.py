"""Main MCP server for Streamlit app building.

This server provides comprehensive tools for building Streamlit applications,
including text elements, widgets, planning tools, and documentation resources.
"""

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource

# Import tool modules
from .tools.display import text, widgets, data, charts, layout, status, media, chat
from .tools.logic import navigation, state, execution, auth, connections
from .tools import planner, resources, drawing_interpreter, app_planner, orchestrator, validator

# Server configuration
SERVER_NAME = "streamlit-mcp-server"
SERVER_VERSION = "0.1.0"

# Create server instance
app = Server(SERVER_NAME)


# Tool mappings for cleaner handler organization
TOOL_HANDLERS = {
    # Text element tools
    "add_title": text.add_title,
    "add_header": text.add_header,
    "add_subheader": text.add_subheader,
    "add_markdown": text.add_markdown,
    "add_text": text.add_text,
    "add_caption": text.add_caption,
    "add_code": text.add_code,
    "add_latex": text.add_latex,
    "add_divider": text.add_divider,
    "add_html": text.add_html,
    "add_badge": text.add_badge,
    
    # Widget tools
    "add_button": widgets.add_button,
    "add_checkbox": widgets.add_checkbox,
    "add_toggle": widgets.add_toggle,
    "add_radio": widgets.add_radio,
    "add_selectbox": widgets.add_selectbox,
    "add_multiselect": widgets.add_multiselect,
    "add_slider": widgets.add_slider,
    "add_text_input": widgets.add_text_input,
    "add_number_input": widgets.add_number_input,
    "add_file_uploader": widgets.add_file_uploader,

    # Data display tools
    "add_dataframe": data.add_dataframe,
    "add_data_editor": data.add_data_editor,
    "add_table": data.add_table,
    "add_metric": data.add_metric,
    "add_json": data.add_json,
    "add_column_config": data.add_column_config,

    # Chart tools
    "add_line_chart": charts.add_line_chart,
    "add_bar_chart": charts.add_bar_chart,
    "add_area_chart": charts.add_area_chart,
    "add_scatter_chart": charts.add_scatter_chart,
    "add_map": charts.add_map,
    "add_plotly_chart": charts.add_plotly_chart,
    "add_altair_chart": charts.add_altair_chart,
    "add_vega_lite_chart": charts.add_vega_lite_chart,
    "add_bokeh_chart": charts.add_bokeh_chart,
    "add_pydeck_chart": charts.add_pydeck_chart,
    "add_graphviz_chart": charts.add_graphviz_chart,
    "add_pyplot": charts.add_pyplot,

    # Layout tools
    "add_columns": layout.add_columns,
    "add_tabs": layout.add_tabs,
    "add_expander": layout.add_expander,
    "add_container": layout.add_container,
    "add_sidebar": layout.add_sidebar,
    "add_popover": layout.add_popover,
    "add_dialog": layout.add_dialog,
    "add_empty": layout.add_empty,
    "add_form": layout.add_form,

    # Status element tools
    "add_progress": status.add_progress,
    "add_spinner": status.add_spinner,
    "add_status": status.add_status,
    "add_toast": status.add_toast,
    "add_success": status.add_success,
    "add_error": status.add_error,
    "add_warning": status.add_warning,
    "add_info": status.add_info,
    "add_balloons": status.add_balloons,
    "add_snow": status.add_snow,

    # Media element tools
    "add_image": media.add_image,
    "add_audio": media.add_audio,
    "add_video": media.add_video,
    "add_logo": media.add_logo,
    "add_link_button": media.add_link_button,

    # Chat element tools
    "add_chat_message": chat.add_chat_message,
    "add_chat_input": chat.add_chat_input,
    "add_write_stream": chat.add_write_stream,

    # Navigation tools
    "add_navigation": navigation.add_navigation,
    "add_page_link": navigation.add_page_link,
    "switch_page": navigation.switch_page,
    "get_query_params": navigation.get_query_params,
    "set_query_params": navigation.set_query_params,

    # State management tools
    "init_session_state": state.init_session_state,
    "get_session_state": state.get_session_state,
    "set_session_state": state.set_session_state,
    "clear_session_state": state.clear_session_state,
    "manage_state_pattern": state.manage_state_pattern,

    # Execution flow tools
    "add_fragment": execution.add_fragment,
    "add_rerun": execution.add_rerun,
    "add_stop": execution.add_stop,
    "add_form_submit_button": execution.add_form_submit_button,
    "control_execution_flow": execution.control_execution_flow,

    # Authentication tools
    "add_login": auth.add_login,
    "add_logout": auth.add_logout,
    "check_user_status": auth.check_user_status,
    "generate_auth_pattern": auth.generate_auth_pattern,
    "generate_secrets_config": auth.generate_secrets_config,

    # Data connection tools
    "add_sql_connection": connections.add_sql_connection,
    "add_snowflake_connection": connections.add_snowflake_connection,
    "add_custom_connection": connections.add_custom_connection,
    "generate_connection_config": connections.generate_connection_config,
    "generate_connection_pattern": connections.generate_connection_pattern,

    # App planning tools
    "create_app_plan": app_planner.create_app_plan,
    "create_page_plan": app_planner.create_page_plan,

    # Orchestration and validation tools
    "orchestrate_app_from_drawing": orchestrator.orchestrate_app_from_drawing,
    "validate_implementation": validator.validate_implementation,

    # Resource management tools
    "get_caching_guide": resources.get_caching_guide,
    "get_architecture_guide": resources.get_architecture_guide,
    "get_code_snippets": resources.get_code_snippets,
    "search_snippets": resources.search_snippets,
    "list_templates": resources.list_templates,
    "load_template": resources.load_template,
    "suggest_cache_strategy": resources.suggest_cache_strategy,
    "get_navigation_guide": resources.get_navigation_guide,
    "get_docs_overview": resources.get_docs_overview,
    "get_api_quick_ref": resources.get_api_quick_ref,
    "search_develop_docs": resources.search_develop_docs,
}


def create_tool_handler(tool_func):
    """Create an async tool handler from a sync function."""
    async def handler(**kwargs):
        try:
            result = tool_func(**kwargs)
            if isinstance(result, dict):
                # For complex results like the planner or JSON responses
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            else:
                # For simple code generation and text responses
                return [TextContent(
                    type="text",
                    text=str(result)
                )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error executing {tool_func.__name__}: {str(e)}"
            )]
    return handler


def register_tools_from_module(tool_list: List[Tool], module_tools: List[Dict]) -> None:
    """Helper function to register tools from a module's TOOLS list."""
    for tool_def in module_tools:
        tool_list.append(Tool(
            name=tool_def["name"],
            description=tool_def["description"],
            inputSchema=tool_def["inputSchema"]
        ))


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List all available tools."""
    tools = []

    # Register text element tools
    register_tools_from_module(tools, text.TOOLS)

    # Register widget tools
    register_tools_from_module(tools, widgets.TOOLS)

    # Register data display tools
    register_tools_from_module(tools, data.TOOLS)

    # Register chart tools
    register_tools_from_module(tools, charts.TOOLS)

    # Register layout tools
    register_tools_from_module(tools, layout.TOOLS)

    # Register status element tools
    register_tools_from_module(tools, status.TOOLS)

    # Register media element tools
    register_tools_from_module(tools, media.TOOLS)

    # Register chat element tools
    register_tools_from_module(tools, chat.TOOLS)

    # Register navigation tools
    register_tools_from_module(tools, navigation.TOOLS)

    # Register state management tools
    register_tools_from_module(tools, state.TOOLS)

    # Register execution flow tools
    register_tools_from_module(tools, execution.TOOLS)

    # Register authentication tools
    register_tools_from_module(tools, auth.TOOLS)

    # Register data connection tools
    register_tools_from_module(tools, connections.TOOLS)

    # Register app planning tools
    register_tools_from_module(tools, app_planner.TOOLS)

    # Register page planner tool
    tools.append(Tool(
        name=planner.TOOL["name"],
        description=planner.TOOL["description"],
        inputSchema=planner.TOOL["inputSchema"]
    ))

    # Register drawing interpreter tool
    tools.append(Tool(
        name=drawing_interpreter.TOOL["name"],
        description=drawing_interpreter.TOOL["description"],
        inputSchema=drawing_interpreter.TOOL["inputSchema"]
    ))

    # Register orchestrator tool
    tools.append(Tool(
        name=orchestrator.TOOL["name"],
        description=orchestrator.TOOL["description"],
        inputSchema=orchestrator.TOOL["inputSchema"]
    ))

    # Register validator tool
    tools.append(Tool(
        name=validator.TOOL["name"],
        description=validator.TOOL["description"],
        inputSchema=validator.TOOL["inputSchema"]
    ))

    # Register resource management tools
    register_tools_from_module(tools, resources.TOOLS)

    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool execution."""

    # Handle page planner tool specially (returns formatted output)
    if name == "plan_streamlit_page":
        try:
            result = planner.plan_streamlit_page(**arguments)
            formatted_output = format_planner_output(result)
            return [TextContent(type="text", text=formatted_output)]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error in page planner: {str(e)}"
            )]

    # Handle drawing interpreter tool specially (returns formatted output)
    if name == "interpret_page_drawing":
        try:
            result = drawing_interpreter.interpret_page_drawing(**arguments)
            formatted_output = drawing_interpreter.format_interpretation_output(result)
            return [TextContent(type="text", text=formatted_output)]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error in drawing interpreter: {str(e)}"
            )]

    # Handle orchestrator tool specially (returns formatted output)
    if name == "orchestrate_app_from_drawing":
        try:
            result = orchestrator.orchestrate_app_from_drawing(**arguments)
            formatted_output = _format_orchestrator_output(result)
            return [TextContent(type="text", text=formatted_output)]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error in orchestrator: {str(e)}"
            )]

    # Handle validator tool specially (returns formatted output)
    if name == "validate_implementation":
        try:
            result = validator.validate_implementation(**arguments)
            formatted_output = _format_validator_output(result)
            return [TextContent(type="text", text=formatted_output)]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error in validator: {str(e)}"
            )]

    # Handle all other tools using the mapping
    if name in TOOL_HANDLERS:
        handler = create_tool_handler(TOOL_HANDLERS[name])
        try:
            return await handler(**arguments)
        except TypeError as e:
            return [TextContent(
                type="text",
                text=f"Invalid arguments for tool '{name}': {str(e)}"
            )]

    # Unknown tool
    return [TextContent(
        type="text",
        text=f"Unknown tool: {name}. Available tools: {', '.join(TOOL_HANDLERS.keys())}"
    )]


def format_planner_output(result: Dict) -> str:
    """Format the page planner output in a readable way."""
    return f"""# Streamlit Page Plan

## Layout Structure
{json.dumps(result['layout'], indent=2)}

## Recommended Components
{json.dumps(result['components'], indent=2)}

## Data Handling
{json.dumps(result['data_handling'], indent=2)}

## State Management
{json.dumps(result['state_management'], indent=2)}

## Generated Code

```python
{result['code']}
```

---

**Next Steps:**
1. Copy the generated code to a new .py file
2. Customize it based on your specific needs
3. Use the recommended components to add more features
4. Run with: `streamlit run your_app.py`
"""


def _format_orchestrator_output(result: Dict) -> str:
    """Format the orchestrator output in a readable way."""
    workflow_summary = result.get("workflow_summary", {})
    validation_results = result.get("validation_results")
    generated_code = result.get("generated_code", [])
    next_steps = result.get("next_steps", [])

    output = []

    # Header
    output.append("# 🎭 Orchestration Workflow Results")
    output.append("")
    output.append(f"**Workflow Type**: {workflow_summary.get('workflow_type', 'unknown')}")
    output.append(f"**Total Pages**: {workflow_summary.get('total_pages', 0)}")
    output.append(f"**Code Generated**: {'Yes' if workflow_summary.get('code_generated') else 'No'}")
    output.append("")

    # Workflow steps
    output.append("## 📋 Workflow Steps")
    for step in workflow_summary.get("steps_completed", []):
        output.append(f"- {step}")
    output.append("")

    # Warnings
    if workflow_summary.get("warnings"):
        output.append("## ⚠️ Warnings")
        for warning in workflow_summary["warnings"]:
            output.append(f"- {warning}")
        output.append("")

    # Validation results
    if validation_results:
        output.append("## ✅ Validation Results")
        output.append(f"**Status**: {validation_results.get('status', 'unknown')}")
        output.append(f"**Score**: {workflow_summary.get('validation_score', 'N/A')}")

        if validation_results.get("issues"):
            output.append("")
            output.append("**Issues Found**:")
            for issue in validation_results["issues"]:
                output.append(f"- ❌ {issue}")

        if validation_results.get("suggestions"):
            output.append("")
            output.append("**Suggestions**:")
            for suggestion in validation_results["suggestions"]:
                output.append(f"- 💡 {suggestion}")
        output.append("")

    # Generated code summary
    if generated_code:
        output.append("## 💻 Generated Code")
        output.append("")
        for i, page_code in enumerate(generated_code, 1):
            page_name = page_code.get("page_name", f"Page {i}")
            output.append(f"### {i}. {page_name}")
            output.append(f"**Type**: {page_code.get('page_type', 'custom')}")
            output.append(f"**Components**: {len(page_code.get('components', []))}")
            output.append("")

    # Next steps
    if next_steps:
        output.append("## 🚀 Next Steps")
        output.append("")
        for step in next_steps:
            output.append(step)

    return "\n".join(output)


def _format_validator_output(result: Dict) -> str:
    """Format the validator output in a readable way."""
    output = []

    # Header
    status = result.get("status", "unknown")
    score = result.get("score", 0)

    status_emoji = {
        "passed": "✅",
        "warnings": "⚠️",
        "failed": "❌",
        "unknown": "❓"
    }

    output.append(f"# {status_emoji.get(status, '❓')} Validation Results")
    output.append("")
    output.append(f"**Status**: {status.upper()}")
    output.append(f"**Score**: {score}/100")
    output.append("")

    # Component validation
    component_val = result.get("component_validation", {})
    if component_val:
        output.append("## 🧩 Component Validation")
        output.append(f"**Found**: {len(component_val.get('found_components', []))}")
        output.append(f"**Missing**: {len(component_val.get('missing_components', []))}")

        if component_val.get("missing_components"):
            output.append("")
            output.append("**Missing Components**:")
            for comp in component_val["missing_components"]:
                output.append(f"- {comp}")
        output.append("")

    # Best practices validation
    practices_val = result.get("best_practices_validation", {})
    if practices_val:
        output.append("## ⭐ Best Practices")
        output.append(f"**Score**: {practices_val.get('score', 0)}/100")

        violations = practices_val.get("violations", [])
        if violations:
            output.append("")
            output.append("**Violations**:")
            for violation in violations:
                severity_emoji = {"critical": "🔴", "warning": "🟡", "info": "🔵"}
                emoji = severity_emoji.get(violation.get("severity", "info"), "⚪")
                output.append(f"- {emoji} {violation.get('message', '')}")
        output.append("")

    # Plan alignment
    alignment = result.get("alignment_with_plan", {})
    if alignment and alignment.get("plan_requirements_total", 0) > 0:
        output.append("## 📋 Plan Alignment")
        met = alignment.get("plan_requirements_met", 0)
        total = alignment.get("plan_requirements_total", 0)
        output.append(f"**Requirements Met**: {met}/{total}")
        output.append("")

    # Suggestions
    suggestions = result.get("suggestions", [])
    if suggestions:
        output.append("## 💡 Suggestions")
        for suggestion in suggestions[:10]:  # Limit to 10
            output.append(f"- {suggestion}")
        output.append("")

    # Summary
    if score >= 90:
        output.append("**Summary**: Implementation looks great! 🎉")
    elif score >= 70:
        output.append("**Summary**: Good implementation with some minor issues to address.")
    else:
        output.append("**Summary**: Several issues need attention before deployment.")

    return "\n".join(output)


# Resource definitions organized by category
RESOURCE_DEFINITIONS = {
    "guides": [
        {
            "uri": "guide://caching/overview",
            "name": "Caching Deep Dive", 
            "description": "Complete guide to st.cache_data vs st.cache_resource with decision matrix",
            "mimeType": "text/markdown"
        },
        {
            "uri": "guide://caching/cache_data",
            "name": "st.cache_data Guide",
            "description": "Deep dive into @st.cache_data with examples and best practices", 
            "mimeType": "text/markdown"
        },
        {
            "uri": "guide://caching/cache_resource",
            "name": "st.cache_resource Guide",
            "description": "Deep dive into @st.cache_resource for ML models and connections",
            "mimeType": "text/markdown"
        },
        {
            "uri": "guide://architecture/execution",
            "name": "Execution Model Guide",
            "description": "How Streamlit runs: reruns, session state, fragments, and performance",
            "mimeType": "text/markdown"
        }
    ],
    "documentation": [
        {
            "uri": "docs://overview",
            "name": "Streamlit Documentation Index",
            "description": "Comprehensive index of Streamlit API reference, concepts, and tutorials",
            "mimeType": "text/markdown"
        },
        {
            "uri": "docs://quick-ref",
            "name": "Quick API Reference",
            "description": "Quick lookup for common Streamlit APIs with signatures and examples",
            "mimeType": "text/markdown"
        }
    ],
    "snippets": [
        {
            "uri": "snippets://caching",
            "name": "Caching Code Snippets",
            "description": "12 caching patterns for CSV, API, DB, ML models, and more",
            "mimeType": "application/json"
        },
        {
            "uri": "snippets://navigation", 
            "name": "Navigation Code Snippets",
            "description": "6 modern st.navigation() patterns including auth and grouped pages",
            "mimeType": "application/json"
        },
        {
            "uri": "snippets://session_state",
            "name": "Session State Code Snippets", 
            "description": "7 state management patterns for forms, chat, auth, and more",
            "mimeType": "application/json"
        },
        {
            "uri": "snippets://data_loading",
            "name": "Data Loading Code Snippets",
            "description": "9 data loading patterns for CSV, API, SQL, Parquet, and sample data",
            "mimeType": "application/json" 
        }
    ],
    "templates": [
        {
            "uri": "template://dashboard_cached",
            "name": "Dashboard Template (Cached)",
            "description": "Professional dashboard with @st.cache_data, metrics, charts, and filters",
            "mimeType": "text/x-python"
        },
        {
            "uri": "template://multipage_modern",
            "name": "Multi-Page App Template (Modern)", 
            "description": "Modern multi-page app using st.navigation() with auth and state sharing",
            "mimeType": "text/x-python"
        }
    ]
}


@app.list_resources()
async def list_resources() -> List[Resource]:
    """List available resources (templates, guides, snippets)."""
    resource_list = []
    
    # Add all resources from definitions
    for category_resources in RESOURCE_DEFINITIONS.values():
        for resource_def in category_resources:
            resource_list.append(Resource(
                uri=resource_def["uri"],
                name=resource_def["name"],
                description=resource_def["description"],
                mimeType=resource_def["mimeType"]
            ))
    
    return resource_list


# Resource URI handlers
RESOURCE_HANDLERS = {
    "docs://overview": lambda: _read_docs_overview(),
    "docs://quick-ref": lambda: _get_quick_reference_guide(),
    "guide://caching/overview": lambda: resources.get_caching_guide("overview"),
    "guide://caching/cache_data": lambda: resources.get_caching_guide("cache_data"),
    "guide://caching/cache_resource": lambda: resources.get_caching_guide("cache_resource"), 
    "guide://architecture/execution": lambda: resources.get_architecture_guide("execution"),
}


def _read_docs_overview() -> str:
    """Read the documentation overview file."""
    docs_path = Path(__file__).parent / "resources" / "docs_overview.md"
    if docs_path.exists():
        return docs_path.read_text()
    else:
        return "Documentation overview not found."


def _get_quick_reference_guide() -> str:
    """Generate a quick reference guide with common APIs."""
    common_apis = [
        "cache_data", "cache_resource", "session_state", "button", "selectbox", 
        "text_input", "dataframe", "plotly_chart", "columns", "sidebar"
    ]
    
    guide = "# Streamlit Quick API Reference\n\n"
    guide += "Quick lookup for the most commonly used Streamlit APIs.\n\n"
    
    for api in common_apis:
        try:
            api_ref = resources.get_api_quick_ref(api)
            guide += f"{api_ref}\n\n---\n\n"
        except Exception:
            guide += f"## {api}\n*Reference not available*\n\n---\n\n"
    
    guide += "**Note**: Use `get_api_quick_ref(api_name)` tool for individual API lookups.\n"
    guide += "**Search**: Use `search_develop_docs(query, mode='quick')` for broader searches."
    
    return guide


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read the content of a specific resource."""
    try:
        # Handle specific URI patterns
        if uri in RESOURCE_HANDLERS:
            return RESOURCE_HANDLERS[uri]()
            
        elif uri.startswith("snippets://"):
            # Code snippets
            snippet_type = uri.split("://")[1]
            snippets = resources.get_code_snippets(snippet_type)
            return json.dumps(snippets, indent=2)
            
        elif uri.startswith("template://"):
            # Templates
            template_name = uri.split("://")[1]
            return resources.load_template(template_name)
            
        else:
            return f"Unknown resource URI: {uri}"
            
    except Exception as e:
        return f"Error reading resource {uri}: {str(e)}"


async def main():
    """Run the MCP server with stdio communication."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def run():
    """Entry point for the server.
    
    This function is used by the console script defined in pyproject.toml.
    It starts the async event loop and runs the MCP server.
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{SERVER_NAME} shutting down gracefully...")
    except Exception as e:
        print(f"Error running {SERVER_NAME}: {e}")
        raise


if __name__ == "__main__":
    run()
