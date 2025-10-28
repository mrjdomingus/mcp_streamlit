"""Resource management tools for accessing guides, snippets, and templates."""

import json
import os
from pathlib import Path
from typing import Dict, List, Any


# Get the base directory for resources
BASE_DIR = Path(__file__).parent.parent
RESOURCES_DIR = BASE_DIR / "resources"
TEMPLATES_DIR = BASE_DIR / "templates"


def get_caching_guide(topic: str = "overview") -> str:
    """
    Get comprehensive caching documentation.

    Args:
        topic: Which caching topic to retrieve
            - "overview": Complete caching deep dive
            - "cache_data": Guide to @st.cache_data
            - "cache_resource": Guide to @st.cache_resource

    Returns:
        Markdown content of the guide
    """
    guides = {
        "overview": RESOURCES_DIR / "guides" / "caching_deep_dive.md",
        "cache_data": RESOURCES_DIR / "guides" / "cache_data_guide.md",
        "cache_resource": RESOURCES_DIR / "guides" / "cache_resource_guide.md"
    }

    guide_path = guides.get(topic)
    if not guide_path or not guide_path.exists():
        available = ", ".join(guides.keys())
        return f"Guide not found. Available topics: {available}"

    return guide_path.read_text()


def get_docs_overview() -> str:
    """
    Get the complete Streamlit documentation index.

    Returns:
        Markdown content of the documentation overview
    """
    docs_path = RESOURCES_DIR / "docs_overview.md"
    if not docs_path.exists():
        return "Documentation overview not found."
    
    return docs_path.read_text()


def get_api_quick_ref(api_name: str) -> str:
    """
    Get quick reference for a specific Streamlit API function.

    Args:
        api_name: Name of the API function (e.g., 'cache_data', 'session_state', 'dataframe')

    Returns:
        Quick reference with signature, description, and basic usage
    """
    # Map API names to their documentation files
    api_map = {
        "cache_data": "api-reference/caching-and-state/cache-data.md",
        "cache_resource": "api-reference/caching-and-state/cache-resource.md",
        "session_state": "api-reference/caching-and-state/session_state.md",
        "dataframe": "api-reference/data/dataframe.md",
        "data_editor": "api-reference/data/data_editor.md",
        "button": "api-reference/widgets/button.md",
        "selectbox": "api-reference/widgets/selectbox.md",
        "text_input": "api-reference/widgets/text_input.md",
        "slider": "api-reference/widgets/slider.md",
        "columns": "api-reference/layout/columns.md",
        "sidebar": "api-reference/layout/sidebar.md",
        "tabs": "api-reference/layout/tabs.md",
        "plotly_chart": "api-reference/charts/plotly_chart.md",
        "bar_chart": "api-reference/charts/bar_chart.md",
        "line_chart": "api-reference/charts/line_chart.md"
    }
    
    file_path = api_map.get(api_name.lower())
    if not file_path:
        available_apis = ", ".join(sorted(api_map.keys()))
        return f"API '{api_name}' not found in quick reference. Available APIs: {available_apis}"
    
    full_path = RESOURCES_DIR / "official" / file_path
    if not full_path.exists():
        return f"Documentation file not found: {file_path}"
    
    try:
        content = full_path.read_text()
        lines = content.split('\n')
        
        # Extract key information
        title = ""
        description = ""
        signature = ""
        example = ""
        
        in_frontmatter = False
        in_code_block = False
        code_block_content = []
        
        for i, line in enumerate(lines):
            if line.strip() == "---":
                in_frontmatter = not in_frontmatter
                continue
                
            if in_frontmatter:
                if line.startswith('title:'):
                    title = line.replace('title:', '').strip()
                elif line.startswith('description:'):
                    description = line.replace('description:', '').strip()
            else:
                # Look for function signature
                if 'st.' in line and '(' in line and not signature:
                    signature = line.strip()
                
                # Capture first code example
                if line.strip().startswith('```python') and not example:
                    in_code_block = True
                    continue
                elif line.strip() == '```' and in_code_block:
                    example = '\n'.join(code_block_content)
                    break
                elif in_code_block:
                    code_block_content.append(line)
                    if len(code_block_content) > 10:  # Limit example length
                        example = '\n'.join(code_block_content)
                        break
        
        # Format quick reference
        quick_ref = f"## {title}\n\n"
        if description:
            quick_ref += f"**Description**: {description}\n\n"
        if signature:
            quick_ref += f"**Signature**: `{signature}`\n\n"
        if example:
            quick_ref += f"**Example**:\n```python\n{example}\n```\n\n"
        
        quick_ref += f"**Full documentation**: `official/{file_path}`"
        
        return quick_ref
        
    except Exception as e:
        return f"Error reading API documentation: {str(e)}"


