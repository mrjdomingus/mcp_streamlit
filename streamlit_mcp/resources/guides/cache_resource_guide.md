# st.cache_resource - Complete Guide

## What is st.cache_resource?

`@st.cache_resource` is the decorator for caching **global resources** like ML models, database connections, or any unserializable objects.

**Key Feature**: Stores the **original object** without copying (singleton pattern). All users share the same instance.

## When to Use

✅ **Perfect for**:
- ML models (transformers, torch, sklearn, tensorflow)
- Database connections (SQLAlchemy, pymongo, psycopg2)
- Tokenizers (tiktoken, sentencepiece)
- API clients (initialized with credentials)
- File handles
- Thread pools
- WebSocket connections
- Any unserializable object

❌ **Not recommended for**:
- Data (DataFrames, lists, dicts) → use `@st.cache_data`
- API responses → use `@st.cache_data`
- Database query results → use `@st.cache_data`

## Basic Usage

```python
import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_model():
    # This expensive operation runs only once across ALL users
    return pipeline("sentiment-analysis")

# First user/call: loads model
model = load_model()

# All subsequent users/calls: get the SAME model instance
model = load_model()

# Use the model
prediction = model("I love Streamlit!")
```

## How It Works

### The Singleton Behavior

```python
@st.cache_resource
def get_counter():
    return {"count": 0}

# User 1
counter1 = get_counter()
counter1["count"] += 1
print(counter1)  # {"count": 1}

# User 2 (concurrent session)
counter2 = get_counter()
print(counter2)  # {"count": 1} - SAME object as User 1!

# Both users share the same object!
print(counter1 is counter2)  # True
```

**Why singleton is important**:
- No serialization overhead (very fast)
- Memory efficient (one instance for all users)
- Perfect for heavy objects like ML models

**⚠️ Warning: Shared mutations**:
- Changes by one user affect all users
- Requires thread safety for mutable objects

## Parameters

### 1. ttl (Time To Live)

Cache expires after specified seconds.

```python
@st.cache_resource(ttl=3600)  # Reload model every hour
def load_model():
    return pipeline("sentiment-analysis")
```

**Use cases**:
- Periodically refresh database connections
- Reload updated models
- Refresh API clients with rotated credentials

**Note**: Usually not needed for resources. Models and connections typically don't need TTL.

### 2. max_entries

Limit number of cached resources (LRU eviction).

```python
@st.cache_resource(max_entries=5)
def load_model(model_name: str):
    # Keep only 5 models in memory
    return pipeline(model_name)
```

**Use cases**:
- Multiple model variants
- Different database connections
- Memory-constrained environments

### 3. show_spinner

Control loading indicator.

```python
@st.cache_resource(show_spinner="Loading model... (this may take a minute)")
def load_large_model():
    return transformers.AutoModel.from_pretrained("large-model")

@st.cache_resource(show_spinner=False)
def get_db():
    return SQLAlchemy.create_engine("postgresql://...")
```

### 4. hash_funcs

Custom hashing for unhashable parameters (rarely needed).

```python
@st.cache_resource(hash_funcs={torch.device: lambda d: str(d)})
def load_model(device: torch.device):
    model = MyModel()
    model.to(device)
    return model
```

## Parameter Exclusion with Underscore

Like `@st.cache_data`, prefix with `_` to exclude from cache key:

```python
@st.cache_resource
def initialize_client(_config_dict):
    # _config_dict not hashed
    return APIClient(config_dict)
```

## Common Patterns

### Pattern 1: ML Model Loading

```python
@st.cache_resource(show_spinner="Loading sentiment model...")
def load_sentiment_model():
    return pipeline("sentiment-analysis")

@st.cache_resource(show_spinner="Loading GPT-2 model...")
def load_gpt2():
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    return model, tokenizer

# Usage
sentiment_model = load_sentiment_model()
result = sentiment_model("Streamlit is amazing!")

gpt2_model, gpt2_tokenizer = load_gpt2()
```

### Pattern 2: Database Connections

```python
@st.cache_resource
def get_database_engine():
    from sqlalchemy import create_engine
    return create_engine("postgresql://user:pass@localhost/db")

@st.cache_resource
def get_mongo_client():
    from pymongo import MongoClient
    return MongoClient("mongodb://localhost:27017/")

# Usage
engine = get_database_engine()

# For queries, use @st.cache_data
@st.cache_data(ttl=3600)
def query_sales(_engine, start_date):
    query = f"SELECT * FROM sales WHERE date >= '{start_date}'"
    return pd.read_sql(query, _engine)

data = query_sales(engine, "2024-01-01")
```

### Pattern 3: Tokenizer Loading

