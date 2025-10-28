# Streamlit Execution Model

## How Streamlit Apps Run

Streamlit apps have a unique execution model that differs from traditional web frameworks. Understanding this model is crucial for building efficient Streamlit applications.

## The Basic Execution Flow

### 1. Script Runs Top-to-Bottom

```python
import streamlit as st

print("This runs every time")  # Executes on every rerun
st.title("My App")              # Executes on every rerun
x = st.slider("Value", 0, 100)  # Executes on every rerun
st.write(f"x = {x}")            # Executes on every rerun
print("End of script")          # Executes on every rerun
```

**Key insight**: The entire script executes from top to bottom on every interaction.

### 2. Reruns Happen on Interaction

Every time a user interacts with a widget, Streamlit reruns the entire script:

```python
import streamlit as st

st.write("Script execution started")

# This slider causes a rerun when changed
value = st.slider("Adjust value", 0, 100)

st.write(f"Current value: {value}")

st.write("Script execution finished")
```

**What happens**:
1. User loads app → Script runs once
2. User moves slider → Script runs again (full rerun)
3. User moves slider again → Script runs again
4. Every interaction → Full script rerun

### 3. Widget State Persists Across Reruns

```python
# Run 1: User sets slider to 50
value = st.slider("Value", 0, 100)  # value = 50

# Run 2: User clicks button (slider stays at 50)
if st.button("Click me"):
    st.write(f"Slider is still: {value}")  # Prints 50
```

Widget values are automatically preserved by Streamlit between reruns.

## The Rerun Cycle

```
User opens app
       ↓
Script executes top-to-bottom
       ↓
Widgets rendered with default values
       ↓
User interacts with widget
       ↓
Script reruns top-to-bottom
       ↓
Widget shows new value
       ↓
(cycle continues)
```

## What Triggers a Rerun?

### Automatic Reruns

1. **Widget interactions**
   ```python
   st.button("Click")       # Click → rerun
   st.slider("Move", 0, 10) # Move → rerun
   st.text_input("Type")    # Type → rerun
   st.selectbox("Pick", []) # Select → rerun
   ```

2. **File changes** (development mode only)
   - Save Python file → Auto-rerun
   - Streamlit detects changes and reruns

### Manual Reruns

```python
if st.button("Refresh"):
    st.rerun()  # Manually trigger rerun

# Or based on logic
if some_condition:
    st.rerun()
```

### Preventing Reruns

```python
# Forms batch inputs - only rerun on submit
with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age")
    submitted = st.form_submit_button("Submit")

    # This block only reruns when form is submitted
    if submitted:
        st.write(f"{name} is {age} years old")
```

## Session State

### The Problem: Variables Don't Persist

```python
# This DOES NOT work as expected!
count = 0  # Reset to 0 on every rerun!

if st.button("Increment"):
    count += 1  # Increments, but resets next rerun

st.write(f"Count: {count}")  # Always shows 0
```

### The Solution: st.session_state

```python
# Initialize session state
if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Increment"):
    st.session_state.count += 1

st.write(f"Count: {st.session_state.count}")  # Persists!
```

### Session State Lifecycle

```
User Session Starts
       ↓
st.session_state created (empty dict)
       ↓
Script runs, populates session_state
       ↓
User interacts → Rerun
       ↓
st.session_state persists (same values)
       ↓
Script can read/write session_state
       ↓
User closes tab → session_state destroyed
```

## Execution Order

### Top-to-Bottom Execution

```python
st.write("1. First")

x = st.slider("Value", 0, 100)

st.write("2. Second")

if x > 50:
    st.write("3. Third (only if x > 50)")

st.write("4. Fourth (always)")
```

Output order matches code order (top-to-bottom).

### Conditional Execution

```python
mode = st.radio("Mode", ["A", "B"])

if mode == "A":
    st.write("Showing A")
    # This block only executes if mode == "A"
else:
    st.write("Showing B")
    # This block only executes if mode == "B"
```

Only the matching branch executes.

## Layout Rendering

### Widgets Create Placeholders

```python
# This creates a slider placeholder and returns value
value = st.slider("Pick", 0, 100)

# You can use the value immediately
doubled = value * 2
st.write(f"Double: {doubled}")
```

Streamlit renders widgets in order, but their values are set before the rerun.

### Container Execution

```python
# Main area
st.write("Main area 1")

# Sidebar executed in order too
with st.sidebar:
    st.write("Sidebar 1")
    st.write("Sidebar 2")

# Back to main
st.write("Main area 2")
```

Containers (sidebar, columns, etc.) execute when reached in script order.

## Fragments (Partial Reruns)

### The Problem: Full Reruns Are Expensive

```python
# Without fragments
@st.cache_data
def expensive_data():
    time.sleep(5)
    return load_data()

data = expensive_data()  # Runs once (cached)

# But this causes full rerun on every update!
refresh = st.button("Refresh metrics")
if refresh:
    st.write(f"Metrics updated at {time.time()}")
```