def search_develop_docs(query: str, mode: str = "quick") -> str:
    """
    Search within the official Streamlit documentation.

    Args:
        query: Search term to look for in documentation
        mode: "quick" for brief summaries, "detailed" for full context

    Returns:
        Formatted search results with file paths and context
    """
    official_dir = RESOURCES_DIR / "official"
    if not official_dir.exists():
        return "Official documentation directory not found."
    
    results = []
    search_term = query.lower()
    
    # Search through markdown files
    for md_file in official_dir.rglob("*.md"):
        try:
            content = md_file.read_text()
            if search_term in content.lower():
                # Get relative path from official docs
                rel_path = md_file.relative_to(official_dir)
                
                if mode == "quick":
                    # Quick mode: just show file path and brief description
                    title_line = content.split('\n')[0] if content.split('\n') else ""
                    if title_line.startswith('title:'):
                        title = title_line.replace('title:', '').strip().strip('"')
                    else:
                        title = rel_path.stem.replace('-', ' ').title()
                    
                    # Get first description line
                    lines = content.split('\n')
                    description = ""
                    for line in lines:
                        if line.startswith('description:'):
                            description = line.replace('description:', '').strip()
                            break
                    
                    results.append(f"**{rel_path}**: {title}")
                    if description:
                        results.append(f"  ↳ {description}")
                    
                else:
                    # Detailed mode: show context around matches
                    lines = content.split('\n')
                    matching_lines = []
                    for i, line in enumerate(lines):
                        if search_term in line.lower():
                            # Include context around the match
                            start = max(0, i-1)
                            end = min(len(lines), i+2)
                            context = '\n'.join(lines[start:end])
                            matching_lines.append(f"Line {i+1}: {context}")
                            if len(matching_lines) >= 3:  # Limit matches per file
                                break
                    
                    if matching_lines:
                        results.append(f"**{rel_path}**:\n" + "\n\n".join(matching_lines))
                        
        except Exception as e:
            continue  # Skip files that can't be read
    
    if not results:
        return f"No matches found for '{query}' in official Streamlit documentation."
    
    if mode == "quick":
        # Show more results in quick mode since they're shorter
        result_count = min(10, len(results))
        result_text = f"Found {len(results)} files matching '{query}' (showing {result_count}):\n\n"
        return result_text + "\n".join(results[:result_count])
    else:
        # Show fewer but more detailed results
        result_count = min(5, len(results))
        result_text = f"Found {len(results)} files matching '{query}' (showing {result_count} with details):\n\n"
        return result_text + "\n\n---\n\n".join(results[:result_count])


def get_architecture_guide(topic: str = "execution") -> str:
    """
    Get architecture and execution model documentation.

    Args:
        topic: Which architecture topic to retrieve
            - "execution": Execution model and reruns

    Returns:
        Markdown content of the guide
    """
    guides = {
        "execution": RESOURCES_DIR / "guides" / "execution_model.md"
    }

    guide_path = guides.get(topic)
    if not guide_path or not guide_path.exists():
        available = ", ".join(guides.keys())
        return f"Guide not found. Available topics: {available}"

    return guide_path.read_text()


def get_code_snippets(category: str = "all") -> Dict[str, Any]:
    """
    Get code snippets by category.

    Args:
        category: Which snippet category to retrieve
            - "all": All snippets
            - "caching": Caching patterns
            - "navigation": Navigation patterns
            - "session_state": State management patterns
            - "data_loading": Data loading patterns

    Returns:
        Dictionary of code snippets
    """
    snippet_files = {
        "caching": RESOURCES_DIR / "snippets" / "caching_snippets.json",
        "navigation": RESOURCES_DIR / "snippets" / "navigation_snippets.json",
        "session_state": RESOURCES_DIR / "snippets" / "session_state_snippets.json",
        "data_loading": RESOURCES_DIR / "snippets" / "data_loading_snippets.json"
    }

    if category == "all":
        all_snippets = {}
        for cat, file_path in snippet_files.items():
            if file_path.exists():
                all_snippets[cat] = json.loads(file_path.read_text())
        return all_snippets

    file_path = snippet_files.get(category)
    if not file_path or not file_path.exists():
        available = ", ".join(snippet_files.keys())
        return {"error": f"Category not found. Available: {available}"}

    return json.loads(file_path.read_text())


