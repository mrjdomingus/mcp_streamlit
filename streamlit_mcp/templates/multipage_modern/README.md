# Modern Multi-Page Streamlit App Template

This template demonstrates the modern approach to building multi-page Streamlit applications using `st.navigation()` and `st.Page()`.

## Features

✅ **Modern Navigation API** - Uses `st.navigation()` instead of pages/ folder
✅ **Conditional Navigation** - Shows different pages based on authentication
✅ **Grouped Pages** - Organized into logical sections
✅ **Shared State** - Data persists across pages via `st.session_state`
✅ **Page Functions** - Each page is a clean function in a module
✅ **Caching** - Proper use of `@st.cache_data`
✅ **Authentication** - Simple login/logout flow (easily replaceable)

## Structure

```
multipage_modern/
├── app.py                  # Main application with navigation
├── pages_lib/              # Page modules (NOT pages/ folder!)
│   ├── home.py            # Welcome page
│   ├── data_analysis.py   # Data loading and filtering
│   ├── visualizations.py  # Charts and graphs
│   └── settings.py        # User preferences
└── README.md              # This file
```

## How to Run

```bash
streamlit run app.py
```

## How It Works

### 1. Main App (app.py)

The main file defines navigation using `st.navigation()`:

```python
import streamlit as st
from pages_lib import home, data_analysis, visualizations, settings

# Define pages
pages = {
    "Home": [
        st.Page(home.show, title="Welcome", icon="🏠")
    ],
    "Data": [
        st.Page(data_analysis.show, title="Data Analysis", icon="📊"),
        st.Page(visualizations.show, title="Visualizations", icon="📈")
    ],
    "Settings": [
        st.Page(settings.show, title="Preferences", icon="⚙️")
    ]
}

# Create and run navigation
pg = st.navigation(pages)
pg.run()
```

### 2. Page Functions

Each page is a simple function:

```python
# pages_lib/my_page.py
def show():
    st.title("My Page")
    # Page content here
```

### 3. Shared State

Pages communicate via `st.session_state`:

```python
# In data_analysis.py
st.session_state.data = load_data()

# In visualizations.py
data = st.session_state.data  # Access data from other page
```

## Key Differences from pages/ Folder Approach

| Feature | pages/ Folder | st.navigation() |
|---------|--------------|-----------------|
| File structure | `pages/01_page.py` | `pages_lib/page.py` |
| Page definition | File-based | Function-based |
| Conditional nav | Not supported | Full support |
| Grouped nav | Not supported | Full support |
| Dynamic pages | Difficult | Easy |
| Testing | Harder | Easier |

## Customization

### Remove Authentication

If you don't need login:

```python
# In app.py, replace the auth section with:
pages = {
    "Home": [...],
    "Data": [...],
    "Settings": [...]
}
pg = st.navigation(pages)
pg.run()
```

### Add New Pages

1. Create `pages_lib/new_page.py`:
```python
def show():
    st.title("New Page")
    # Content here
```

2. Add to navigation in `app.py`:
```python
from pages_lib import new_page

pages = {
    "Home": [...],
    "New Section": [
        st.Page(new_page.show, title="New Page", icon="🎉")
    ]
}
```

### Add Real Authentication

Replace the demo login with:

**Option 1: st.login() (when stable)**
```python
st.login()  # Built-in Streamlit auth
```

**Option 2: Custom Auth**
```python
def login(username, password):
    # Your auth logic
    return check_credentials(username, password)
```

**Option 3: OAuth**
```python
from streamlit_oauth import OAuth
# OAuth implementation
```

## Page Flow Example

1. User logs in → `app.py` sets `st.session_state.logged_in = True`
2. Navigation shows full menu
3. User goes to Data Analysis → Loads data into `st.session_state.data`
4. User goes to Visualizations → Accesses `st.session_state.data`
5. User goes to Settings → Changes preferences in `st.session_state.settings`
6. All pages see updated settings

## Best Practices

1. ✅ **Keep page functions pure** - All page logic in the function
2. ✅ **Use session state for sharing** - Not global variables
3. ✅ **Cache expensive operations** - Use `@st.cache_data`
4. ✅ **Check state existence** - Use `.get()` or `if key in st.session_state`
5. ✅ **Clear state when needed** - Reset on logout or page changes

## Troubleshooting

**Page not showing:**
- Check that function is imported in `app.py`
- Ensure `st.Page()` points to correct function
- Verify no errors in page function

**State not persisting:**
- State persists within a session (one browser tab)
- Closing tab clears state
- Use `st.cache_data` for data that should survive reruns

**Navigation not working:**
- Ensure all pages are defined before `st.navigation()`
- Check that `pg.run()` is called
- Verify conditional logic for auth pages

## Migration from pages/ Folder

**Old structure:**
```
pages/
  01_home.py
  02_data.py
  03_viz.py
```

**New structure:**
```
pages_lib/
  home.py      -> def show(): ...
  data.py      -> def show(): ...
  viz.py       -> def show(): ...
app.py         -> st.navigation(...)
```

**Migration steps:**
1. Create `pages_lib/` directory
2. Move page content into `show()` functions
3. Create `app.py` with `st.navigation()`
4. Update imports
5. Test each page
6. Remove old `pages/` directory

## Learn More

- [st.navigation() docs](https://docs.streamlit.io/develop/api-reference/navigation)
- [Multi-page apps guide](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app)
- [Session State docs](https://docs.streamlit.io/develop/concepts/architecture/session-state)
