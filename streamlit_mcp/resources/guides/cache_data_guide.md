# st.cache_data - Complete Guide

## What is st.cache_data?

`@st.cache_data` is the recommended decorator for caching computations that return **serializable data** (dataframes, lists, dicts, strings, numbers, etc.).

**Key Feature**: Creates a **copy** of the cached value for each caller using pickle serialization.

## When to Use

✅ **Perfect for**:
- Loading data from files (CSV, Excel, Parquet, JSON)
- Fetching data from APIs
- Querying databases
- Running ML model inference (predictions)
- Data transformations (pandas, numpy operations)
- Computing statistics or aggregations

❌ **Not recommended for**:
- ML models themselves → use `@st.cache_resource`
- Database connections → use `@st.cache_resource`
- File handles → use `@st.cache_resource`
- Very large datasets (>100M rows) → consider `@st.cache_resource`

## Basic Usage

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # This expensive operation runs only once
    return pd.read_csv("large_dataset.csv")

# First call: loads from CSV
data = load_data()

# Subsequent calls: returns cached copy instantly
data = load_data()
```

## How It Works

### The Copying Behavior

```python
@st.cache_data
def get_list():
    return [1, 2, 3]

# User 1
list1 = get_list()
list1.append(4)  # Modifies their copy
print(list1)  # [1, 2, 3, 4]

# User 2 (concurrent session)
list2 = get_list()
print(list2)  # [1, 2, 3] - Not affected by User 1's changes!
```

**Why copying is important**:
- Protects against mutations
- Thread-safe for concurrent users
- Each session gets isolated data

## Parameters

### 1. ttl (Time To Live)

Cache expires after specified seconds.

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_stock_prices():
    return requests.get("https://api.stocks.com/prices").json()
```

**Use cases**:
- APIs that return frequently updated data
- Live database queries
- Real-time feeds
- Weather data
- Stock prices
- Social media feeds

```python
# Different TTL examples
@st.cache_data(ttl=60)       # 1 minute - very fresh data
@st.cache_data(ttl=300)      # 5 minutes - recent data
@st.cache_data(ttl=3600)     # 1 hour - moderately fresh
@st.cache_data(ttl=86400)    # 24 hours - daily refresh
```

### 2. max_entries

Limit number of cached entries (LRU eviction).

```python
@st.cache_data(max_entries=1000)
def search_products(query: str):
    return expensive_search(query)
```

**Use cases**:
- Functions with many different parameter combinations
- User-specific queries
- Search functionality
- Memory-constrained environments

```python
# Without max_entries (risky!)
@st.cache_data
def user_query(user_id: str, query: str):
    # Could create unlimited cache entries!
    return process(user_id, query)

# With max_entries (safe)
@st.cache_data(max_entries=500)
def user_query(user_id: str, query: str):
    # Only keeps 500 most recent queries
    return process(user_id, query)
```

### 3. show_spinner

Control loading indicator.

```python
# Default spinner
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")  # Shows "Running..."

# No spinner
@st.cache_data(show_spinner=False)
def silent_load():
    return pd.read_csv("data.csv")

# Custom message
@st.cache_data(show_spinner="Loading data from database...")
def load_from_db():
    return query_database()
```

### 4. hash_funcs

Custom hashing for unhashable types.

```python
from pydantic import BaseModel

class Config(BaseModel):
    api_key: str
    endpoint: str

@st.cache_data(hash_funcs={Config: lambda c: c.model_dump_json()})
def fetch_data(config: Config):
    return requests.get(config.endpoint, headers={"key": config.api_key}).json()
```

**Common unhashable types needing hash_funcs**:
- Custom classes
- Pydantic models
- Dataclasses (sometimes)
- Complex nested structures

### 5. persist

Save cache to disk (experimental).

```python
@st.cache_data(persist="disk")
def expensive_computation():
    # Survives app restarts!
    return long_running_task()
```

## Parameter Exclusion with Underscore

Exclude parameters from cache key by prefixing with `_`:

