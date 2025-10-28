"""Page planning tool - the key feature of the Streamlit MCP server."""

from typing import List, Dict, Any
from .concepts import get_concept_based_recommendations


def plan_streamlit_page(
    description: str,
    page_type: str = "custom",
    features: List[str] | None = None,
    data_source: str = "none",
    layout_preference: str = "centered",
    data_freshness: str = "medium",
    performance_priority: str = "balanced",
    multipage: bool = False,
    include_testing: bool = False
) -> Dict[str, Any]:
    """
    Plan a Streamlit page based on requirements with architectural best practices.

    This is the key AI-powered tool that analyzes requirements and suggests
    optimal component combinations, layout structure, and generates complete
    page code with Streamlit best practices and architectural guidance.
    """
    features = features or []

    # Get concept-based recommendations from knowledge base
    concept_recommendations = get_concept_based_recommendations(
        page_type=page_type,
        features=features,
        data_source=data_source,
        data_freshness=data_freshness,
        performance_priority=performance_priority
    )

    # Component recommendations based on page type and features
    recommendations = {
        "layout": _plan_layout(page_type, layout_preference, features),
        "components": _plan_components(page_type, features, data_source),
        "data_handling": _plan_data_handling(data_source, features, concept_recommendations),
        "state_management": _plan_state_management(page_type, features, concept_recommendations),
        "best_practices": {
            "caching_strategy": concept_recommendations["caching"],
            "architecture_notes": concept_recommendations["architecture_notes"],
            "performance_tips": concept_recommendations["performance_tips"],
            "common_pitfalls": concept_recommendations["common_pitfalls"]
        },
        "advanced_features": {
            "fragments": concept_recommendations["fragments"],
            "forms": concept_recommendations["forms"],
            "multipage": concept_recommendations["multipage"] if multipage else None
        },
        "code": _generate_page_code(
            description, page_type, features, data_source, layout_preference,
            concept_recommendations, include_testing
        )
    }

    return recommendations


def _plan_layout(page_type: str, layout_preference: str, features: List[str]) -> Dict[str, Any]:
    """Plan the page layout structure."""
    layout_plan = {
        "page_config": {
            "layout": "wide" if layout_preference == "wide" else "centered",
            "initial_sidebar_state": "expanded" if layout_preference == "sidebar" else "auto"
        },
        "structure": []
    }

    if page_type == "dashboard":
        layout_plan["structure"] = [
            {"type": "title", "content": "Dashboard"},
            {"type": "metrics_row", "columns": 4},
            {"type": "charts_section", "columns": 2},
            {"type": "data_table"}
        ]
    elif page_type == "data_explorer":
        layout_plan["structure"] = [
            {"type": "title", "content": "Data Explorer"},
            {"type": "sidebar", "content": ["filters", "data_upload"] if "data_upload" in features else ["filters"]},
            {"type": "main_content", "sections": ["data_preview", "visualizations", "statistics"]}
        ]
    elif page_type == "chat":
        layout_plan["structure"] = [
            {"type": "title", "content": "Chat Interface"},
            {"type": "chat_container"},
            {"type": "chat_input"}
        ]
    elif page_type == "form":
        layout_plan["structure"] = [
            {"type": "title", "content": "Form"},
            {"type": "form", "fields": ["text_inputs", "selectors", "submit_button"]}
        ]
    elif page_type == "report":
        layout_plan["structure"] = [
            {"type": "title", "content": "Report"},
            {"type": "executive_summary"},
            {"type": "tabs", "sections": ["overview", "details", "analysis"]}
        ]
    else:  # custom
        layout_plan["structure"] = [
            {"type": "title", "content": "Custom Page"},
            {"type": "flexible", "note": "Build custom structure based on requirements"}
        ]

    return layout_plan