Every button click reruns entire script (even if most is cached).

### The Solution: st.fragment()

```python
@st.cache_data
def expensive_data():
    time.sleep(5)
    return load_data()

data = expensive_data()  # Only runs when necessary

# Fragment: only this section reruns
@st.fragment
def show_metrics():
    st.write(f"Metrics updated at {time.time()}")
    if st.button("Refresh", key="refresh_metrics"):
        st.rerun(scope="fragment")  # Only rerun this fragment

show_metrics()
```

Fragments allow partial reruns without re-executing the entire script.

### Auto-Updating Fragments

```python
@st.fragment(run_every="10s")
def live_metrics():
    st.metric("Active Users", get_user_count())
    st.metric("CPU", get_cpu_usage())

live_metrics()  # Auto-refreshes every 10 seconds
```

## Performance Optimization

### 1. Cache Expensive Operations

```python
# Bad: Runs on every rerun
data = pd.read_csv("large.csv")

# Good: Cached
@st.cache_data
def load_data():
    return pd.read_csv("large.csv")

data = load_data()  # Only loads once
```

### 2. Use Forms to Batch Inputs

```python
# Bad: Every input causes rerun
name = st.text_input("Name")      # Rerun on every keystroke
email = st.text_input("Email")    # Rerun on every keystroke
age = st.number_input("Age")      # Rerun on every change

# Good: Batch with form
with st.form("user_form"):
    name = st.text_input("Name")   # No rerun while typing
    email = st.text_input("Email") # No rerun while typing
    age = st.number_input("Age")   # No rerun while changing
    submitted = st.form_submit_button("Submit")

    # Only reruns on submit
    if submitted:
        save_user(name, email, age)
```

### 3. Use Fragments for Isolated Updates

```python
# Heavy data loading (once)
@st.cache_data
def load_data():
    return expensive_load()

data = load_data()

# Fragment for user interactions
@st.fragment
def filter_ui():
    filter_val = st.slider("Filter", 0, 100)
    return filter_val

filter_val = filter_ui()
filtered_data = data[data['value'] > filter_val]
```

### 4. Minimize Script Length

```python
# Bad: Long script
# ... 1000 lines of code ...
value = st.slider("Value", 0, 100)
# ... 1000 more lines ...

# Good: Modularize
from my_module import process_data

value = st.slider("Value", 0, 100)
result = process_data(value)  # Imported functions are faster
```

## Common Patterns

### Pattern 1: Initialization

```python
# Initialize session state on first run
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.user_data = load_user()
    st.session_state.config = load_config()

# Use session state
st.write(st.session_state.user_data)
```

### Pattern 2: Multi-Step Flow

```python
if "step" not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    name = st.text_input("Name")
    if st.button("Next"):
        st.session_state.name = name
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    email = st.text_input("Email")
    if st.button("Submit"):
        save_user(st.session_state.name, email)
        st.success("Done!")
```

### Pattern 3: Data Loading + User Interaction

```python
# Load once (cached)
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

# Runs every rerun (fast, just filtering)
data = load_data()
category = st.selectbox("Category", data['category'].unique())
filtered = data[data['category'] == category]
st.dataframe(filtered)
```

## Advanced: Stopping Execution

```python
if not st.session_state.get("logged_in"):
    st.warning("Please log in")
    st.stop()  # Stop execution here

# This code only runs if logged in
st.write("Welcome!")
show_dashboard()
```

## Execution Flow Diagram

```
┌─────────────────────────────────────┐
│ User Opens App                      │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Streamlit Server Starts             │
│ - Create session                    │
│ - Initialize st.session_state = {}  │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Execute Script (Top to Bottom)      │
│ - Run all Python code               │
│ - Render widgets                    │
│ - Display output                    │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Wait for User Interaction           │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ User Interacts (click, type, etc.)  │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Rerun Script (Top to Bottom)        │
│ - st.session_state persists         │
│ - Widget values preserved           │
│ - Cached functions skip execution   │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Update Display                      │
└──────────────┬──────────────────────┘
               ↓
     (Loop back to Wait)
```

## Key Takeaways

1. **Script runs top-to-bottom on every interaction**
2. **Reruns are triggered by widget interactions**
3. **Widget state persists automatically**
4. **Use st.session_state for custom state**
5. **Cache expensive operations**
6. **Use forms to batch inputs**
7. **Use fragments for partial reruns**
8. **Execution order matches code order**

## Mental Model

Think of Streamlit as:
```python
while True:  # Infinite loop
    run_script_from_top()
    wait_for_user_interaction()
```

Every interaction triggers a full script rerun with preserved state.

This model makes Streamlit apps easy to reason about: your script is always the single source of truth for what's displayed.
