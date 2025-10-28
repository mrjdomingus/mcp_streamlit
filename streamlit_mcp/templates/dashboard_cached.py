"""
Streamlit Dashboard Template with Caching Best Practices
==========================================================

This template demonstrates:
- @st.cache_data for data loading
- Proper use of TTL for fresh data
- Metrics, charts, and filters
- Efficient rerun handling
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DATA LOADING (WITH CACHING)
# ============================================================================

@st.cache_data(ttl=3600, show_spinner="Loading sales data...")
def load_sales_data():
    """
    Load sales data from source.
    Cached for 1 hour to balance freshness and performance.

    Replace this with your actual data source:
    - pd.read_csv("data/sales.csv")
    - pd.read_sql(query, connection)
    - requests.get("https://api.example.com/sales").json()
    """
    # Generate sample data for demonstration
    dates = pd.date_range(end=datetime.now(), periods=365, freq='D')
    data = pd.DataFrame({
        'date': dates,
        'sales': np.random.randint(1000, 5000, 365) + np.random.randn(365).cumsum() * 100,
        'customers': np.random.randint(50, 200, 365),
        'orders': np.random.randint(100, 400, 365),
        'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], 365),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 365)
    })
    return data

@st.cache_data(ttl=600)
def calculate_metrics(df):
    """
    Calculate key metrics from data.
    Cached for 10 minutes.
    """
    total_sales = df['sales'].sum()
    total_customers = df['customers'].sum()
    total_orders = df['orders'].sum()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0

    # Calculate period-over-period changes
    last_30_days = df[df['date'] >= (df['date'].max() - timedelta(days=30))]
    prev_30_days = df[(df['date'] >= (df['date'].max() - timedelta(days=60))) &
                      (df['date'] < (df['date'].max() - timedelta(days=30)))]

    sales_change = ((last_30_days['sales'].sum() - prev_30_days['sales'].sum()) /
                    prev_30_days['sales'].sum() * 100) if prev_30_days['sales'].sum() > 0 else 0

    return {
        'total_sales': total_sales,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'sales_change': sales_change
    }

# ============================================================================
# MAIN APP
# ============================================================================

st.title("📊 Sales Dashboard")
st.markdown("Real-time sales analytics with intelligent caching")

# Load data (runs once per hour due to caching)
data = load_sales_data()

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================

st.sidebar.header("Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Date Range",
    value=(data['date'].min(), data['date'].max()),
    min_value=data['date'].min(),
    max_value=data['date'].max()
)

# Category filter
categories = st.sidebar.multiselect(
    "Categories",
    options=data['category'].unique(),
    default=data['category'].unique()
)

# Region filter
regions = st.sidebar.multiselect(
    "Regions",
    options=data['region'].unique(),
    default=data['region'].unique()
)

# Apply filters (fast, no caching needed for simple filtering)
filtered_data = data[
    (data['date'] >= pd.to_datetime(date_range[0])) &
    (data['date'] <= pd.to_datetime(date_range[1])) &
    (data['category'].isin(categories)) &
    (data['region'].isin(regions))
]

if filtered_data.empty:
    st.warning("No data matches the selected filters. Please adjust your selection.")
    st.stop()

# ============================================================================
# KEY METRICS
# ============================================================================

metrics = calculate_metrics(filtered_data)

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        f"${metrics['total_sales']:,.0f}",
        delta=f"{metrics['sales_change']:+.1f}%",
        help="Total sales for the selected period"
    )

with col2:
    st.metric(
        "Total Customers",
        f"{metrics['total_customers']:,.0f}",
        help="Number of customers served"
    )

with col3:
    st.metric(
        "Total Orders",
        f"{metrics['total_orders']:,.0f}",
        help="Number of orders placed"
    )

with col4:
    st.metric(
        "Avg Order Value",
        f"${metrics['avg_order_value']:,.2f}",
        help="Average value per order"
    )

st.divider()

# ============================================================================
# CHARTS
# ============================================================================

st.subheader("Sales Analytics")

# Row 1: Time series and category breakdown
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Sales Trend")

    # Aggregate by date
    daily_sales = filtered_data.groupby('date')['sales'].sum().reset_index()

    fig_trend = px.line(
        daily_sales,
        x='date',
        y='sales',
        title='Daily Sales Over Time'
    )
    fig_trend.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        hovermode='x unified'
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.markdown("### Sales by Category")

    category_sales = filtered_data.groupby('category')['sales'].sum().reset_index()

    fig_category = px.pie(
        category_sales,
        values='sales',
        names='category',
        title='Sales Distribution by Category'
    )
    st.plotly_chart(fig_category, use_container_width=True)

# Row 2: Regional analysis and orders
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Sales by Region")

    region_sales = filtered_data.groupby('region')['sales'].sum().reset_index().sort_values('sales', ascending=True)

    fig_region = px.bar(
        region_sales,
        y='region',
        x='sales',
        orientation='h',
        title='Regional Sales Performance'
    )
    fig_region.update_layout(
        xaxis_title="Sales ($)",
        yaxis_title="Region"
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    st.markdown("### Orders vs Customers")

    daily_agg = filtered_data.groupby('date').agg({
        'orders': 'sum',
        'customers': 'sum'
    }).reset_index()

    fig_orders = px.scatter(
        daily_agg,
        x='customers',
        y='orders',
        title='Orders vs Customers Correlation',
        trendline='ols'
    )
    fig_orders.update_layout(
        xaxis_title="Customers",
        yaxis_title="Orders"
    )
    st.plotly_chart(fig_orders, use_container_width=True)

st.divider()

# ============================================================================
# DATA TABLE
# ============================================================================

st.subheader("Detailed Data")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📋 Raw Data", "📊 Summary Statistics", "📈 Top Performers"])

with tab1:
    st.dataframe(
        filtered_data.sort_values('date', ascending=False),
        use_container_width=True,
        hide_index=True
    )

    # Download button
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with tab2:
    st.markdown("### Summary Statistics")
    st.dataframe(
        filtered_data[['sales', 'customers', 'orders']].describe(),
        use_container_width=True
    )

with tab3:
    st.markdown("### Top 10 Days by Sales")
    top_days = filtered_data.nlargest(10, 'sales')[['date', 'sales', 'customers', 'orders', 'category', 'region']]
    st.dataframe(top_days, use_container_width=True, hide_index=True)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data cached for 1 hour")

# ============================================================================
# PERFORMANCE NOTES
# ============================================================================

"""
CACHING STRATEGY USED:

1. @st.cache_data(ttl=3600) for load_sales_data():
   - Caches data for 1 hour
   - Balances freshness vs performance
   - Adjust TTL based on how often your data changes

2. @st.cache_data(ttl=600) for calculate_metrics():
   - Caches metrics for 10 minutes
   - Faster refresh than raw data
   - Recalculates when filters change (different input = cache miss)

3. No caching for filtering:
   - Filtering is fast enough without caching
   - Allows immediate response to filter changes

4. Plotly charts are rendered on every rerun:
   - Chart generation is fast with Plotly
   - Could cache if charts become slow

PERFORMANCE TIPS:

- If data loading is very slow, increase TTL
- If data changes frequently, decrease TTL
- Use st.fragment() for auto-refreshing sections
- Consider pagination for very large datasets
- Use column_config for advanced dataframe formatting
"""
