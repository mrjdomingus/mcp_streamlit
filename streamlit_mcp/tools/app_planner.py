"""App planning tools - comprehensive planning system for Streamlit apps."""

import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from .concepts import get_concept_based_recommendations


# Plans folder at project root
PLANS_DIR = Path("./plans")


def ensure_plans_directory() -> Path:
    """Ensure the plans directory exists."""
    PLANS_DIR.mkdir(exist_ok=True)
    return PLANS_DIR


def get_timestamp() -> str:
    """Get current timestamp for tracking updates."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_app_plan(
    app_name: str,
    description: str,
    pages: List[Dict[str, str]],
    tech_stack: Optional[List[str]] = None,
    shared_dependencies: Optional[List[str]] = None,
    implementation_phases: Optional[List[str]] = None,
    architecture_notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a comprehensive full application plan.

    Generates a markdown file at ./plans/full_plan.md containing:
    - App overview (goals, architecture, tech stack)
    - Page list with links to individual page plan files
    - Shared dependencies (components, libraries, data models)
    - Implementation order and phased approach

    If the file exists, it will append/update the plan with new information.

    Args:
        app_name: Name of the application
        description: Detailed description of what the app does
        pages: List of pages, each with 'name', 'description', and optional 'type'
        tech_stack: List of technologies/libraries to use
        shared_dependencies: List of shared components, utilities, or data models
        implementation_phases: List of implementation phases/milestones
        architecture_notes: Additional architecture considerations

    Returns:
        Dict with plan details and file path
    """
    ensure_plans_directory()

    tech_stack = tech_stack or ["Streamlit", "Python 3.11+", "Pandas", "Plotly"]
    shared_dependencies = shared_dependencies or []
    implementation_phases = implementation_phases or []

    # Generate markdown content
    timestamp = get_timestamp()

    # App Overview Section
    overview_section = f"""# {app_name} - Full Application Plan

**Last Updated**: {timestamp}

## App Overview

### Description
{description}

### Goals
- Build a modern, responsive Streamlit application
- Implement best practices for performance and maintainability
- Create reusable components for consistency across pages
- Ensure proper state management and data flow

### Tech Stack
"""
    for tech in tech_stack:
        overview_section += f"- {tech}\n"

    # Pages Section with links
    pages_section = f"""
## Pages

This application consists of {len(pages)} page(s):

"""
    for i, page in enumerate(pages, 1):
        page_name = page.get('name', f'Page {i}')
        page_desc = page.get('description', 'No description provided')
        page_type = page.get('type', 'custom')
        page_filename = page_name.lower().replace(' ', '_')

        pages_section += f"""### {i}. {page_name}
**Type**: {page_type}
**Description**: {page_desc}
**Plan**: [`page_{page_filename}.md`](./page_{page_filename}.md)

"""

    # Dependencies Section
    dependencies_section = """## Shared Dependencies

### Reusable Components
"""
    if shared_dependencies:
        for dep in shared_dependencies:
            dependencies_section += f"- {dep}\n"
    else:
        dependencies_section += """- `components/header.py` - Shared header component
- `components/footer.py` - Shared footer component
- `utils/data_loader.py` - Common data loading utilities
- `utils/state_manager.py` - Session state helpers
"""

    dependencies_section += """
### Recommended Libraries
- `streamlit` - Core framework
- `pandas` - Data manipulation
- `plotly` - Interactive visualizations
- `streamlit-extras` - Additional UI components (optional)
"""

    # Implementation Order Section
    implementation_section = """
## Implementation Order

### Recommended Approach
"""
    if implementation_phases:
        for i, phase in enumerate(implementation_phases, 1):
            implementation_section += f"{i}. {phase}\n"
    else:
        implementation_section += """1. **Phase 1: Foundation**
   - Set up project structure
   - Create shared components and utilities
   - Implement basic navigation structure

2. **Phase 2: Core Pages**
   - Build main/home page
   - Implement primary functionality pages
   - Add basic state management

3. **Phase 3: Advanced Features**
   - Add authentication (if needed)
   - Implement data connections
   - Add caching strategies

4. **Phase 4: Polish**
   - Add error handling
   - Optimize performance
   - Write tests
   - Documentation
"""

    # Architecture Notes Section
    architecture_section = """
## Architecture Notes

### Best Practices
- **Caching**: Use `@st.cache_data` for data loading, `@st.cache_resource` for ML models/connections
- **State Management**: Initialize session state keys before accessing them
- **Performance**: Use fragments (`@st.fragment`) for expensive operations that update independently
- **Forms**: Batch inputs with `st.form` to prevent reruns on every input change
- **Navigation**: Use modern `st.navigation()` for multi-page apps

### Directory Structure
```
project/
├── app.py                 # Main entry point (if using st.navigation)
├── pages/                 # Individual page files (if using file-based routing)
│   ├── 1_page1.py
│   └── 2_page2.py
├── pages_lib/            # Page modules (if using st.navigation)
│   ├── page1.py
│   └── page2.py
├── components/           # Reusable components
├── utils/                # Utilities and helpers
├── data/                 # Data files
└── plans/                # This folder with planning documents
```
"""

    if architecture_notes:
        architecture_section += f"""
### Additional Considerations
{architecture_notes}
"""

    # Next Steps Section
    next_steps_section = """
## Next Steps

1. **Create Individual Page Plans**: Use the `create_page_plan` tool for each page
2. **Set Up Project Structure**: Create the directory layout
3. **Build Shared Components**: Start with common utilities
4. **Implement Pages**: Follow the implementation order above
5. **Test & Iterate**: Run and refine each page

---

**Generated by Streamlit MCP Server** | Use `create_page_plan` to plan individual pages
"""

    # Combine all sections
    full_content = (
        overview_section +
        pages_section +
        dependencies_section +
        implementation_section +
        architecture_section +
        next_steps_section
    )

    # Write or append to file
    plan_file = PLANS_DIR / "full_plan.md"

    if plan_file.exists():
        # Append mode: add a separator and new content
        existing_content = plan_file.read_text()
        separator = f"\n\n---\n\n## Update ({timestamp})\n\n"
        full_content = existing_content + separator + full_content

    plan_file.write_text(full_content)

    return {
        "status": "success",
        "file_path": str(plan_file.absolute()),
        "app_name": app_name,
        "pages_count": len(pages),
        "message": f"Full application plan created/updated at {plan_file}",
        "next_action": "Use create_page_plan tool to plan individual pages"
    }