def search_snippets(query: str) -> Dict[str, Any]:
    """
    Search for code snippets matching a query.

    Args:
        query: Search term to find in snippet descriptions or code

    Returns:
        Dictionary of matching snippets
    """
    all_snippets = get_code_snippets("all")
    results = {}

    query_lower = query.lower()

    for category, snippets in all_snippets.items():
        if isinstance(snippets, dict):
            for name, snippet in snippets.items():
                if isinstance(snippet, dict):
                    # Search in description, code, and use_case
                    searchable = (
                        snippet.get("description", "").lower() +
                        snippet.get("code", "").lower() +
                        snippet.get("use_case", "").lower()
                    )
                    if query_lower in searchable:
                        if category not in results:
                            results[category] = {}
                        results[category][name] = snippet

    return results


def list_templates() -> Dict[str, Any]:
    """
    List all available templates.

    Returns:
        Dictionary of templates with metadata
    """
    templates = {
        "dashboard_cached": {
            "file": "dashboard_cached.py",
            "path": TEMPLATES_DIR / "dashboard_cached.py",
            "type": "single_page",
            "description": "Professional dashboard with caching best practices, metrics, and charts",
            "features": ["@st.cache_data", "TTL", "Plotly charts", "Filters", "Download"],
            "difficulty": "intermediate",
            "lines": 300
        },
        "multipage_modern": {
            "file": "multipage_modern/",
            "path": TEMPLATES_DIR / "multipage_modern",
            "type": "multi_page",
            "description": "Modern multi-page app using st.navigation() with auth",
            "features": ["st.navigation()", "Authentication", "State sharing", "Grouped pages"],
            "difficulty": "intermediate",
            "files": ["app.py", "pages_lib/home.py", "pages_lib/data_analysis.py",
                     "pages_lib/visualizations.py", "pages_lib/settings.py"]
        }
    }

    # Add existence check
    for name, template in templates.items():
        template["exists"] = template["path"].exists()

    return templates


def load_template(template_name: str) -> str:
    """
    Load a template's code.

    Args:
        template_name: Name of the template to load
            - "dashboard_cached": Dashboard template
            - "multipage_modern": Multi-page app template

    Returns:
        Template code or file structure information
    """
    templates = list_templates()

    if template_name not in templates:
        available = ", ".join(templates.keys())
        return f"Template not found. Available: {available}"

    template = templates[template_name]
    path = template["path"]

    # Security: Validate that resolved path stays within TEMPLATES_DIR
    # This prevents path traversal attacks
    try:
        resolved_path = path.resolve()
        resolved_templates_dir = TEMPLATES_DIR.resolve()
        resolved_path.relative_to(resolved_templates_dir)
    except ValueError:
        return f"Security error: Invalid template path for '{template_name}'"

    if not path.exists():
        return f"Template file not found at {path}"

    if template["type"] == "single_page":
        # Return the file content
        return path.read_text()
    else:
        # For multi-page, return structure and main file
        result = f"# {template_name} Template\n\n"
        result += f"{template['description']}\n\n"
        result += "## Structure:\n"
        for file in template.get("files", []):
            result += f"- {file}\n"
        result += "\n## Main File (app.py):\n\n"
        main_file = path / "app.py"

        # Security: Validate main_file path as well
        try:
            resolved_main = main_file.resolve()
            resolved_main.relative_to(resolved_templates_dir)
        except ValueError:
            return "Security error: Invalid main file path"

        if main_file.exists():
            result += main_file.read_text()
        return result


