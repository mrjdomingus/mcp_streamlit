"""Visualizations page - demonstrates charts and session state sharing."""

import streamlit as st
import plotly.express as px

def show():
    """Display the visualizations page."""
    st.title("📈 Visualizations")

    st.markdown("""
    This page demonstrates:
    - Accessing data from other pages via session state
    - Creating interactive charts
    - Multiple visualization types
    """)

    # Check if data exists from Data Analysis page
    if "filtered_data" not in st.session_state:
        st.warning("⚠️ No data available. Please go to **Data Analysis** page and load data first.")
        if st.button("Go to Data Analysis"):
            st.switch_page("pages_lib/data_analysis.py")
        st.stop()

    data = st.session_state.filtered_data

    st.success(f"✅ Using data from Data Analysis ({len(data)} rows)")

    # ========================================================================
    # CHART SELECTION
    # ========================================================================

    st.subheader("Chart Options")

    col1, col2 = st.columns([2, 1])

    with col1:
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Time Series", "Category Distribution", "Score Distribution", "Scatter Plot"]
        )

    with col2:
        use_container_width = st.checkbox("Use full width", value=True)

    st.divider()

    # ========================================================================
    # CHARTS
    # ========================================================================

    if chart_type == "Time Series":
        st.subheader("📊 Time Series - Value Over Time")

        # Aggregate by date
        daily_data = data.groupby('date')['value'].mean().reset_index()

        fig = px.line(
            daily_data,
            x='date',
            y='value',
            title='Average Value Over Time'
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Value",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=use_container_width)

        # Additional stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Min Value", f"{data['value'].min():.2f}")
        with col2:
            st.metric("Max Value", f"{data['value'].max():.2f}")
        with col3:
            st.metric("Avg Value", f"{data['value'].mean():.2f}")

    elif chart_type == "Category Distribution":
        st.subheader("📊 Category Distribution")

        category_counts = data['category'].value_counts().reset_index()
        category_counts.columns = ['category', 'count']

        fig = px.bar(
            category_counts,
            x='category',
            y='count',
            title='Count by Category',
            color='count',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            xaxis_title="Category",
            yaxis_title="Count"
        )
        st.plotly_chart(fig, use_container_width=use_container_width)

        # Pie chart alternative
        st.markdown("**Pie Chart View**")
        fig_pie = px.pie(
            category_counts,
            values='count',
            names='category',
            title='Category Distribution'
        )
        st.plotly_chart(fig_pie, use_container_width=use_container_width)

    elif chart_type == "Score Distribution":
        st.subheader("📊 Score Distribution")

        fig = px.histogram(
            data,
            x='score',
            nbins=20,
            title='Score Distribution',
            color_discrete_sequence=['#636EFA']
        )
        fig.update_layout(
            xaxis_title="Score",
            yaxis_title="Frequency"
        )
        st.plotly_chart(fig, use_container_width=use_container_width)

        # Box plot by category
        st.markdown("**Score Distribution by Category**")
        fig_box = px.box(
            data,
            x='category',
            y='score',
            title='Score Distribution by Category',
            color='category'
        )
        st.plotly_chart(fig_box, use_container_width=use_container_width)

    elif chart_type == "Scatter Plot":
        st.subheader("📊 Scatter Plot - Value vs Score")

        fig = px.scatter(
            data,
            x='value',
            y='score',
            color='category',
            title='Value vs Score by Category',
            trendline='ols'
        )
        fig.update_layout(
            xaxis_title="Value",
            yaxis_title="Score"
        )
        st.plotly_chart(fig, use_container_width=use_container_width)

    # ========================================================================
    # MULTIPLE CHARTS VIEW
    # ========================================================================

    st.divider()
    st.subheader("📊 Multi-Chart Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Time Series**")
        daily_data = data.groupby('date')['value'].mean().reset_index()
        fig1 = px.line(daily_data, x='date', y='value', height=300)
        fig1.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("**Category Pie Chart**")
        category_counts = data['category'].value_counts().reset_index()
        category_counts.columns = ['category', 'count']
        fig2 = px.pie(category_counts, values='count', names='category', height=300)
        fig2.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    # ========================================================================
    # EXPORT
    # ========================================================================

    st.divider()

    if st.button("📊 Generate Report Summary"):
        st.markdown("### 📄 Data Summary Report")

        st.markdown(f"""
        **Report Generated:** {st.session_state.get('username', 'User')}

        **Data Overview:**
        - Total Records: {len(data):,}
        - Date Range: {data['date'].min().strftime('%Y-%m-%d')} to {data['date'].max().strftime('%Y-%m-%d')}
        - Categories: {', '.join(data['category'].unique())}

        **Statistics:**
        - Average Value: {data['value'].mean():.2f}
        - Average Score: {data['score'].mean():.2f}
        - Value Range: {data['value'].min():.2f} to {data['value'].max():.2f}
        """)

        st.success("✅ Report generated!")