def _plan_components(page_type: str, features: List[str], data_source: str) -> List[Dict[str, Any]]:
    """Recommend specific Streamlit components."""
    components = []

    # Always start with page config
    components.append({
        "component": "st.set_page_config",
        "purpose": "Configure page metadata and layout",
        "priority": "critical"
    })

    # Add components based on page type
    if page_type == "dashboard":
        components.extend([
            {"component": "st.metric", "purpose": "Display KPIs", "count": "3-6"},
            {"component": "st.plotly_chart / st.altair_chart", "purpose": "Interactive visualizations", "count": "2-4"},
            {"component": "st.dataframe", "purpose": "Show data tables", "count": "1-2"},
            {"component": "st.columns", "purpose": "Side-by-side layout"},
        ])

    elif page_type == "data_explorer":
        components.extend([
            {"component": "st.file_uploader", "purpose": "Data upload"} if "data_upload" in features else None,
            {"component": "st.selectbox / st.multiselect", "purpose": "Data filtering"},
            {"component": "st.dataframe / st.data_editor", "purpose": "Interactive data view"},
            {"component": "st.download_button", "purpose": "Export data"} if "file_download" in features else None,
            {"component": "st.line_chart / st.bar_chart", "purpose": "Quick visualizations"},
        ])
        components = [c for c in components if c is not None]

    elif page_type == "chat":
        components.extend([
            {"component": "st.chat_message", "purpose": "Display messages"},
            {"component": "st.chat_input", "purpose": "User input"},
            {"component": "st.session_state", "purpose": "Store conversation history"},
            {"component": "st.write_stream", "purpose": "Streaming responses"} if "real_time_updates" in features else None,
        ])
        components = [c for c in components if c is not None]

    elif page_type == "form":
        components.extend([
            {"component": "st.form", "purpose": "Group inputs for batch submission"},
            {"component": "st.text_input", "purpose": "Text fields"},
            {"component": "st.selectbox / st.radio", "purpose": "Selection inputs"},
            {"component": "st.slider / st.number_input", "purpose": "Numeric inputs"},
            {"component": "st.form_submit_button", "purpose": "Submit form"},
        ])

    # Add common features
    if "data_filtering" in features:
        components.append({"component": "st.sidebar with filters", "purpose": "Filter controls"})

    if "authentication" in features:
        components.append({"component": "st.login / st.logout", "purpose": "User authentication"})

    if data_source != "none":
        components.append({"component": "st.cache_data", "purpose": "Cache data loading"})

    return components


def _plan_data_handling(data_source: str, features: List[str], concept_recommendations: Dict[str, Any]) -> Dict[str, Any]:
    """Plan data loading and processing with concept-based guidance."""
    data_plan = {}
    caching_guidance = concept_recommendations["caching"]

    if data_source == "upload":
        data_plan["method"] = "st.file_uploader"
        data_plan["processing"] = "pd.read_csv() or appropriate reader"
        data_plan["caching"] = caching_guidance["explanation"]
        data_plan["example"] = caching_guidance["example"]

    elif data_source == "api":
        data_plan["method"] = "requests.get() or httpx"
        data_plan["processing"] = "JSON parsing to DataFrame"
        data_plan["caching"] = caching_guidance["explanation"]
        data_plan["example"] = caching_guidance["example"]
        data_plan["ttl"] = caching_guidance["ttl"]

    elif data_source == "database":
        data_plan["method"] = "st.connection('sql') or database connector"
        data_plan["processing"] = "SQL query to DataFrame"
        data_plan["caching"] = caching_guidance["explanation"]
        data_plan["example"] = caching_guidance["example"]
        data_plan["ttl"] = caching_guidance["ttl"]

    elif data_source == "example":
        data_plan["method"] = "Generate sample data"
        data_plan["processing"] = "NumPy/Pandas generation"
        data_plan["caching"] = caching_guidance["explanation"]
        data_plan["example"] = caching_guidance["example"]

    else:  # none
        data_plan["method"] = "No data source specified"
        data_plan["note"] = "Add data source as needed"

    return data_plan


def _plan_state_management(page_type: str, features: List[str], concept_recommendations: Dict[str, Any]) -> Dict[str, Any]:
    """Plan session state usage with concept-based patterns."""
    # Use concept-based session state patterns
    state_patterns = concept_recommendations["session_state"]

    state_plan = {
        "required": state_patterns["required"],
        "variables": state_patterns["variables"],
        "initialization_code": state_patterns["initialization_code"],
        "best_practices": state_patterns["best_practices"]
    }

    return state_plan