```python
@st.cache_resource
def load_tokenizer(model_name: str = "gpt-4"):
    import tiktoken
    return tiktoken.encoding_for_model(model_name)

# Usage
tokenizer = load_tokenizer()
tokens = tokenizer.encode("Hello, world!")
st.write(f"Token count: {len(tokens)}")
```

### Pattern 4: Multiple Model Variants

```python
@st.cache_resource(max_entries=3)
def load_language_model(language: str):
    # Cache English, Spanish, French models
    return pipeline("sentiment-analysis", model=f"model-{language}")

# Usage
language = st.selectbox("Language", ["en", "es", "fr"])
model = load_language_model(language)
text = st.text_input("Enter text")
if text:
    result = model(text)
    st.write(result)
```

### Pattern 5: File Handles

```python
@st.cache_resource
def open_log_file():
    return open("app.log", "a")

# Usage (be careful with thread safety!)
log_file = open_log_file()
log_file.write("User action logged\n")
log_file.flush()
```

### Pattern 6: API Clients

```python
@st.cache_resource
def get_openai_client():
    from openai import OpenAI
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Usage
client = get_openai_client()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Thread Safety Considerations

### Problem: Concurrent Mutations

```python
# ⚠️ DANGEROUS: Mutable shared resource
@st.cache_resource
def get_counter():
    return {"count": 0}

counter = get_counter()
counter["count"] += 1  # Race condition if multiple users!
```

**What happens**: Multiple users simultaneously incrementing causes data loss.

### Solution 1: Use Locks

```python
import threading

lock = threading.Lock()

@st.cache_resource
def get_counter():
    return {"count": 0}

counter = get_counter()

# Thread-safe increment
with lock:
    counter["count"] += 1
    st.write(f"Count: {counter['count']}")
```

### Solution 2: Use Immutable Objects

```python
from types import MappingProxyType

@st.cache_resource
def get_config():
    # Return immutable dict
    config = {"api_key": "secret", "endpoint": "https://api.com"}
    return MappingProxyType(config)

config = get_config()
# config["api_key"] = "new"  # ❌ TypeError: cannot modify
```

### Solution 3: Use cache_data Instead

```python
# If you need mutable data that varies per user, use cache_data
@st.cache_data
def get_user_data():
    return {"count": 0}

# Each user gets their own copy
user_data = get_user_data()
user_data["count"] += 1  # Safe!
```

### Solution 4: Read-Only Resource

```python
@st.cache_resource
def load_model():
    # Models are typically used read-only (inference)
    return pipeline("sentiment-analysis")

model = load_model()
result = model("text")  # Read-only operation - safe!
```

## Performance Optimization

### No Serialization Overhead

```python
# cache_data: slower for large objects (copies via pickle)
@st.cache_data
def load_huge_model():  # Takes seconds to copy
    return load_100gb_model()

# cache_resource: instant (no copying)
@st.cache_resource
def load_huge_model():  # Instant retrieval
    return load_100gb_model()
```

### Large Dataset Strategy

```python
# For datasets > 100M rows, cache_resource is faster
@st.cache_resource
def load_massive_dataset():
    # No serialization overhead
    return pd.read_parquet("100M_rows.parquet")

# But be careful about mutations!
data = load_massive_dataset()
# filtered = data[data["col"] > 5]  # ⚠️ If this mutates data, affects all users

# Safer: explicitly copy for mutations
filtered = load_massive_dataset().copy()
filtered = filtered[filtered["col"] > 5]  # Safe
```

## Combining cache_data and cache_resource

```python
# Pattern: Connection (resource) + Query (data)

@st.cache_resource
def get_database():
    return SQLAlchemy.create_engine("postgresql://...")

@st.cache_data(ttl=3600)
def query_data(_db, query: str):
    return pd.read_sql(query, _db)

# Usage
db = get_database()  # Shared connection
data = query_data(db, "SELECT * FROM sales")  # Cached data copy
```

## Real-World Examples

### Example 1: ML Inference App

```python
@st.cache_resource(show_spinner="Loading models...")
def load_models():
    sentiment = pipeline("sentiment-analysis")
    ner = pipeline("ner")
    return sentiment, ner

sentiment_model, ner_model = load_models()

text = st.text_area("Enter text")
if text:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sentiment")
        sentiment = sentiment_model(text)
        st.json(sentiment)

    with col2:
        st.subheader("Named Entities")
        entities = ner_model(text)
        st.json(entities)
```

### Example 2: Multi-Database Dashboard

```python
@st.cache_resource
def get_postgres():
    return SQLAlchemy.create_engine("postgresql://...")

@st.cache_resource
def get_mongo():
    return MongoClient("mongodb://...")

@st.cache_data(ttl=600)
def get_postgres_data(_engine):
    return pd.read_sql("SELECT * FROM metrics", _engine)

