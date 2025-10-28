"""Settings page - demonstrates state management and configuration."""

import streamlit as st


def show():
    """Display the settings page."""
    st.title("⚙️ Settings")

    st.markdown(
        """
    Configure your preferences. Settings are stored in session state
    and persist across page navigation.
    """
    )

    # ========================================================================
    # INITIALIZE SETTINGS IN SESSION STATE
    # ========================================================================

    if "settings" not in st.session_state:
        st.session_state.settings = {
            "theme": "Light",
            "chart_color": "#636EFA",
            "rows_per_page": 50,
            "show_advanced": False,
            "auto_refresh": False,
            "notifications": True,
        }

    # ========================================================================
    # DISPLAY SETTINGS
    # ========================================================================

    st.subheader("User Preferences")

    # Theme
    theme = st.selectbox(
        "Theme",
        ["Light", "Dark", "Auto"],
        index=["Light", "Dark", "Auto"].index(st.session_state.settings["theme"]),
    )
    st.session_state.settings["theme"] = theme

    # Chart color
    chart_color = st.color_picker(
        "Default Chart Color", value=st.session_state.settings["chart_color"]
    )
    st.session_state.settings["chart_color"] = chart_color

    # Rows per page
    rows_per_page = st.slider(
        "Rows per page in tables",
        min_value=10,
        max_value=200,
        value=st.session_state.settings["rows_per_page"],
        step=10,
    )
    st.session_state.settings["rows_per_page"] = rows_per_page

    st.divider()

    # ========================================================================
    # ADVANCED SETTINGS
    # ========================================================================

    st.subheader("Advanced Options")

    show_advanced = st.checkbox(
        "Show advanced features", value=st.session_state.settings["show_advanced"]
    )
    st.session_state.settings["show_advanced"] = show_advanced

    auto_refresh = st.checkbox(
        "Auto-refresh data (every 5 minutes)", value=st.session_state.settings["auto_refresh"]
    )
    st.session_state.settings["auto_refresh"] = auto_refresh

    notifications = st.checkbox(
        "Enable notifications", value=st.session_state.settings["notifications"]
    )
    st.session_state.settings["notifications"] = notifications

    st.divider()

    # ========================================================================
    # USER INFO
    # ========================================================================

    st.subheader("User Information")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Username", value=st.session_state.get("username", "Guest"), disabled=True)

    with col2:
        st.text_input(
            "Login Status",
            value="Logged In" if st.session_state.get("logged_in") else "Guest",
            disabled=True,
        )

    st.divider()

    # ========================================================================
    # ACTIONS
    # ========================================================================

    st.subheader("Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Save Settings", type="primary", use_container_width=True):
            st.success("✅ Settings saved successfully!")

    with col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.session_state.settings = {
                "theme": "Light",
                "chart_color": "#636EFA",
                "rows_per_page": 50,
                "show_advanced": False,
                "auto_refresh": False,
                "notifications": True,
            }
            st.success("✅ Settings reset to defaults!")
            st.rerun()

    with col3:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            # Clear data but keep auth
            keys_to_keep = ["logged_in", "username", "settings"]
            keys_to_delete = [k for k in st.session_state.keys() if k not in keys_to_keep]
            for key in keys_to_delete:
                del st.session_state[key]
            st.success("✅ Data cleared!")
            st.rerun()

    # ========================================================================
    # CURRENT SETTINGS DISPLAY
    # ========================================================================

    st.divider()
    st.subheader("Current Settings")

    st.json(st.session_state.settings)

    # ========================================================================
    # SESSION STATE DEBUG
    # ========================================================================

    with st.expander("🔍 Debug: All Session State"):
        st.json(dict(st.session_state))

    # ========================================================================
    # TIPS
    # ========================================================================

    st.divider()

    st.markdown(
        """
    ### 💡 Tips

    **Settings Persistence:**
    - Settings are stored in `st.session_state`
    - They persist across page navigation
    - Cleared when you close the browser tab

    **For Production:**
    - Save settings to a database or file
    - Use `st.secrets` for sensitive configuration
    - Implement user-specific settings storage

    **Try it:**
    1. Change some settings here
    2. Navigate to another page
    3. Come back - settings are preserved!
    """
    )