def _generate_page_code(
    description: str,
    page_type: str,
    features: List[str],
    data_source: str,
    layout_preference: str,
    concept_recommendations: Dict[str, Any],
    include_testing: bool = False
) -> str:
    """Generate complete page code with best practices."""

    # Generate imports
    imports = ["import streamlit as st"]
    if data_source in ["api", "example", "database"]:
        imports.append("import pandas as pd")
    if data_source == "example":
        imports.append("import numpy as np")
    if data_source == "api":
        imports.append("import requests")

    # Generate page config with comments
    layout = "wide" if layout_preference == "wide" else "centered"
    page_config = f'''# Page Configuration
# Learn more: https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
st.set_page_config(
    page_title="{page_type.replace('_', ' ').title()}",
    page_icon="📊",
    layout="{layout}",  # 'wide' for dashboards, 'centered' for forms
    initial_sidebar_state="auto"
)
'''

    # Add best practices header comment
    best_practices_comment = """
# ========================================
# STREAMLIT BEST PRACTICES
# ========================================
# • Use @st.cache_data for data loading
# • Initialize session_state before accessing
# • Use fragments for expensive operations
# • Batch inputs with forms when appropriate
# ========================================
"""

    # Generate main content based on page type
    if page_type == "dashboard":
        main_content = _generate_dashboard_code(features, data_source, concept_recommendations)
    elif page_type == "data_explorer":
        main_content = _generate_data_explorer_code(features, data_source, concept_recommendations)
    elif page_type == "chat":
        main_content = _generate_chat_code(features, concept_recommendations)
    elif page_type == "form":
        main_content = _generate_form_code(features, concept_recommendations)
    elif page_type == "report":
        main_content = _generate_report_code(features, data_source, concept_recommendations)
    else:
        main_content = _generate_custom_code(description, features, concept_recommendations)

    # Combine all parts
    full_code = "\n".join(imports) + "\n" + page_config + best_practices_comment + "\n" + main_content

    # Add testing template if requested
    if include_testing:
        full_code += _generate_test_code(page_type)

    return full_code


def _generate_dashboard_code(features: List[str], data_source: str, concept_recommendations: Dict[str, Any]) -> str:
    """Generate dashboard page code with proper caching and best practices."""
    # Get caching recommendation from concepts
    caching = concept_recommendations["caching"]
    fragments_rec = concept_recommendations["fragments"]

    # Determine cache decorator
    if caching["decorator"]:
        if caching["ttl"]:
            cache_decorator = f'{caching["decorator"]}(ttl={caching["ttl"]})  # {caching["explanation"]}'
        else:
            cache_decorator = f'{caching["decorator"]}  # {caching["explanation"]}'
    else:
        cache_decorator = f'# {caching["explanation"]}'

    # Generate code with fragments if recommended
    if fragments_rec["should_use"]:
        return f'''
# Dashboard Title
st.title("📊 Dashboard")

# ================================================================================
# Data Loading with Caching
# Best Practice: Cache expensive data loading to avoid reloading on every rerun
# ================================================================================
{cache_decorator}
def load_data():
    # TODO: Replace with your data source
    import pandas as pd
    import numpy as np
    return pd.DataFrame({{
        'date': pd.date_range('2024-01-01', periods=100),
        'value': np.random.randn(100).cumsum(),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    }})

data = load_data()

# ================================================================================
# Key Metrics Row
# ================================================================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Records", len(data), delta="12%")
with col2:
    st.metric("Average Value", f"{{data['value'].mean():.2f}}", delta="-3%")
with col3:
    st.metric("Categories", data['category'].nunique())
with col4:
    st.metric("Latest Value", f"{{data['value'].iloc[-1]:.2f}}", delta="5%")

st.divider()

# ================================================================================
# Interactive Charts with Fragment
# Best Practice: Use fragments for expensive visualizations that update independently
# This prevents full page rerun when only charts need to update
# ================================================================================
@st.fragment
def chart_section():
    """Charts update independently from rest of page."""
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Time Series")
        st.line_chart(data.set_index('date')['value'])

    with col2:
        st.subheader("Category Distribution")
        st.bar_chart(data['category'].value_counts())

chart_section()

st.divider()

# ================================================================================
# Data Table
# ================================================================================
st.subheader("Data Table")
st.dataframe(data, use_container_width=True, hide_index=True)
'''
    else:
        # Standard dashboard without fragments
        return f'''
# Dashboard Title
st.title("📊 Dashboard")

# Data Loading with Caching
{cache_decorator}
def load_data():
    # TODO: Replace with your data source
    import pandas as pd
    import numpy as np
    return pd.DataFrame({{
        'date': pd.date_range('2024-01-01', periods=100),
        'value': np.random.randn(100).cumsum(),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    }})

data = load_data()

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Records", len(data), delta="12%")
with col2:
    st.metric("Average Value", f"{{data['value'].mean():.2f}}", delta="-3%")
with col3:
    st.metric("Categories", data['category'].nunique())
with col4:
    st.metric("Latest Value", f"{{data['value'].iloc[-1]:.2f}}", delta="5%")

st.divider()

# Charts Section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Time Series")
    st.line_chart(data.set_index('date')['value'])

with col2:
    st.subheader("Category Distribution")
    st.bar_chart(data['category'].value_counts())

st.divider()

# Data Table
st.subheader("Data Table")
st.dataframe(data, use_container_width=True, hide_index=True)
'''


