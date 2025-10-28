"""
Simple Streamlit App Example
Generated using the Streamlit MCP Server

This example shows a basic dashboard with metrics and charts.
"""

import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Simple Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Simple Dashboard")
st.markdown("*Example generated with Streamlit MCP Server*")

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Sales",
        value="$45,231",
        delta="+12.5%"
    )

with col2:
    st.metric(
        label="Revenue",
        value="$89,432",
        delta="+8.2%"
    )

with col3:
    st.metric(
        label="Customers",
        value="1,234",
        delta="+5.1%"
    )

with col4:
    st.metric(
        label="Orders",
        value="567",
        delta="-2.3%"
    )

st.divider()

# Charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Sales Trend")

    # Generate sample data
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    sales_data = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.randint(1000, 5000, size=30).cumsum() / 100
    })

    st.line_chart(sales_data, x='Date', y='Sales')

with chart_col2:
    st.subheader("Category Distribution")

    # Generate sample data
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Sports']
    values = np.random.randint(100, 1000, size=5)

    category_data = pd.DataFrame({
        'Category': categories,
        'Sales': values
    })

    st.bar_chart(category_data, x='Category', y='Sales')

st.divider()

# Data table
st.subheader("Recent Transactions")

# Generate sample data
transactions_data = pd.DataFrame({
    'Date': pd.date_range(start='2024-01-28', periods=10, freq='H'),
    'Product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Headphones'], 10),
    'Amount': np.random.randint(50, 1500, 10),
    'Status': np.random.choice(['Completed', 'Pending', 'Cancelled'], 10)
})

st.dataframe(
    transactions_data,
    use_container_width=True,
    hide_index=True
)

# Footer
st.markdown("---")
st.caption("Built with Streamlit MCP Server | Data is randomly generated for demo purposes")
