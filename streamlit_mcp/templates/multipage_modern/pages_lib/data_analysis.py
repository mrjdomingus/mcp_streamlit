"""Data Analysis page - demonstrates caching and state."""

import streamlit as st
import pandas as pd
import numpy as np

# ============================================================================
# CACHED DATA LOADING
# ============================================================================


@st.cache_data
def generate_sample_data(rows: int = 1000):
    """Generate sample data for analysis."""
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=rows, freq="D"),
            "value": np.random.randn(rows).cumsum() + 100,
            "category": np.random.choice(["A", "B", "C", "D"], rows),
            "score": np.random.randint(0, 100, rows),
        }
    )


def show():
    """Display the data analysis page."""
    st.title("📊 Data Analysis")

    st.markdown(
        """
    This page demonstrates:
    - Data loading with caching
    - Filtering and transformations
    - Shared state across pages
    - Data persistence
    """
    )

    # ========================================================================
    # DATA LOADING
    # ========================================================================

    st.subheader("1. Load Data")

    # Option to load data or use existing
    col1, col2 = st.columns([3, 1])

    with col1:
        rows = st.slider("Number of rows", 100, 5000, 1000, step=100)

    with col2:
        if st.button("Load Data", type="primary"):
            # Load and store in session state
            st.session_state.data = generate_sample_data(rows)
            st.session_state.data_loaded = True
            st.success(f"Loaded {rows} rows!")

    # Check if data exists in session state
    if not st.session_state.get("data_loaded", False):
        st.info("👆 Click 'Load Data' to get started")
        st.stop()

    data = st.session_state.data

    # ========================================================================
    # DATA OVERVIEW
    # ========================================================================

    st.subheader("2. Data Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Rows", len(data))

    with col2:
        st.metric("Columns", len(data.columns))

    with col3:
        st.metric("Date Range", f"{(data['date'].max() - data['date'].min()).days} days")

    with col4:
        st.metric("Categories", data["category"].nunique())

    # ========================================================================
    # FILTERING
    # ========================================================================

    st.subheader("3. Filter Data")

    col1, col2 = st.columns(2)

    with col1:
        selected_categories = st.multiselect(
            "Select Categories",
            options=data["category"].unique(),
            default=data["category"].unique(),
        )

    with col2:
        score_range = st.slider(
            "Score Range",
            int(data["score"].min()),
            int(data["score"].max()),
            (int(data["score"].min()), int(data["score"].max())),
        )

    # Apply filters
    filtered_data = data[
        (data["category"].isin(selected_categories))
        & (data["score"] >= score_range[0])
        & (data["score"] <= score_range[1])
    ]

    st.info(
        f"Showing {len(filtered_data):,} of {len(data):,} rows ({len(filtered_data)/len(data)*100:.1f}%)"
    )

    # ========================================================================
    # DATA DISPLAY
    # ========================================================================

    st.subheader("4. View Data")

    tab1, tab2, tab3 = st.tabs(["📋 Data Table", "📊 Statistics", "📁 Download"])

    with tab1:
        st.dataframe(filtered_data, use_container_width=True, hide_index=True)

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Numeric Columns**")
            st.dataframe(filtered_data[["value", "score"]].describe())

        with col2:
            st.markdown("**Category Distribution**")
            st.dataframe(filtered_data["category"].value_counts().to_frame("count"))

    with tab3:
        st.markdown("Download filtered data as CSV")

        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download CSV", data=csv, file_name="filtered_data.csv", mime="text/csv"
        )

    # ========================================================================
    # SAVE FOR OTHER PAGES
    # ========================================================================

    st.divider()

    # Save filtered data to session state for use in other pages
    if st.button("Save filtered data for Visualizations page"):
        st.session_state.filtered_data = filtered_data
        st.success("✅ Data saved! Navigate to Visualizations to see charts.")

    # Show if data is saved
    if "filtered_data" in st.session_state:
        st.info(f"💾 Saved data available ({len(st.session_state.filtered_data)} rows)")
