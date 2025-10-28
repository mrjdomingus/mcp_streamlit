"""Streamlit concepts knowledge base for planning tool."""

from typing import Dict, List, Any
from pathlib import Path


class StreamlitConcepts:
    """
    Knowledge base of Streamlit architectural concepts and best practices.
    Extracted from official Streamlit documentation.
    """

    @staticmethod
    def get_caching_guidance(data_source: str, data_freshness: str = "medium") -> Dict[str, Any]:
        """Get caching strategy recommendations based on data source and freshness needs."""
        guidance = {
            "decorator": None,
            "ttl": None,
            "explanation": "",
            "example": ""
        }

        if data_source == "upload":
            guidance["decorator"] = None
            guidance["explanation"] = "User-uploaded data should not be cached as it's session-specific"
            guidance["example"] = "# No caching needed - user uploads are session-specific"

        elif data_source == "api":
            guidance["decorator"] = "@st.cache_data"
            if data_freshness == "high":
                guidance["ttl"] = 300  # 5 minutes
            elif data_freshness == "low":
                guidance["ttl"] = 7200  # 2 hours
            else:  # medium
                guidance["ttl"] = 1800  # 30 minutes

            guidance["explanation"] = (
                "API data should use @st.cache_data with TTL to balance freshness and performance. "
                "The cache creates a new copy for each session, preventing race conditions."
            )
            guidance["example"] = f"""@st.cache_data(ttl={guidance['ttl']})  # Cache for {guidance['ttl']/60:.0f} minutes
def load_api_data():
    response = requests.get("https://api.example.com/data")
    return pd.DataFrame(response.json())"""

        elif data_source == "database":
            guidance["decorator"] = "@st.cache_data"
            if data_freshness == "high":
                guidance["ttl"] = 600  # 10 minutes
            elif data_freshness == "low":
                guidance["ttl"] = 3600  # 1 hour
            else:  # medium
                guidance["ttl"] = 1800  # 30 minutes

            guidance["explanation"] = (
                "Database queries should use @st.cache_data with TTL. For connection objects, "
                "use @st.cache_resource to avoid recreating connections."
            )
            guidance["example"] = f"""@st.cache_data(ttl={guidance['ttl']})  # Cache query results
def run_query(query):
    conn = st.connection("sql")
    return conn.query(query)

@st.cache_resource  # Cache connection object
def get_database_connection():
    return create_db_connection()"""

        elif data_source == "example":
            guidance["decorator"] = "@st.cache_data"
            guidance["ttl"] = None
            guidance["explanation"] = "Static example data can be cached indefinitely"
            guidance["example"] = """@st.cache_data  # Cache indefinitely
def generate_sample_data():
    return pd.DataFrame({
        'x': np.random.randn(100),
        'y': np.random.randn(100)
    })"""

        return guidance

    @staticmethod
    def get_session_state_patterns(page_type: str, features: List[str]) -> Dict[str, Any]:
        """Get session state patterns based on page type and features."""
        patterns = {
            "required": False,
            "variables": [],
            "initialization_code": "",
            "best_practices": []
        }

        # Chat interfaces always need session state
        if page_type == "chat":
            patterns["required"] = True
            patterns["variables"] = [
                {"name": "messages", "type": "list", "purpose": "Store chat history", "default": "[]"}
            ]
            patterns["initialization_code"] = """# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []"""
            patterns["best_practices"] = [
                "Always check if key exists before initializing",
                "Use session state for chat history to persist across reruns",
                "Session state persists across pages in multipage apps"
            ]

        # Data filtering needs session state
        if "data_filtering" in features:
            patterns["required"] = True
            patterns["variables"].append(
                {"name": "filters", "type": "dict", "purpose": "Active filter values", "default": "{}"}
            )
            if not patterns["initialization_code"]:
                patterns["initialization_code"] = """# Initialize filter state
if "filters" not in st.session_state:
    st.session_state.filters = {}"""

        # Authentication needs session state
        if "authentication" in features:
            patterns["required"] = True
            patterns["variables"].append(
                {"name": "authenticated", "type": "bool", "purpose": "Auth status", "default": "False"}
            )
            patterns["best_practices"].append(
                "Store authentication state in session_state to persist across pages"
            )

        # Multi-step forms need state
        if "multi_step_form" in features:
            patterns["required"] = True
            patterns["variables"].extend([
                {"name": "step", "type": "int", "purpose": "Current form step", "default": "0"},
                {"name": "form_data", "type": "dict", "purpose": "Collected form data", "default": "{}"}
            ])
            patterns["best_practices"].append(
                "Use session state to preserve form data between steps"
            )

        return patterns

    @staticmethod
    def get_fragment_recommendations(page_type: str, features: List[str]) -> Dict[str, Any]:
        """Recommend fragment usage for performance optimization."""
        recommendations = {
            "should_use": False,
            "use_cases": [],
            "example_code": ""
        }

        # Dashboards with charts benefit from fragments
        if page_type == "dashboard":
            recommendations["should_use"] = True
            recommendations["use_cases"] = [
                "Wrap filter controls in fragment to update charts without full rerun",
                "Wrap individual chart sections to update independently",
                "Use for expensive visualizations that don't need to update together"
            ]
            recommendations["example_code"] = """@st.fragment
def chart_section():
    # This chart updates independently
    filter_val = st.slider("Filter", 0, 100, 50)
    filtered_data = data[data['value'] > filter_val]
    st.line_chart(filtered_data)

chart_section()  # Only this section reruns when slider changes"""

        # Data explorers with visualizations
        if page_type == "data_explorer" and "charts" in features:
            recommendations["should_use"] = True
            recommendations["use_cases"] = [
                "Isolate expensive data processing in fragments",
                "Update visualizations without reloading data"
            ]

        # Real-time updates need fragments
        if "real_time_updates" in features:
            recommendations["should_use"] = True
            recommendations["use_cases"] = [
                "Auto-refresh specific components without full rerun",
                "Stream data updates to isolated sections"
            ]
            recommendations["example_code"] = """@st.fragment(run_every="5s")
def live_metrics():
    # Auto-updates every 5 seconds
    latest_data = fetch_latest_data()
    st.metric("Live Value", latest_data)

live_metrics()"""

        return recommendations

    @staticmethod
    def get_form_recommendations(page_type: str, features: List[str]) -> Dict[str, Any]:
        """Recommend form usage for batch input."""
        recommendations = {
            "should_use": False,
            "rationale": "",
            "example_code": ""
        }

        # Form pages obviously need forms
        if page_type == "form":
            recommendations["should_use"] = True
            recommendations["rationale"] = (
                "Forms batch user input into a single rerun, preventing the app from "
                "updating with each field change. Essential for multi-field forms."
            )
            recommendations["example_code"] = """with st.form("my_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=0)

    submitted = st.form_submit_button("Submit")
    if submitted:
        # Process form data only when submitted
        process_form(name, email, age)"""

        # Multi-field filters benefit from forms
        if "data_filtering" in features and page_type in ["dashboard", "data_explorer"]:
            recommendations["should_use"] = True
            recommendations["rationale"] = (
                "Use forms for multi-field filters to prevent expensive data processing "
                "on each filter change. Users can set all filters then click 'Apply'."
            )

        return recommendations

    @staticmethod
    def get_multipage_guidance(features: List[str]) -> Dict[str, Any]:
        """Provide guidance on multipage app structure."""
        guidance = {
            "recommended": False,
            "method": "st.navigation",
            "rationale": "",
            "structure": {},
            "example_code": ""
        }

        # Recommend multipage for complex apps
        if any(f in features for f in ["authentication", "multi_step_form"]) or len(features) > 5:
            guidance["recommended"] = True
            guidance["rationale"] = (
                "Complex apps benefit from multipage structure for better organization, "
                "clearer navigation, and improved performance (only active page loads)."
            )
            guidance["structure"] = {
                "entrypoint": "app.py",
                "method": "st.navigation with st.Page (using functions or file paths)",
                "note": "No pages/ folder required - define page functions in app.py or use separate files in any location",
                "benefits": [
                    "Share common elements (auth, sidebar) across pages",
                    "Better code organization",
                    "Faster load times (lazy loading)",
                    "Session state persists across pages",
                    "Flexible file organization (no magic folders)"
                ]
            }
            guidance["example_code"] = """# app.py (entrypoint)
import streamlit as st

# Define page functions directly (no pages folder needed)
def home():
    st.title("🏠 Home")
    st.write("Welcome to the home page!")

def dashboard():
    st.title("📊 Dashboard")
    st.write("Dashboard content here...")

def profile():
    st.title("👤 Profile")
    st.write("User profile settings...")

def config():
    st.title("⚙️ Config")
    st.write("App configuration...")

# Define navigation using st.Page with functions
pages = {
    "Main": [
        st.Page(home, title="Home", icon="🏠"),
        st.Page(dashboard, title="Dashboard", icon="📊"),
    ],
    "Settings": [
        st.Page(profile, title="Profile", icon="👤"),
        st.Page(config, title="Config", icon="⚙️"),
    ]
}

pg = st.navigation(pages)
pg.run()

# Alternative: Use file paths if you prefer separate files
# pages = {
#     "Main": [
#         st.Page("home.py", title="Home", icon="🏠"),
#         st.Page("dashboard.py", title="Dashboard", icon="📊"),
#     ]
# }
# Note: Files can be in root directory, no pages/ folder required"""

        return guidance

    @staticmethod
    def get_architecture_notes(page_type: str, features: List[str]) -> List[str]:
        """Get important architectural considerations."""
        notes = []

        # Client-server architecture
        notes.append(
            "Remember: Streamlit has a client-server architecture. Your Python code runs on the "
            "server, while the browser is the client. The app can't access user's local files "
            "except through st.file_uploader."
        )

        # Rerun model
        notes.append(
            "Streamlit reruns your script from top to bottom on every interaction. Use caching "
            "and session state to optimize performance and maintain state."
        )

        # File uploads
        if "data_upload" in features:
            notes.append(
                "File uploads are temporary and stored on the server. In production with load "
                "balancing, enable session affinity to avoid MediaFileStorageError."
            )

        # Database connections
        if "database" in [f for f in features if "database" in f.lower()]:
            notes.append(
                "Use st.connection() for database connections. Connection objects should be "
                "cached with @st.cache_resource to avoid recreating connections on each rerun."
            )

        # Real-time updates
        if "real_time_updates" in features:
            notes.append(
                "For real-time updates, use fragments with run_every parameter or WebSocket "
                "connections. Remember that each browser tab creates a separate session."
            )

        return notes

    @staticmethod
    def get_performance_tips(page_type: str, data_source: str, features: List[str]) -> List[str]:
        """Get performance optimization tips."""
        tips = []

        # Caching is key
        if data_source != "none":
            tips.append(
                "✓ Cache expensive data loading operations with @st.cache_data to avoid "
                "reloading on every rerun"
            )

        # Fragments for dashboards
        if page_type == "dashboard" or "charts" in features:
            tips.append(
                "✓ Use @st.fragment for expensive visualizations to update them independently "
                "without full script rerun"
            )

        # Data loading
        if data_source in ["api", "database"]:
            tips.append(
                "✓ Load minimal data needed for display. Use pagination or filtering on the "
                "backend rather than loading everything and filtering client-side"
            )

        # Forms
        if page_type == "form" or "data_filtering" in features:
            tips.append(
                "✓ Use st.form to batch multiple inputs, preventing reruns on each change"
            )

        # Dataframes
        if page_type in ["dashboard", "data_explorer"]:
            tips.append(
                "✓ Use st.dataframe with large datasets instead of st.data_editor unless "
                "editing is required. Limit rows displayed with slicing or pagination"
            )

        return tips

    @staticmethod
    def get_common_pitfalls(page_type: str, features: List[str]) -> List[str]:
        """Get common mistakes to avoid."""
        pitfalls = []

        # Session state initialization
        pitfalls.append(
            "⚠️ Always check if key exists in session_state before accessing it, or use "
            "setdefault(). Accessing uninitialized keys raises an exception."
        )

        # Button behavior
        if any(f in features for f in ["user_input", "data_filtering"]):
            pitfalls.append(
                "⚠️ Button state is only True for one rerun (when clicked). If you need to "
                "preserve state after button click, store it in session_state."
            )

        # Caching mutable objects
        pitfalls.append(
            "⚠️ Don't mutate cached objects returned by @st.cache_data. It creates copies "
            "to prevent this, but mutations to returned objects won't persist as expected."
        )

        # Forms
        if page_type == "form":
            pitfalls.append(
                "⚠️ Widgets inside forms don't trigger reruns until the form is submitted. "
                "Don't mix form and non-form widgets if you expect immediate updates."
            )

        # File paths
        if "data_upload" in features:
            pitfalls.append(
                "⚠️ Don't use hardcoded local file paths - they won't work when deployed. "
                "Use st.file_uploader for user data or package data files with your app."
            )

        return pitfalls


def get_concept_based_recommendations(
    page_type: str,
    features: List[str],
    data_source: str,
    data_freshness: str = "medium",
    performance_priority: str = "balanced"
) -> Dict[str, Any]:
    """
    Get comprehensive concept-based recommendations for app planning.

    Args:
        page_type: Type of page (dashboard, data_explorer, chat, etc.)
        features: List of features the page needs
        data_source: Where data comes from (upload, api, database, etc.)
        data_freshness: How fresh data needs to be (high, medium, low)
        performance_priority: Priority level (speed, memory, balanced)

    Returns:
        Dictionary with comprehensive recommendations
    """
    concepts = StreamlitConcepts()

    return {
        "caching": concepts.get_caching_guidance(data_source, data_freshness),
        "session_state": concepts.get_session_state_patterns(page_type, features),
        "fragments": concepts.get_fragment_recommendations(page_type, features),
        "forms": concepts.get_form_recommendations(page_type, features),
        "multipage": concepts.get_multipage_guidance(features),
        "architecture_notes": concepts.get_architecture_notes(page_type, features),
        "performance_tips": concepts.get_performance_tips(page_type, data_source, features),
        "common_pitfalls": concepts.get_common_pitfalls(page_type, features)
    }