```python
import sqlalchemy

@st.cache_data
def query_data(_engine, query: str):
    # _engine is NOT part of cache key
    # Only query affects caching
    return pd.read_sql(query, _engine)

engine = sqlalchemy.create_engine("postgresql://...")
data1 = query_data(engine, "SELECT * FROM users")  # Cache miss
data2 = query_data(engine, "SELECT * FROM users")  # Cache hit
```

**When to use `_` prefix**:
- Database connections
- File handles
- API clients
- Configuration objects that don't affect results

## Common Patterns

### Pattern 1: CSV/Excel Loading

```python
@st.cache_data
def load_csv(file_path: str):
    return pd.read_csv(file_path)

@st.cache_data
def load_excel(file_path: str, sheet: str):
    return pd.read_excel(file_path, sheet_name=sheet)

# Usage
sales_data = load_csv("data/sales.csv")
inventory = load_excel("data/inventory.xlsx", "Sheet1")
```

### Pattern 2: API Calls with TTL

```python
@st.cache_data(ttl=300, show_spinner="Fetching latest data...")
def get_weather(city: str):
    response = requests.get(f"https://api.weather.com/{city}")
    return response.json()

@st.cache_data(ttl=60)
def get_crypto_prices():
    return requests.get("https://api.crypto.com/prices").json()

# Cache refreshes every 5 minutes
weather = get_weather("New York")

# Cache refreshes every minute
prices = get_crypto_prices()
```

### Pattern 3: Database Queries

```python
@st.cache_data(ttl=3600)
def query_sales(_connection, start_date: str, end_date: str):
    query = f"""
        SELECT * FROM sales
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
    """
    return pd.read_sql(query, _connection)

# Connection is excluded from cache key
conn = get_database_connection()
data = query_sales(conn, "2024-01-01", "2024-12-31")
```

### Pattern 4: Data Transformations

```python
@st.cache_data
def clean_data(df: pd.DataFrame):
    df = df.dropna()
    df = df.drop_duplicates()
    return df

@st.cache_data
def aggregate_by_category(df: pd.DataFrame, category_col: str):
    return df.groupby(category_col).agg({
        'sales': 'sum',
        'quantity': 'sum'
    })

# Chain transformations
raw_data = load_csv("sales.csv")
clean = clean_data(raw_data)
aggregated = aggregate_by_category(clean, "product_category")
```

### Pattern 5: User-Specific Data

```python
@st.cache_data(max_entries=200)
def get_user_dashboard(user_id: str):
    # Each user gets their own cache entry
    # Keep only 200 most recent users in cache
    return fetch_user_data(user_id)

user = st.text_input("User ID")
if user:
    dashboard_data = get_user_dashboard(user)
    st.dataframe(dashboard_data)
```

### Pattern 6: File Upload Processing

```python
@st.cache_data
def process_uploaded_file(file_contents: bytes, file_name: str):
    # Cache expensive processing
    df = pd.read_csv(BytesIO(file_contents))
    return perform_analysis(df)

uploaded_file = st.file_uploader("Upload CSV")
if uploaded_file:
    # Reprocessing is cached based on file contents
    contents = uploaded_file.read()
    results = process_uploaded_file(contents, uploaded_file.name)
    st.write(results)
```

## Cache Invalidation Strategies

### Manual Clearing

```python
# Clear all @st.cache_data caches
if st.button("Clear all caches"):
    st.cache_data.clear()
    st.success("Cache cleared!")

# Clear specific function cache
if st.button("Reload data"):
    load_data.clear()
    st.rerun()
```

### Automatic with TTL

```python
@st.cache_data(ttl=3600)  # Auto-clear after 1 hour
def get_fresh_data():
    return fetch_api()
```

### Parameter-Based

```python
@st.cache_data
def load_data(version: str):
    return pd.read_csv(f"data_v{version}.csv")

# Change version to invalidate cache
version = st.selectbox("Data version", ["1", "2", "3"])
data = load_data(version)  # Different version = cache miss
```

## Performance Optimization

### Serialization Overhead

```python
# For small/medium datasets (< 100M rows)
@st.cache_data  # Recommended - safe and fast enough
def load_medium_data():
    return pd.read_parquet("medium.parquet")

# For huge datasets (> 100M rows)
@st.cache_resource  # Faster but risky (no copying)
def load_huge_data():
    return pd.read_parquet("huge.parquet")
```