def _generate_data_explorer_code(features: List[str], data_source: str, concept_recommendations: Dict[str, Any]) -> str:
    """Generate data explorer page code with best practices."""
    upload_code = ""
    if "data_upload" in features:
        upload_code = '''
# File Upload
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    # Load example data
    data = pd.DataFrame({
        'A': np.random.randn(100),
        'B': np.random.randn(100),
        'Category': np.random.choice(['X', 'Y', 'Z'], 100)
    })
'''
    else:
        upload_code = '''
# Load example data
data = pd.DataFrame({
    'A': np.random.randn(100),
    'B': np.random.randn(100),
    'Category': np.random.choice(['X', 'Y', 'Z'], 100)
})
'''

    return f'''
st.title("🔍 Data Explorer")

{upload_code}

# Sidebar filters
st.sidebar.header("Filters")
if 'Category' in data.columns:
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=data['Category'].unique(),
        default=data['Category'].unique()
    )
    data = data[data['Category'].isin(selected_categories)]

# Main content
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Visualizations", "📋 Data"])

with tab1:
    st.subheader("Data Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", len(data))
    with col2:
        st.metric("Columns", len(data.columns))
    with col3:
        st.metric("Memory", f"{{data.memory_usage(deep=True).sum() / 1024:.1f}} KB")

    st.subheader("Summary Statistics")
    st.dataframe(data.describe(), use_container_width=True)

with tab2:
    st.subheader("Data Visualizations")
    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()

    if len(numeric_cols) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            st.line_chart(data[numeric_cols[:2]])
        with col2:
            st.bar_chart(data[numeric_cols[:2]])

with tab3:
    st.subheader("Raw Data")
    st.dataframe(data, use_container_width=True)

    # Download button
    csv = data.to_csv(index=False)
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="data.csv",
        mime="text/csv"
    )
'''


def _generate_chat_code(features: List[str], concept_recommendations: Dict[str, Any]) -> str:
    """Generate chat interface code with best practices."""
    # Get session state initialization from concepts
    session_state = concept_recommendations["session_state"]
    init_code = session_state.get("initialization_code", "# Initialize chat history\nif 'messages' not in st.session_state:\n    st.session_state.messages = []")

    return f'''
st.title("💬 Chat Interface")

# ================================================================================
# Session State Initialization
# Best Practice: Always check if key exists before accessing session_state
# ================================================================================
{init_code}

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ================================================================================
# Chat Input
# Note: Session state persists across reruns, maintaining conversation history
# ================================================================================
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to history
    st.session_state.messages.append({{"role": "user", "content": prompt}})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        # TODO: Replace with your AI/logic
        response = f"Echo: " + prompt
        st.markdown(response)

    # Add assistant message to history
    st.session_state.messages.append({{"role": "assistant", "content": response}})
'''


