"""
Modern Multi-Page Streamlit App using st.navigation()
======================================================

This template demonstrates the modern approach to multi-page apps:
- Uses st.navigation() and st.Page() (NOT pages/ folder)
- Page functions in separate modules
- Conditional navigation based on auth
- Proper caching and state management
"""

import streamlit as st
from pages_lib import home, data_analysis, visualizations, settings

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Multi-Page App",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# AUTHENTICATION (Optional - can be removed)
# ============================================================================

# Initialize auth state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

def login(username: str, password: str) -> bool:
    """Simple auth - replace with real authentication."""
    # For demo: any username/password works
    # In production, use st.login() or your own auth system
    return username and password

def logout():
    """Clear authentication state."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

# ============================================================================
# LOGIN PAGE (shown when not authenticated)
# ============================================================================

def show_login():
    st.title("🔐 Login")
    st.markdown("Enter any username and password to continue (demo mode)")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# ============================================================================
# NAVIGATION SETUP
# ============================================================================

if not st.session_state.logged_in:
    # Not logged in - show only login page
    show_login()
else:
    # Logged in - show full app navigation

    # Define pages using st.Page() with functions from page modules
    pages = {
        "Home": [
            st.Page(home.show, title="Welcome", icon="🏠", default=True)
        ],
        "Data": [
            st.Page(data_analysis.show, title="Data Analysis", icon="📊"),
            st.Page(visualizations.show, title="Visualizations", icon="📈")
        ],
        "Settings": [
            st.Page(settings.show, title="Preferences", icon="⚙️")
        ]
    }

    # Create navigation
    pg = st.navigation(pages, position="sidebar")

    # Add logout button to sidebar
    with st.sidebar:
        st.divider()
        st.write(f"👤 {st.session_state.username}")
        if st.button("Logout", use_container_width=True):
            logout()

    # Run the selected page
    pg.run()

# ============================================================================
# NOTES ON THIS ARCHITECTURE
# ============================================================================

"""
KEY FEATURES:

1. Modern st.navigation() API:
   - No pages/ folder needed
   - More flexible than file-based routing
   - Conditional navigation support
   - Grouped pages

2. Page Functions:
   - Each page is a function in pages_lib/
   - Clean separation of concerns
   - Easy to test
   - Reusable across multiple nav schemes

3. Authentication Integration:
   - Conditional navigation based on login state
   - Can easily adapt to st.login() when stable
   - Logout functionality in sidebar

4. Grouped Navigation:
   - Pages organized into logical sections
   - "Home", "Data", "Settings" groups
   - Clean sidebar organization

5. State Management:
   - Session state for auth
   - State persists across page switches
   - Shared state accessible in all pages

ADVANTAGES OVER pages/ FOLDER:

✓ More control over navigation
✓ Conditional pages (auth, permissions)
✓ Dynamic page generation
✓ Grouped navigation
✓ Easier testing (functions vs files)
✓ Better IDE support

MIGRATION FROM pages/:

OLD (pages/ folder):
pages/
  home.py
  data.py
  viz.py

NEW (st.navigation()):
pages_lib/
  home.py      -> def show(): ...
  data.py      -> def show(): ...
  viz.py       -> def show(): ...
app.py         -> st.navigation(pages)
"""