def create_page_plan(
    page_name: str,
    page_type: str,
    description: str,
    features: Optional[List[str]] = None,
    data_source: str = "none",
    layout_preference: str = "centered",
    data_freshness: str = "medium",
    performance_priority: str = "balanced",
    dependencies: Optional[List[str]] = None,
    related_pages: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a detailed plan for an individual page.

    Generates a markdown file at ./plans/page_<name>.md containing:
    - UI components and layout structure
    - Data flow (state management, API calls, transformations)
    - Dependencies (libraries, shared components, other pages)
    - Step-by-step implementation guide

    If the file exists, it will append/update the plan with new information.

    Args:
        page_name: Name of the page
        page_type: Type of page (dashboard, data_explorer, chat, form, report, custom)
        description: What the page should do/display
        features: List of features to include
        data_source: Where data comes from (upload, api, database, example, none)
        layout_preference: Layout style (wide, centered, sidebar)
        data_freshness: How fresh data needs to be (high, medium, low)
        performance_priority: Performance optimization priority (speed, memory, balanced)
        dependencies: List of required libraries/components
        related_pages: List of related pages that this page links to/from

    Returns:
        Dict with plan details and file path
    """
    ensure_plans_directory()

    features = features or []
    dependencies = dependencies or []
    related_pages = related_pages or []

    # Get concept-based recommendations
    concept_recommendations = get_concept_based_recommendations(
        page_type=page_type,
        features=features,
        data_source=data_source,
        data_freshness=data_freshness,
        performance_priority=performance_priority
    )

    timestamp = get_timestamp()
    page_filename = page_name.lower().replace(' ', '_')

    # Header Section
    header_section = f"""# {page_name} - Page Plan

**Last Updated**: {timestamp}
**Page Type**: {page_type}
**Status**: Planning

## Overview

{description}

"""

    # UI Components Section
    components_section = """## UI Components & Layout

### Page Configuration
"""
    layout = "wide" if layout_preference == "wide" else "centered"
    sidebar_state = "expanded" if layout_preference == "sidebar" else "auto"

    components_section += f"""- **Layout**: {layout}
- **Sidebar**: {sidebar_state}
- **Page Icon**: 📊 (customize as needed)

### Main Components
"""

    # Get component recommendations based on page type
    if page_type == "dashboard":
        components_section += """- Title/Header
- Metrics row (3-6 KPI cards using `st.metric`)
- Interactive filters (in sidebar)
- Charts section (2-4 visualizations using `st.plotly_chart` or `st.altair_chart`)
- Data table (`st.dataframe` with full-width)
"""
    elif page_type == "data_explorer":
        components_section += """- Title/Header
- File uploader (if needed) - `st.file_uploader`
- Sidebar filters - `st.selectbox`, `st.multiselect`
- Tabs for different views - `st.tabs`
  - Overview tab: summary statistics
  - Visualizations tab: charts
  - Data tab: raw data table
- Download button - `st.download_button`
"""
    elif page_type == "chat":
        components_section += """- Title/Header
- Chat message container (scrollable)
- Individual messages - `st.chat_message`
- Chat input - `st.chat_input`
- Optional: streaming response - `st.write_stream`
"""
    elif page_type == "form":
        components_section += """- Title/Header
- Form container - `st.form`
- Input fields:
  - Text inputs - `st.text_input`
  - Selection inputs - `st.selectbox`, `st.radio`
  - Numeric inputs - `st.number_input`, `st.slider`
- Submit button - `st.form_submit_button`
- Success/error messages
"""
    elif page_type == "report":
        components_section += """- Title/Header
- Executive summary section
- Tabs for different sections - `st.tabs`
- Metrics for key findings - `st.metric`
- Charts and visualizations
- Download report button (optional)
"""
    else:  # custom
        components_section += """- Title/Header
- Custom components based on requirements
- (Define specific UI elements needed)
"""

    # Data Flow Section
    data_flow_section = """
## Data Flow

### Data Loading
"""

    caching_rec = concept_recommendations["caching"]
    if data_source != "none":
        data_flow_section += f"""**Strategy**: {caching_rec['explanation']}

**Implementation**:
```python
{caching_rec.get('example', '# Add caching decorator')}
```

**TTL**: {caching_rec.get('ttl', 'Not applicable')}
"""
    else:
        data_flow_section += "No external data source specified.\n"

    # State Management
    state_rec = concept_recommendations["session_state"]
    data_flow_section += f"""
### State Management

**Required**: {"Yes" if state_rec["required"] else "No"}

"""
    if state_rec["required"]:
        data_flow_section += f"""**State Variables**:
"""
        for var in state_rec.get("variables", []):
            data_flow_section += f"- `{var}`\n"

        data_flow_section += f"""
**Initialization**:
```python
{state_rec.get('initialization_code', '# Initialize state here')}
```
"""

    # Dependencies Section
    dependencies_section = """
## Dependencies

### Required Libraries
"""
    required_libs = ["streamlit"]
    if data_source in ["api", "database"]:
        required_libs.append("pandas")
    if data_source == "api":
        required_libs.append("requests")
    if "charts" in features:
        required_libs.append("plotly")

    for lib in required_libs:
        dependencies_section += f"- `{lib}`\n"

    if dependencies:
        dependencies_section += "\n### Additional Dependencies\n"
        for dep in dependencies:
            dependencies_section += f"- {dep}\n"

    if related_pages:
        dependencies_section += "\n### Related Pages\n"
        for page in related_pages:
            page_file = page.lower().replace(' ', '_')
            dependencies_section += f"- [{page}](./page_{page_file}.md)\n"

    # Implementation Steps Section
    implementation_section = f"""
## Implementation Steps

### Step 1: Set Up Page Structure
1. Create new Python file: `{page_filename}.py`
2. Add page configuration:
```python
import streamlit as st

st.set_page_config(
    page_title="{page_name}",
    page_icon="📊",
    layout="{layout}",
    initial_sidebar_state="{sidebar_state}"
)
```

### Step 2: Implement Data Loading
"""

    if data_source != "none":
        implementation_section += f"""1. Add data loading function with caching
2. {caching_rec['explanation']}
3. Handle errors gracefully with try/except

"""
    else:
        implementation_section += "No data loading needed for this page.\n\n"

    implementation_section += """### Step 3: Initialize Session State
"""
    if state_rec["required"]:
        implementation_section += """1. Initialize required state variables
2. Use the pattern: `if 'key' not in st.session_state: st.session_state.key = default`
3. Access state throughout the page

"""
    else:
        implementation_section += "No session state needed for this page.\n\n"

    implementation_section += f"""### Step 4: Build UI Components
1. Add title and header
2. Create layout structure (columns, tabs, sidebar)
3. Add widgets and display elements
4. Implement interactivity (buttons, inputs)

### Step 5: Test & Refine
1. Run locally: `streamlit run {page_filename}.py`
2. Test all interactions and data flows
3. Optimize performance if needed
4. Add error handling
"""

    # Best Practices Section
    best_practices_section = """
## Best Practices & Tips

### Performance
"""
    for tip in concept_recommendations.get("performance_tips", []):
        best_practices_section += f"- {tip}\n"

    best_practices_section += "\n### Common Pitfalls\n"
    for pitfall in concept_recommendations.get("common_pitfalls", []):
        best_practices_section += f"- {pitfall}\n"

    # Fragments recommendation
    fragments_rec = concept_recommendations.get("fragments", {})
    if fragments_rec.get("should_use"):
        best_practices_section += f"""
### Use Fragments
{fragments_rec.get('explanation', 'Consider using fragments for better performance')}

Example use case: {fragments_rec.get('use_case', 'Expensive visualizations that update independently')}
"""

    # Forms recommendation
    forms_rec = concept_recommendations.get("forms", {})
    if forms_rec.get("should_use"):
        best_practices_section += f"""
### Use Forms
{forms_rec.get('explanation', 'Use forms to batch inputs')}
"""

    # Code Generation Section
    code_section = """
## Code Template

See the generated code template using the `plan_streamlit_page` tool, or build manually following the implementation steps above.

---

**Generated by Streamlit MCP Server**
"""

    # Combine all sections
    full_content = (
        header_section +
        components_section +
        data_flow_section +
        dependencies_section +
        implementation_section +
        best_practices_section +
        code_section
    )

    # Write or append to file
    plan_file = PLANS_DIR / f"page_{page_filename}.md"

    if plan_file.exists():
        # Append mode: add a separator and new content
        existing_content = plan_file.read_text()
        separator = f"\n\n---\n\n## Update ({timestamp})\n\n"
        full_content = existing_content + separator + full_content

    plan_file.write_text(full_content)

    return {
        "status": "success",
        "file_path": str(plan_file.absolute()),
        "page_name": page_name,
        "page_type": page_type,
        "message": f"Page plan created/updated at {plan_file}",
        "recommendations": {
            "caching": caching_rec.get("decorator"),
            "session_state_required": state_rec["required"],
            "use_fragments": fragments_rec.get("should_use", False),
            "use_forms": forms_rec.get("should_use", False)
        }
    }


# Tool definitions
TOOLS = [
    {
        "name": "create_app_plan",
        "description": """
        Create a comprehensive full application plan for a multi-page Streamlit app.

        This tool generates a markdown file at ./plans/full_plan.md containing:
        • App overview with goals, architecture, and tech stack
        • Complete list of pages with links to individual page plans
        • Shared dependencies (components, libraries, data models)
        • Implementation order and phased approach
        • Best practices and architecture notes

        Use this tool when starting a new Streamlit project to create a master plan.
        The plan file will be updated (not overwritten) if it already exists.
        """,
        "inputSchema": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "Name of the application"
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of what the app does and its purpose"
                },
                "pages": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "type": {
                                "type": "string",
                                "enum": ["dashboard", "data_explorer", "chat", "form", "report", "custom"]
                            }
                        },
                        "required": ["name", "description"]
                    },
                    "description": "List of pages in the app, each with name, description, and optional type"
                },
                "tech_stack": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Technologies and libraries to use (optional, defaults provided)"
                },
                "shared_dependencies": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Shared components, utilities, or data models (optional)"
                },
                "implementation_phases": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of implementation phases/milestones (optional, defaults provided)"
                },
                "architecture_notes": {
                    "type": "string",
                    "description": "Additional architecture considerations (optional)"
                }
            },
            "required": ["app_name", "description", "pages"]
        }
    },
    {
        "name": "create_page_plan",
        "description": """
        Create a detailed plan for an individual page in your Streamlit app.

        This tool generates a markdown file at ./plans/page_<name>.md containing:
        • UI components and layout structure specific to the page
        • Data flow including state management and API calls
        • Dependencies on libraries, shared components, and other pages
        • Step-by-step implementation guide with code examples
        • Best practices and performance tips

        Use this tool after creating the full app plan to plan each page in detail.
        The plan file will be updated (not overwritten) if it already exists.
        """,
        "inputSchema": {
            "type": "object",
            "properties": {
                "page_name": {
                    "type": "string",
                    "description": "Name of the page"
                },
                "page_type": {
                    "type": "string",
                    "enum": ["dashboard", "data_explorer", "chat", "form", "report", "custom"],
                    "description": "Type of page to create"
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of what the page should do/display"
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
                    "description": "List of features the page should include (optional)"
                },
                "data_source": {
                    "type": "string",
                    "enum": ["upload", "api", "database", "example", "none"],
                    "description": "Where data comes from",
                    "default": "none"
                },
                "layout_preference": {
                    "type": "string",
                    "enum": ["wide", "centered", "sidebar"],
                    "description": "Preferred layout style",
                    "default": "centered"
                },
                "data_freshness": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "How fresh data needs to be (affects caching TTL)",
                    "default": "medium"
                },
                "performance_priority": {
                    "type": "string",
                    "enum": ["speed", "memory", "balanced"],
                    "description": "Performance optimization priority",
                    "default": "balanced"
                },
                "dependencies": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of required libraries/components beyond defaults (optional)"
                },
                "related_pages": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of related pages that this page links to/from (optional)"
                }
            },
            "required": ["page_name", "page_type", "description"]
        }
    }
]
