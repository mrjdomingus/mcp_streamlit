# Streamlit MCP Server - Best Practices Guide

> **MCP Resource Type**: Best Practices Guide
> **Purpose**: Essential guidelines for building Streamlit applications with this MCP server
> **Usage**: Reference these practices in all code generation and planning

## Core Best Practices

### 1. Multipage Navigation

**✅ ALWAYS DO:**
- Use `st.navigation()` with `st.Page()` for multipage apps (modern method)
- Define pages as functions in your main `app.py` or reference separate files
- If using separate page files, name them with a number prefix: `1_home.py`, `2_dashboard.py`, `3_settings.py`
- Use the entrypoint pattern with `pg = st.navigation(pages)` and `pg.run()`

**❌ NEVER DO:**
- Don't use the legacy `pages/` folder structure
- Don't rely on automatic page discovery
- Don't use the old multipage approach without explicit navigation

**Example:**
```python
# app.py (correct approach)
import streamlit as st

# Option 1: Define page functions directly
def home():
    st.title("🏠 Home")
    st.write("Welcome!")

def dashboard():
    st.title("📊 Dashboard")
    st.write("Dashboard content...")

# Create navigation
pages = {
    "Main": [
        st.Page(home, title="Home", icon="🏠"),
        st.Page(dashboard, title="Dashboard", icon="📊"),
    ]
}

pg = st.navigation(pages)
pg.run()

# Option 2: Reference separate files (must start with numbers)
# pages = {
#     "Main": [
#         st.Page("1_home.py", title="Home", icon="🏠"),
#         st.Page("2_dashboard.py", title="Dashboard", icon="📊"),
#     ]
# }
```

### 2. Package Management

**✅ ALWAYS USE UV:**
- Use `uv` for all package management operations
- Install packages: `uv pip install package-name`
- Add to project: `uv add package-name`
- Sync dependencies: `uv sync`
- Create environments: `uv venv`

**❌ AVOID:**
- Don't use `pip` directly when UV is available
- Don't use `conda` unless specifically required by user

**Why UV?**
- 10-100x faster than pip
- Better dependency resolution
- Built-in virtual environment management
- Compatible with existing pip workflows
- First-class support in this MCP server

### 3. Caching Strategies

**Data Loading:**
```python
@st.cache_data(ttl=1800)  # Cache for 30 minutes
def load_api_data():
    response = requests.get("https://api.example.com/data")
    return pd.DataFrame(response.json())
```

**Resource Management:**
```python
@st.cache_resource  # Cache connections, don't recreate
def get_database_connection():
    return create_db_connection()
```

**When NOT to cache:**
- User-uploaded files (session-specific)
- Rapidly changing data (unless using appropriate TTL)
- Random data generation (unless intentional)

### 4. Session State Management

**Always initialize before use:**
```python
# Initialize session state
if 'counter' not in st.session_state:
    st.session_state.counter = 0

if 'messages' not in st.session_state:
    st.session_state.messages = []
```

**Best practices:**
- Check existence before accessing
- Initialize at the top of your script
- Use descriptive keys
- Keep state minimal and focused

### 5. Performance Optimization

**Use Fragments for expensive operations:**
```python
@st.fragment
def expensive_chart():
    """This section updates independently"""
    # Expensive visualization here
    st.plotly_chart(create_complex_chart())

expensive_chart()  # Won't trigger full page rerun
```

**Use Forms for batch inputs:**
```python
with st.form("my_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Submit")

    if submitted:
        # Process all inputs at once
        process_form(name, email)
```

### 6. File Naming Conventions

**Page files:**
- Use number prefix: `1_home.py`, `2_dashboard.py`, `3_settings.py`
- Numbers control default order (but you can override in st.Page())
- Use descriptive names after the number

**Regular Python files:**
- Use standard Python naming: `utils.py`, `data_loader.py`, `config.py`
- No number prefix needed for non-page files

### 7. Page Configuration

**Always set page config first:**
```python
import streamlit as st

# MUST be the first Streamlit command
st.set_page_config(
    page_title="My App",
    page_icon="📊",
    layout="wide",  # or "centered"
    initial_sidebar_state="auto"
)
```

### 8. Code Organization

**Recommended structure:**
```
project/
├── app.py                  # Main entry point with navigation
├── 1_home.py              # Home page (optional separate file)
├── 2_dashboard.py         # Dashboard page (optional)
├── utils/                 # Utility functions
│   ├── data_loader.py
│   └── charts.py
├── requirements.txt       # OR pyproject.toml
└── .streamlit/
    └── config.toml
```

**Don't create:**
- `pages/` folder (use st.navigation instead)
- Deeply nested page structures
- Monolithic single-file apps (split into functions/modules)

## Quick Reference Checklist

When planning or generating Streamlit code:

- [ ] Use st.navigation() for multipage apps
- [ ] Number page files (1_home.py, 2_dashboard.py)
- [ ] Use UV for package management
- [ ] Initialize session_state before use
- [ ] Apply appropriate caching (@st.cache_data or @st.cache_resource)
- [ ] Use fragments for expensive operations
- [ ] Use forms for batch inputs
- [ ] Set page config as first command
- [ ] Organize code into logical functions/modules

## Related Resources

- **Caching Guide**: See `cache_data_guide.md` and `cache_resource_guide.md`
- **Testing Guide**: See `app_testing_guide.md`
- **Official Docs**: See `official/concepts/multipage-apps/`
- **Templates**: See `templates/` directory for working examples

---

*Last Updated: 2025-10-29*
*Version: 1.0*