**Benchmark (100M rows)**:
- First load: ~14 seconds
- Cached with `@st.cache_data`: ~2 seconds (12s serialization overhead)
- Cached with `@st.cache_resource`: <0.1 seconds (no overhead)

### Chunking Large Operations

```python
@st.cache_data
def load_data_chunk(chunk_id: int):
    # Cache smaller chunks separately
    return pd.read_parquet(f"data_chunk_{chunk_id}.parquet")

# Load in parallel, each chunk cached independently
all_chunks = [load_data_chunk(i) for i in range(10)]
full_data = pd.concat(all_chunks)
```

## Debugging

### Add Logging

```python
@st.cache_data
def load_data():
    st.write("⚡ Cache miss - loading data...")  # Only shown on cache miss
    data = pd.read_csv("data.csv")
    st.success("✅ Data loaded!")
    return data
```

### Inspect Cache Behavior

```python
import time

@st.cache_data
def timed_load():
    start = time.time()
    st.write(f"Loading at {start}")  # Check if this prints (cache miss)
    data = pd.read_csv("data.csv")
    elapsed = time.time() - start
    st.write(f"Took {elapsed:.2f}s")
    return data
```

## Common Mistakes

### ❌ Mistake 1: Not using cache for expensive operations

```python
# Bad - loads every rerun!
data = pd.read_csv("huge_file.csv")
st.dataframe(data)

# Good - loads once, cached
@st.cache_data
def load_data():
    return pd.read_csv("huge_file.csv")

data = load_data()
st.dataframe(data)
```

### ❌ Mistake 2: Mutating cached data without copying

```python
@st.cache_data
def get_data():
    return pd.DataFrame({"a": [1, 2, 3]})

data = get_data()
data["b"] = [4, 5, 6]  # This is fine with cache_data (you get a copy)

# But be aware: changes don't persist to cache
data2 = get_data()  # New copy, doesn't have column "b"
```

### ❌ Mistake 3: Using cache_data for models

```python
# Bad - models may not serialize well
@st.cache_data
def load_model():
    return transformers.pipeline("sentiment-analysis")

# Good - use cache_resource for models
@st.cache_resource
def load_model():
    return transformers.pipeline("sentiment-analysis")
```

### ❌ Mistake 4: Forgetting TTL for live data

```python
# Bad - stale data!
@st.cache_data
def get_stock_price():
    return requests.get("https://api.stocks.com/AAPL").json()

# Good - fresh data
@st.cache_data(ttl=60)  # Refresh every minute
def get_stock_price():
    return requests.get("https://api.stocks.com/AAPL").json()
```

## Best Practices Summary

1. ✅ Use `@st.cache_data` as your default caching decorator
2. ✅ Set `ttl` for data that changes over time
3. ✅ Set `max_entries` for functions with varying parameters
4. ✅ Prefix unchanging parameters with `_`
5. ✅ Use clear `show_spinner` messages for better UX
6. ✅ Test cache behavior during development
7. ✅ Monitor memory usage in production
8. ❌ Don't use for ML models (use `@st.cache_resource`)
9. ❌ Don't forget TTL for live/API data
10. ❌ Don't cache functions with side effects

---

## Quick Examples Cheat Sheet

```python
# Basic caching
@st.cache_data
def load_csv():
    return pd.read_csv("data.csv")

# With TTL (expires)
@st.cache_data(ttl=3600)
def fetch_api():
    return requests.get(url).json()

# With max entries (memory limit)
@st.cache_data(max_entries=100)
def user_search(query: str):
    return search(query)

# Custom spinner
@st.cache_data(show_spinner="Processing...")
def process():
    return heavy_computation()

# Exclude parameter
@st.cache_data
def query(_conn, sql: str):
    return pd.read_sql(sql, _conn)

# Custom hashing
@st.cache_data(hash_funcs={MyClass: lambda x: x.id})
def process(obj: MyClass):
    return obj.compute()
```
