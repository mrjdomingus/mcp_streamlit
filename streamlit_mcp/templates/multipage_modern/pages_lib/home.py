"""Home page for multi-page app."""

import streamlit as st


def show():
    """Display the home page."""
    st.title("🏠 Welcome to the Multi-Page App")

    st.markdown(
        """
    This is a modern Streamlit multi-page application using **st.navigation()**.

    ### Features

    - ✅ Modern `st.navigation()` API (not pages/ folder)
    - ✅ Conditional navigation based on authentication
    - ✅ Grouped pages in sidebar
    - ✅ Shared session state across pages
    - ✅ Clean page function architecture

    ### Navigation

    Use the sidebar to navigate between pages:

    **Home**
    - Welcome (this page)

    **Data**
    - Data Analysis - Load and analyze data
    - Visualizations - Create charts and graphs

    **Settings**
    - Preferences - Configure app settings

    ### Getting Started

    Try navigating to the **Data Analysis** page to load some sample data!
    """
    )

    # Example: Shared state across pages
    if "visit_count" not in st.session_state:
        st.session_state.visit_count = 0

    st.session_state.visit_count += 1

    st.info(f"📊 You've visited this page {st.session_state.visit_count} times")

    # Quick stats
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Pages", "4", help="Total pages in this app")

    with col2:
        st.metric("Groups", "3", help="Navigation groups")

    with col3:
        st.metric("User", st.session_state.get("username", "Guest"))

    # Show session state (helpful for debugging)
    with st.expander("🔍 Session State (for debugging)"):
        st.json(dict(st.session_state))
