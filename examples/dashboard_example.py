"""Example dashboard created using Streamlit MCP Server."""

import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto"
)

# Title
st.title("📊 Sales Dashboard")

# Load data (cache for performance)
@st.cache_data
def load_data():
    """Generate example sales data."""
    dates = pd.date_range('2024-01-01', periods=100)
    data = pd.DataFrame({
        'date': dates,
        'sales': np.random.randn(100).cumsum() + 100,
        'customers': np.random.randint(50, 200, 100),
        'category': np.random.choice(['Electronics', 'Clothing', 'Food'], 100)
    })
    return data

data = load_data()

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        f"${data['sales'].sum():.2f}",
        delta="+12%"
    )

with col2:
    st.metric(
        "Avg Customers",
        f"{data['customers'].mean():.0f}",
        delta="+5%"
    )

with col3:
    st.metric(
        "Total Records",
        len(data),
        delta="100"
    )

with col4:
    st.metric(
        "Categories",
        data['category'].nunique(),
        delta="3"
    )

st.divider()

# Charts Section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales Trend")
    st.line_chart(data.set_index('date')['sales'])

with col2:
    st.subheader("Category Distribution")
    category_counts = data['category'].value_counts()
    st.bar_chart(category_counts)

st.divider()

# Filters in Sidebar
st.sidebar.header("Filters")
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=data['category'].unique(),
    default=data['category'].unique()
)

# Filter data
filtered_data = data[data['category'].isin(selected_categories)]

# Data Table
st.subheader("Sales Data")
st.dataframe(
    filtered_data,
    use_container_width=True,
    hide_index=True
)

# Download button
csv = filtered_data.to_csv(index=False)
st.download_button(
    label="Download Data as CSV",
    data=csv,
    file_name="sales_data.csv",
    mime="text/csv"
)

# Footer
st.caption("Dashboard created with Streamlit MCP Server")