def suggest_cache_strategy(use_case: str) -> Dict[str, Any]:
    """
    Suggest optimal caching strategy based on use case.

    Args:
        use_case: Description of what needs to be cached

    Returns:
        Dictionary with recommendation and code example
    """
    use_case_lower = use_case.lower()

    # Keywords for cache_data
    data_keywords = ["csv", "excel", "api", "query", "dataframe", "json", "transform", "filter"]
    # Keywords for cache_resource
    resource_keywords = ["model", "connection", "database", "ml", "tokenizer", "engine"]

    data_score = sum(1 for kw in data_keywords if kw in use_case_lower)
    resource_score = sum(1 for kw in resource_keywords if kw in use_case_lower)

    if resource_score > data_score:
        decorator = "cache_resource"
        reason = "This appears to be an unserializable resource (model, connection, etc.)"
        example = """@st.cache_resource
def load_resource():
    # Load your model, connection, or resource
    return resource"""
    else:
        decorator = "cache_data"
        reason = "This appears to be serializable data (DataFrame, API response, etc.)"
        example = """@st.cache_data
def load_data():
    # Load your data
    return data"""

    # Additional recommendations
    recommendations = []

    if any(kw in use_case_lower for kw in ["api", "live", "real-time", "fresh"]):
        recommendations.append("Consider adding TTL: @st.cache_data(ttl=3600) for hourly refresh")

    if any(kw in use_case_lower for kw in ["user", "query", "search", "filter"]):
        recommendations.append("Consider adding max_entries: @st.cache_data(max_entries=1000)")

    if any(kw in use_case_lower for kw in ["slow", "expensive", "loading"]):
        recommendations.append("Consider custom spinner: show_spinner='Loading data...'")

    return {
        "recommended_decorator": f"@st.{decorator}",
        "reason": reason,
        "example": example,
        "additional_recommendations": recommendations,
        "learn_more": f"Use get_caching_guide('{decorator.replace('cache_', '')}') for details"
    }


def get_navigation_guide() -> str:
    """
    Get guide on modern navigation patterns.

    Returns:
        Navigation guide content
    """
    template_readme = TEMPLATES_DIR / "multipage_modern" / "README.md"
    if template_readme.exists():
        return template_readme.read_text()
    return "Navigation guide not found"


# Tool definitions for MCP server
TOOLS = [
    {
        "name": "get_caching_guide",
        "description": "Get comprehensive caching documentation (cache_data vs cache_resource, parameters, best practices)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "enum": ["overview", "cache_data", "cache_resource"],
                    "description": "Which caching topic: overview (complete guide), cache_data, or cache_resource",
                    "default": "overview"
                }
            }
        }
    },
    {
        "name": "get_architecture_guide",
        "description": "Get Streamlit architecture and execution model documentation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "enum": ["execution"],
                    "description": "Which architecture topic",
                    "default": "execution"
                }
            }
        }
    },
    {
        "name": "get_code_snippets",
        "description": "Get code snippets for common Streamlit patterns",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["all", "caching", "navigation", "session_state", "data_loading"],
                    "description": "Snippet category to retrieve",
                    "default": "all"
                }
            }
        }
    },
    {
        "name": "search_snippets",
        "description": "Search for code snippets matching a query",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search term to find in snippets"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "list_templates",
        "description": "List all available Streamlit app templates",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "load_template",
        "description": "Load a complete Streamlit app template",
        "inputSchema": {
            "type": "object",
            "properties": {
                "template_name": {
                    "type": "string",
                    "enum": ["dashboard_cached", "multipage_modern"],
                    "description": "Name of template to load"
                }
            },
            "required": ["template_name"]
        }
    },
    {
        "name": "suggest_cache_strategy",
        "description": "Get recommendations for caching strategy based on use case",
        "inputSchema": {
            "type": "object",
            "properties": {
                "use_case": {
                    "type": "string",
                    "description": "Description of what you want to cache (e.g., 'load CSV file', 'ML model', 'API call')"
                }
            },
            "required": ["use_case"]
        }
    },
    {
        "name": "get_navigation_guide",
        "description": "Get guide on modern st.navigation() patterns and multi-page apps",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_docs_overview",
        "description": "Get complete Streamlit documentation index with API reference, concepts, and tutorials",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_api_quick_ref",
        "description": "Get quick reference for a specific Streamlit API function with signature, description, and example",
        "inputSchema": {
            "type": "object",
            "properties": {
                "api_name": {
                    "type": "string",
                    "description": "Name of the API function (e.g., 'cache_data', 'session_state', 'dataframe', 'button', 'plotly_chart')"
                }
            },
            "required": ["api_name"]
        }
    },
    {
        "name": "search_develop_docs",
        "description": "Search within the complete Streamlit documentation for specific topics or APIs",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search term to find in documentation (e.g., 'cache_data', 'session_state', 'charts')"
                },
                "mode": {
                    "type": "string",
                    "enum": ["quick", "detailed"],
                    "description": "Search mode: 'quick' for brief file list with descriptions, 'detailed' for full context around matches",
                    "default": "quick"
                }
            },
            "required": ["query"]
        }
    }
]
