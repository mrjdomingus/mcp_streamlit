# Streamlit Caching Deep Dive

## Overview

Streamlit's caching mechanism solves two critical problems:
1. **Slow Function Reruns**: Avoid re-executing expensive computations on every rerun
2. **Object Recreation**: Prevent recreating heavy objects (models, connections) for each user session

Streamlit provides two caching decorators with different behaviors and use cases.

## The Two Caching Decorators

### @st.cache_data

**Purpose**: Cache computations that return serializable data

**How it works**:
- Creates a **copy** of the cached return value using pickle serialization
- Each function call gets its own copy of the data
- Protects against mutations and race conditions

**When to use**:
- Loading data from CSV, Excel, Parquet files
- Fetching data from APIs
- Querying databases
- Running ML model inference
- Data transformations (pandas, numpy)
- Any function returning serializable data

**Example**:
```python
@st.cache_data
def load_csv():
    return pd.read_csv("data.csv")

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_api():
    response = requests.get("https://api.example.com/data")
    return response.json()

@st.cache_data
def transform_data(df):
    return df.groupby('category').sum()
```

**Key Characteristics**:
- ✅ Thread-safe (each caller gets a copy)
- ✅ Mutation-safe (changes don't affect cached value)
- ⚠️ Serialization overhead (slower for very large datasets)
- ⚠️ Memory usage (copies consume more RAM)

### @st.cache_resource

**Purpose**: Cache global resources like ML models or database connections

**How it works**:
- Stores the **original object** without copying (singleton pattern)
- All function calls share the same object instance
- No serialization overhead

**When to use**:
- Loading ML models (transformers, torch, sklearn)
- Creating database connections
- Opening file handles
- Initializing thread pools
- Any unserializable object

**Example**:
```python
@st.cache_resource
def load_ml_model():
    return transformers.pipeline("sentiment-analysis")

@st.cache_resource
def get_database_connection():
    return SQLAlchemy.create_engine("postgresql://...")

@st.cache_resource
def load_tokenizer():
    return tiktoken.encoding_for_model("gpt-4")
```

**Key Characteristics**:
- ✅ No serialization overhead (very fast)
- ✅ Memory efficient (single instance)
- ✅ Perfect for unserializable objects
- ⚠️ Must ensure thread-safety
- ⚠️ Mutations affect all users

## Decision Matrix

| Scenario | Use This | Why |
|----------|----------|-----|
| Loading CSV/Excel | `@st.cache_data` | Data can be serialized, needs copies |
| API calls | `@st.cache_data` | Serializable data, want fresh copies |
| Database queries | `@st.cache_data` | Serializable results, isolation needed |
| pandas/numpy operations | `@st.cache_data` | Serializable, mutation protection |
| Loading ML models | `@st.cache_resource` | Unserializable, singleton pattern |
| Database connections | `@st.cache_resource` | Unserializable, shared resource |
| File handles | `@st.cache_resource` | Unserializable, shared access |
| Tokenizers | `@st.cache_resource` | Often unserializable, reusable |

## Key Parameters

### ttl (Time To Live)

Automatically invalidate cache after specified seconds.

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_stock_prices():
    return fetch_from_api()

@st.cache_data(ttl=60)  # Cache for 1 minute
def get_real_time_data():
    return requests.get(endpoint).json()
```

**When to use ttl**:
- API calls that return frequently changing data
- Database queries on live data
- Any data that becomes stale

### max_entries

Limit the number of cached entries to control memory usage.

```python
@st.cache_data(max_entries=1000)
def process_user_query(query: str):
    return expensive_computation(query)
```

When the cache exceeds `max_entries`, the oldest entry is removed (LRU strategy).

**When to use max_entries**:
- Functions called with many different parameter combinations
- Memory-constrained environments
- User-specific computations

### show_spinner

Control the loading indicator during cache computation.

```python
@st.cache_data(show_spinner=False)
def silent_load():
    return load_data()

@st.cache_data(show_spinner="Loading data from API...")
def load_with_custom_message():
    return fetch_api()
```

Options:
- `True` (default): Show "Running..."
- `False`: No spinner
- `"Custom message"`: Custom spinner text

### hash_funcs

Provide custom hashing for unhashable parameters.

```python
class MyClass:
    def __init__(self, id):
        self.id = id

@st.cache_data(hash_funcs={MyClass: lambda obj: obj.id})
def process(obj: MyClass):
    return obj.compute()
```

**Common use cases**:
- Custom classes
- Pydantic models
- ML model objects
- Database connections

### Excluding Parameters from Hashing

Prefix parameter names with underscore to exclude from cache key:

```python
@st.cache_data
def query_database(_connection, query: str):
    # _connection is not hashed, query is
    return pd.read_sql(query, _connection)
```

This is useful for:
- Database connections
- File handles
- Configuration objects that don't affect results

## Cache Invalidation

Caches automatically clear when:

1. **Parameter values change**
   ```python
   load_data("file1.csv")  # Cache miss
   load_data("file1.csv")  # Cache hit
   load_data("file2.csv")  # Cache miss (different parameter)
   ```

2. **Function code is modified** (during development)
   - Streamlit detects source code changes
   - Useful for iterative development

3. **TTL expires**
   ```python
   @st.cache_data(ttl=60)
   def get_data():
       return fetch_api()
   # Cache clears after 60 seconds
   ```

4. **max_entries limit reached**
   - Oldest entries are removed (LRU)

## Performance Considerations

### Large Dataset Performance

**Benchmark (100M rows)**:
- First run: ~14 seconds
- Subsequent runs with `@st.cache_data`: ~2 seconds
- Serialization overhead: ~12 seconds

**For datasets > 100M rows**:
```python
# Consider using cache_resource despite mutation risks
@st.cache_resource
def load_huge_dataset():
    return pd.read_parquet("huge_file.parquet")
```

**Trade-off**: No serialization overhead, but mutations affect all users.

### Thread Safety with cache_resource

**Problem**: Multiple users mutating shared objects causes data corruption

**Solution 1**: Use immutable objects
```python
@st.cache_resource
def get_config():
    return FrozenDict(config)  # Immutable
```

**Solution 2**: Use locks for mutations
```python
import threading

lock = threading.Lock()

@st.cache_resource
def get_counter():
    return {"count": 0}

counter = get_counter()
with lock:
    counter["count"] += 1
```

**Solution 3**: Use cache_data instead
```python
@st.cache_data  # Each user gets a copy
def get_mutable_data():
    return {"count": 0}
```

## Advanced Features

### Static Elements in Cached Functions

Streamlit commands inside cached functions are replayed:

```python
@st.cache_data
def load_and_display_data():
    st.write("Loading data...")  # Displayed from cache too!
    data = pd.read_csv("data.csv")
    st.success("Data loaded!")
    return data
```

This enables caching entire UI sections.

### Widgets in Cached Functions (Experimental)

```python
@st.cache_data(experimental_allow_widgets=True)
def get_filtered_data():
    filter_val = st.slider("Filter", 0, 100)  # Widget in cached function!
    return data[data['value'] > filter_val]
```

**Warning**: Can cause excessive memory usage with many widgets.

## Common Patterns

### Pattern 1: API with TTL

```python
@st.cache_data(ttl=300, show_spinner="Fetching latest data...")
def get_live_prices():
    response = requests.get("https://api.example.com/prices")
    return pd.DataFrame(response.json())

data = get_live_prices()
st.dataframe(data)
```

### Pattern 2: ML Model Loading

```python
@st.cache_resource(show_spinner="Loading model...")
def load_model():
    model = transformers.pipeline("text-classification")
    return model

model = load_model()
prediction = model(user_input)
```

### Pattern 3: Database Connection + Query

```python
@st.cache_resource
def get_database():
    return SQLAlchemy.create_engine("postgresql://...")

@st.cache_data(ttl=3600)
def query_data(_engine, query: str):
    return pd.read_sql(query, _engine)

engine = get_database()
data = query_data(engine, "SELECT * FROM sales WHERE date > '2024-01-01'")
```

### Pattern 4: User-Specific Caching

```python
@st.cache_data(max_entries=100)
def get_user_data(user_id: str):
    # Each user_id creates a separate cache entry
    return fetch_user_specific_data(user_id)

user_id = st.text_input("User ID")
if user_id:
    data = get_user_data(user_id)
```

## Migration from Deprecated st.cache

The old `st.cache` decorator is deprecated. Migration checklist:

**Old code**:
```python
@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_data():
    return pd.read_csv("data.csv")
```

**New code**:
```python
@st.cache_data  # or @st.cache_resource
def load_data():
    return pd.read_csv("data.csv")
```

**Changes**:
1. Remove `allow_output_mutation` parameter
2. Remove `suppress_st_warning` parameter
3. Choose `cache_data` (for most cases) or `cache_resource` (for models/connections)

## Best Practices

1. **Start with @st.cache_data** - It's safer due to copying behavior
2. **Use @st.cache_resource only when necessary** - For unserializable objects or performance-critical cases
3. **Set appropriate ttl** - Prevent stale data from APIs/databases
4. **Use max_entries for user queries** - Prevent unbounded memory growth
5. **Prefix unchanging parameters with `_`** - Optimize cache key computation
6. **Be cautious with cache_resource mutations** - Ensure thread safety
7. **Use custom hash_funcs** - For complex objects that need special hashing
8. **Monitor cache size** - Check memory usage in production

## Debugging Caches

### Clear all caches
```python
st.cache_data.clear()  # Clear all @st.cache_data caches
st.cache_resource.clear()  # Clear all @st.cache_resource caches
```

### Clear specific cache
```python
load_data.clear()  # Clear cache for specific function
```

### Check if cache is working
Add print statements to see when function executes:
```python
@st.cache_data
def load_data():
    print("Loading data...")  # Will print only on cache miss
    return pd.read_csv("data.csv")
```

---

## Quick Reference Card

| Need | Decorator | Key Parameter |
|------|-----------|---------------|
| Cache CSV loading | `@st.cache_data` | - |
| Cache API calls | `@st.cache_data` | `ttl=seconds` |
| Cache DB queries | `@st.cache_data` | `ttl=seconds` |
| Cache transformations | `@st.cache_data` | - |
| Load ML model | `@st.cache_resource` | - |
| DB connection | `@st.cache_resource` | - |
| Limit memory | Either | `max_entries=N` |
| Custom message | Either | `show_spinner="..."` |
| Unhashable params | Either | `hash_funcs={Type: func}` |
| Exclude param | Either | Prefix with `_` |

**Remember**: When in doubt, use `@st.cache_data` - it's the safer default!