def _generate_form_code(features: List[str], concept_recommendations: Dict[str, Any]) -> str:
    """Generate form page code with best practices."""
    return '''
st.title("📝 Form")

with st.form("my_form"):
    st.subheader("User Information")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        email = st.text_input("Email")
    with col2:
        age = st.number_input("Age", min_value=0, max_value=120)
        category = st.selectbox("Category", ["Option A", "Option B", "Option C"])

    st.subheader("Additional Details")
    comments = st.text_area("Comments")

    # Submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success("Form submitted successfully!")
        st.json({
            "name": name,
            "email": email,
            "age": age,
            "category": category,
            "comments": comments
        })
'''


def _generate_report_code(features: List[str], data_source: str, concept_recommendations: Dict[str, Any]) -> str:
    """Generate report page code with best practices."""
    return '''
st.title("📄 Report")

# Executive Summary
st.header("Executive Summary")
st.markdown("""
This report provides an overview of key metrics and insights.
""")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["Overview", "Detailed Analysis", "Conclusions"])

with tab1:
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Key Metric 1", "100", "+10%")
    with col2:
        st.metric("Key Metric 2", "85", "-5%")
    with col3:
        st.metric("Key Metric 3", "42", "+2%")

with tab2:
    st.subheader("Detailed Analysis")
    st.write("Detailed charts and tables go here...")

with tab3:
    st.subheader("Conclusions")
    st.markdown("""
    - Key finding 1
    - Key finding 2
    - Key finding 3
    """)
'''


def _generate_custom_code(description: str, features: List[str], concept_recommendations: Dict[str, Any]) -> str:
    """Generate custom page code with best practices."""
    return f'''
st.title("Custom Page")

st.write("""
## Page Description
{description}
""")

# TODO: Implement your custom logic here based on requirements:
# Features requested: {", ".join(features) if features else "None specified"}

st.info("This is a starting template. Customize it based on your needs.")
'''


def _generate_test_code(page_type: str) -> str:
    """Generate test template for the page."""
    return f'''


# ================================================================================
# TEST TEMPLATE
# ================================================================================
# Save this as test_{page_type}.py
# Run with: pytest test_{page_type}.py

"""
from streamlit.testing.v1 import AppTest

def test_{page_type}_loads():
    \"\"\"Test that the {page_type} page loads without errors.\"\"\"
    at = AppTest.from_file("{page_type}.py")
    at.run()
    assert not at.exception

def test_{page_type}_title():
    \"\"\"Test that page has correct title.\"\"\"
    at = AppTest.from_file("{page_type}.py")
    at.run()
    assert len(at.title) > 0

# Add more tests as needed
"""
'''


# Tool definition
TOOL = {
    "name": "plan_streamlit_page",
    "description": """
    AI-powered page planner that analyzes requirements and generates a complete Streamlit page plan
    with architectural best practices and performance optimization.

    This enhanced tool provides:
    • Component recommendations based on page type
    • Caching strategies for different data sources
    • Session state patterns for stateful apps
    • Fragment recommendations for performance
    • Form usage guidance for batch inputs
    • Multipage app structure suggestions
    • Architecture notes and common pitfalls
    • Complete runnable code with inline best practices

    Use this tool when starting a new page or when you need guidance on Streamlit best practices.
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Detailed description of what the page should do/display"
            },
            "page_type": {
                "type": "string",
                "enum": ["dashboard", "data_explorer", "chat", "form", "report", "custom"],
                "description": "Type of page to create",
                "default": "custom"
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
            "multipage": {
                "type": "boolean",
                "description": "Whether to include multipage app guidance",
                "default": False
            },
            "include_testing": {
                "type": "boolean",
                "description": "Whether to include test template",
                "default": False
            }
        },
        "required": ["description", "page_type"]
    }
}