@st.cache_data(ttl=600)
def get_mongo_data(_client):
    return list(_client.db.collection.find())

# Usage
pg = get_postgres()
mg = get_mongo()

pg_data = get_postgres_data(pg)
mg_data = get_mongo_data(mg)

st.dataframe(pg_data)
st.json(mg_data)
```

### Example 3: Model Zoo

```python
MODELS = {
    "Fast": "distilbert-base-uncased",
    "Accurate": "bert-large-uncased",
    "Balanced": "bert-base-uncased"
}

@st.cache_resource(max_entries=3)
def load_bert_model(model_name: str):
    from transformers import AutoModel, AutoTokenizer
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

# User selects model
choice = st.selectbox("Select model", list(MODELS.keys()))
model_name = MODELS[choice]

# Load selected model (cached)
model, tokenizer = load_bert_model(model_name)
st.success(f"Loaded {model_name}")
```

## Debugging

### Check Resource Usage

```python
@st.cache_resource
def load_model():
    import psutil
    import os

    process = psutil.Process(os.getpid())
    before = process.memory_info().rss / 1024 / 1024  # MB

    st.write(f"Memory before: {before:.1f} MB")
    model = pipeline("sentiment-analysis")

    after = process.memory_info().rss / 1024 / 1024
    st.write(f"Memory after: {after:.1f} MB")
    st.write(f"Model size: ~{after - before:.1f} MB")

    return model
```

### Verify Singleton Behavior

```python
@st.cache_resource
def get_object():
    import uuid
    return {"id": str(uuid.uuid4())}

obj1 = get_object()
obj2 = get_object()

st.write(f"Object 1 ID: {obj1['id']}")
st.write(f"Object 2 ID: {obj2['id']}")
st.write(f"Same object: {obj1 is obj2}")  # Should be True
```

## Common Mistakes

### ❌ Mistake 1: Using cache_resource for data

```python
# Bad - data should use cache_data
@st.cache_resource
def load_csv():
    return pd.read_csv("data.csv")

# Good - use cache_data for data
@st.cache_data
def load_csv():
    return pd.read_csv("data.csv")
```

### ❌ Mistake 2: Mutating shared resources unsafely

```python
# Bad - race condition!
@st.cache_resource
def get_list():
    return []

my_list = get_list()
my_list.append(item)  # Affects all users!

# Good - use lock or cache_data
import threading
lock = threading.Lock()

my_list = get_list()
with lock:
    my_list.append(item)
```

### ❌ Mistake 3: Not considering memory for max_entries

```python
# Bad - could load 100 models = OOM!
@st.cache_resource(max_entries=100)
def load_model(name: str):
    return huge_model(name)

# Good - reasonable limit
@st.cache_resource(max_entries=3)
def load_model(name: str):
    return huge_model(name)
```

## Best Practices Summary

1. ✅ Use `@st.cache_resource` for ML models and connections
2. ✅ Be aware of singleton behavior (shared across users)
3. ✅ Ensure thread safety for mutable resources
4. ✅ Set `max_entries` for model variants
5. ✅ Use descriptive `show_spinner` messages
6. ✅ Combine with `@st.cache_data` for queries
7. ❌ Don't use for serializable data
8. ❌ Don't mutate shared resources without locks
9. ❌ Don't set unlimited `max_entries` for large models
10. ❌ Don't use for data that varies per user

---

## Quick Examples Cheat Sheet

```python
# ML Model
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

# Database Connection
@st.cache_resource
def get_db():
    return SQLAlchemy.create_engine("postgresql://...")

# Tokenizer
@st.cache_resource
def get_tokenizer():
    return tiktoken.encoding_for_model("gpt-4")

# Multiple models
@st.cache_resource(max_entries=5)
def load_model_variant(name: str):
    return load(name)

# With custom spinner
@st.cache_resource(show_spinner="Loading model...")
def load_large_model():
    return transformers.AutoModel.from_pretrained("large")

# Thread-safe mutation
lock = threading.Lock()

@st.cache_resource
def get_counter():
    return {"count": 0}

counter = get_counter()
with lock:
    counter["count"] += 1
```

## When to Choose cache_resource vs cache_data

| Question | Answer → Decorator |
|----------|-------------------|
| Is it a model? | Yes → `@st.cache_resource` |
| Is it a connection? | Yes → `@st.cache_resource` |
| Is it serializable data? | Yes → `@st.cache_data` |
| Is it very large (>100M rows)? | Maybe → `@st.cache_resource` (with caution) |
| Does it need to be mutable per-user? | Yes → `@st.cache_data` |
| Is thread safety a concern? | Yes → `@st.cache_data` (safer) |

**Default rule**: Start with `@st.cache_data`. Only use `@st.cache_resource` when you have a clear reason (models, connections, huge objects).
