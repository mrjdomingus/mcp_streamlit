# Streamlit App Testing - Complete Guide

## Overview

Streamlit's native testing framework (`st.testing.v1.AppTest`) enables automated testing of your applications without a browser. It provides similar functionality to Selenium or Playwright but with less overhead.

**Key Benefits:**
- ✅ No browser required
- ✅ Fast execution
- ✅ Easy integration with pytest
- ✅ Access to app state and elements
- ✅ Simulate user interactions
- ✅ Test in CI/CD pipelines

## Getting Started

### Installation

```bash
pip install streamlit pytest
```

### Basic Example

```python
# app.py
import streamlit as st

name = st.text_input("Your name")
if st.button("Greet"):
    st.write(f"Hello, {name}!")
```

```python
# test_app.py
from streamlit.testing.v1 import AppTest

def test_greeting():
    # Initialize the app
    at = AppTest.from_file("app.py")

    # Run the app
    at.run()
    assert not at.exception

    # Simulate user input
    at.text_input[0].input("Alice").run()

    # Click the button
    at.button[0].click().run()

    # Verify output
    assert "Hello, Alice!" in at.markdown[0].value
```

## AppTest Class

### Initialization Methods

#### 1. from_file()

Load app from a Python file:

```python
at = AppTest.from_file("streamlit_app.py")
at.run()
```

**Best for:** Testing deployed apps, integration tests

#### 2. from_string()

Create app from inline code:

```python
app_code = """
import streamlit as st
st.title("Test App")
value = st.slider("Value", 0, 100)
st.write(f"Value: {value}")
"""

at = AppTest.from_string(app_code)
at.run()
```

**Best for:** Unit tests, testing code snippets

#### 3. from_function()

Initialize from a callable:

```python
def my_app():
    import streamlit as st
    st.title("My App")
    # app logic

at = AppTest.from_function(my_app)
at.run()
```

**Best for:** Modular apps, testing specific functions

## Core Concepts

### The run() Method

Every interaction must be followed by `.run()` to execute the app:

```python
at = AppTest.from_file("app.py")

# Initial run
at.run()

# After interaction
at.button[0].click().run()

# Chain multiple interactions
at.text_input[0].input("test").button[0].click().run()
```

### Element Access

Access elements by type and index:

```python
# First button
at.button[0]

# Second text input
at.text_input[1]

# All buttons
for button in at.button:
    print(button.value)
```

### Element Properties

All elements have a `.value` property:

```python
assert at.title[0].value == "My App"
assert at.text_input[0].value == "default text"
assert at.checkbox[0].value == True
```

### Exception Handling

Always check for exceptions after `.run()`:

```python
at.run()
if at.exception:
    raise at.exception

# Or use assert
assert not at.exception
```

## Testing Widgets

### Button

```python
# Click a button
at.button[0].click().run()

# Get button label
assert at.button[0].label == "Submit"

# Check if button exists
assert len(at.button) > 0
```

### Text Input

```python
# Set value
at.text_input[0].input("Hello").run()

# Get current value
assert at.text_input[0].value == "Hello"

# Test with key
at.text_input("my_key").input("World").run()
```

### Text Area

```python
# Multi-line input
at.text_area[0].input("Line 1\nLine 2").run()

# Verify value
assert "Line 1" in at.text_area[0].value
```

### Checkbox

```python
# Check/uncheck
at.checkbox[0].check().run()
at.checkbox[0].uncheck().run()

# Set specific value
at.checkbox[0].set_value(True).run()

# Get state
assert at.checkbox[0].value == True
```

### Radio

```python
# Select option
at.radio[0].set_value("Option B").run()

# Verify selection
assert at.radio[0].value == "Option B"
```

### Selectbox

```python
# Select option
at.selectbox[0].select("New York").run()

# Or by index
at.selectbox[0].select_index(2).run()

# Verify selection
assert at.selectbox[0].value == "New York"
```

### Multiselect

```python
# Select multiple options
at.multiselect[0].select("Option A").run()
at.multiselect[0].select("Option B").run()

# Unselect
at.multiselect[0].unselect("Option A").run()

# Verify selections
assert "Option B" in at.multiselect[0].value
```

### Slider

```python
# Set value
at.slider[0].set_value(50).run()

# Set range (for range slider)
at.slider[0].set_range(20, 80).run()

# Verify value
assert at.slider[0].value == 50
```

### Number Input

```python
# Increment
at.number_input[0].increment().run()

# Decrement
at.number_input[0].decrement().run()

# Set specific value
at.number_input[0].set_value(42).run()
```

### Date Input

```python
import datetime

# Set date
at.date_input[0].set_value(datetime.date(2024, 1, 15)).run()

# Verify date
assert at.date_input[0].value == datetime.date(2024, 1, 15)
```

### Time Input

```python
import datetime

# Set time
at.time_input[0].set_value(datetime.time(14, 30)).run()

# Increment
at.time_input[0].increment().run()
```

### Color Picker

```python
# Pick color
at.color_picker[0].pick("#FF4B4B").run()

# Verify color
assert at.color_picker[0].value == "#FF4B4B"
```

### File Uploader

```python
# Upload file
import io

file_data = io.BytesIO(b"file contents")
at.file_uploader[0].upload(file_data, "test.txt").run()
```

### Toggle

```python
# Toggle on/off
at.toggle[0].set_value(True).run()

# Verify state
assert at.toggle[0].value == True
```

### Chat Input

```python
# Send message
at.chat_input[0].set_value("Hello, chatbot!").run()

# Verify message
assert at.chat_input[0].value == "Hello, chatbot!"
```

## Testing Forms

```python
# app.py
with st.form("my_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success(f"Welcome, {name}!")

# test_app.py
def test_form_submission():
    at = AppTest.from_file("app.py")
    at.run()

    # Fill form
    at.text_input[0].input("Alice")
    at.text_input[1].input("alice@example.com")

    # Submit (all changes happen on submit)
    at.button[0].click().run()

    # Verify success message
    assert "Welcome, Alice!" in at.success[0].value
```

## Testing Session State

```python
# app.py
if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Increment"):
    st.session_state.count += 1

st.write(f"Count: {st.session_state.count}")

# test_app.py
def test_session_state():
    at = AppTest.from_file("app.py")
    at.run()

    # Initial state
    assert "Count: 0" in at.markdown[0].value

    # Click button
    at.button[0].click().run()

    # Verify state updated
    assert "Count: 1" in at.markdown[0].value

    # Click again
    at.button[0].click().run()
    assert "Count: 2" in at.markdown[0].value
```

### Setting Session State Directly

```python
def test_with_preset_state():
    at = AppTest.from_file("app.py")

    # Set session state before running
    at.session_state["user_id"] = 123
    at.session_state["logged_in"] = True

    at.run()

    # App sees the preset state
    assert at.session_state["logged_in"] == True
```

## Testing with Secrets

```python
# app.py
import streamlit as st

api_key = st.secrets["API_KEY"]
st.write(f"Key length: {len(api_key)}")

# test_app.py
def test_with_secrets():
    at = AppTest.from_file("app.py")

    # Set secrets before running
    at.secrets["API_KEY"] = "test_key_12345"

    at.run()
    assert not at.exception

    # Verify app used the secret
    assert "Key length: 14" in at.markdown[0].value
```

## Testing Data Loading

```python
# app.py
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

data = load_data()
st.dataframe(data)

# test_app.py
import pytest
from unittest.mock import patch, MagicMock

def test_data_loading():
    # Mock the data loading
    with patch('pandas.read_csv') as mock_csv:
        mock_csv.return_value = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })

        at = AppTest.from_file("app.py")
        at.run()

        assert not at.exception
        # Verify dataframe is displayed
        assert len(at.dataframe) == 1
```

## Testing Multi-Page Apps

```python
# app.py (using st.navigation)
import streamlit as st
from pages_lib import home, data

pages = {
    "Home": st.Page(home.show, title="Home"),
    "Data": st.Page(data.show, title="Data")
}

pg = st.navigation(pages)
pg.run()

# test_app.py
def test_multipage_navigation():
    at = AppTest.from_file("app.py")
    at.run()

    # Verify home page loads
    assert not at.exception

    # TODO: Navigation testing support coming
    # at.switch_page("Data")
    # at.run()
```

## Container Access

### Sidebar

```python
# Access sidebar elements
sidebar_button = at.sidebar.button[0]
sidebar_button.click().run()

# Verify sidebar content
assert at.sidebar.title[0].value == "Settings"
```

### Columns

```python
# app.py
col1, col2 = st.columns(2)
with col1:
    st.write("Left")
with col2:
    st.write("Right")

# test_app.py
def test_columns():
    at = AppTest.from_file("app.py")
    at.run()

    # Access columns
    assert at.columns[0][0].markdown[0].value == "Left"
    assert at.columns[0][1].markdown[0].value == "Right"
```

### Tabs

```python
# app.py
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    st.write("Content 1")
with tab2:
    st.write("Content 2")

# test_app.py
def test_tabs():
    at = AppTest.from_file("app.py")
    at.run()

    # Both tabs render
    assert at.tabs[0][0].markdown[0].value == "Content 1"
    assert at.tabs[0][1].markdown[0].value == "Content 2"
```

## Common Patterns

### Test Fixture for AppTest

```python
import pytest

@pytest.fixture
def app():
    """Provide a fresh AppTest instance."""
    at = AppTest.from_file("app.py")
    at.run()
    return at

def test_with_fixture(app):
    assert not app.exception
    app.button[0].click().run()
    assert "Success" in app.success[0].value
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input_value,expected", [
    ("apple", "APPLE"),
    ("banana", "BANANA"),
    ("cherry", "CHERRY"),
])
def test_uppercase_conversion(input_value, expected):
    at = AppTest.from_file("app.py")
    at.run()

    at.text_input[0].input(input_value).run()
    at.button[0].click().run()

    assert expected in at.markdown[0].value
```

### Testing Error Conditions

```python
def test_error_handling():
    at = AppTest.from_file("app.py")
    at.run()

    # Trigger error condition
    at.text_input[0].input("invalid").run()
    at.button[0].click().run()

    # Verify error message
    assert len(at.error) > 0
    assert "Invalid input" in at.error[0].value
```

### Testing User Flow

```python
def test_complete_user_flow():
    """Test entire user journey."""
    at = AppTest.from_file("app.py")
    at.run()

    # Step 1: Login
    at.text_input("username").input("alice").run()
    at.text_input("password").input("secret").run()
    at.button[0].click().run()

    assert "Welcome" in at.success[0].value

    # Step 2: Upload data
    file_data = io.BytesIO(b"data")
    at.file_uploader[0].upload(file_data, "data.csv").run()

    assert len(at.dataframe) > 0

    # Step 3: Process
    at.button[1].click().run()

    assert "Processing complete" in at.info[0].value
```

## Best Practices

### 1. Test Organization

```python
# tests/
#   conftest.py        # Shared fixtures
#   test_ui.py         # UI interaction tests
#   test_logic.py      # Business logic tests
#   test_integration.py # Full flow tests
```

### 2. Descriptive Test Names

```python
# Good
def test_form_validates_email_format():
    ...

def test_button_increments_counter_by_one():
    ...

# Bad
def test_form():
    ...

def test_button():
    ...
```

### 3. Arrange-Act-Assert Pattern

```python
def test_search_functionality():
    # Arrange
    at = AppTest.from_file("app.py")
    at.secrets["API_KEY"] = "test_key"
    at.run()

    # Act
    at.text_input[0].input("search query").run()
    at.button[0].click().run()

    # Assert
    assert not at.exception
    assert len(at.dataframe) > 0
```

### 4. Use Fixtures for Common Setup

```python
@pytest.fixture
def authenticated_app():
    at = AppTest.from_file("app.py")
    at.session_state["logged_in"] = True
    at.session_state["user_id"] = 123
    at.run()
    return at

def test_dashboard(authenticated_app):
    assert "Welcome" in authenticated_app.title[0].value
```

### 5. Test Edge Cases

```python
def test_empty_input():
    at = AppTest.from_file("app.py")
    at.run()
    at.text_input[0].input("").run()
    at.button[0].click().run()
    assert "Please enter" in at.warning[0].value

def test_very_long_input():
    at = AppTest.from_file("app.py")
    at.run()
    long_text = "x" * 10000
    at.text_input[0].input(long_text).run()
    # Verify app handles it gracefully
```

## Debugging Tests

### Print App State

```python
def test_debug():
    at = AppTest.from_file("app.py")
    at.run()

    # Print all elements
    print("Buttons:", len(at.button))
    print("Text inputs:", len(at.text_input))
    print("Markdown:", [m.value for m in at.markdown])

    # Print session state
    print("Session state:", dict(at.session_state))
```

### Check for Exceptions

```python
def test_with_exception_details():
    at = AppTest.from_file("app.py")
    at.run()

    if at.exception:
        print(f"Exception: {at.exception}")
        print(f"Traceback: {at.exception.__traceback__}")
        raise at.exception
```

## Running Tests

### Run with pytest

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_app.py

# Run specific test
pytest tests/test_app.py::test_greeting

# Run with verbose output
pytest -v tests/

# Run with coverage
pytest --cov=. tests/
```

### pytest.ini Configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

## Quick Reference

```python
# Initialize
at = AppTest.from_file("app.py")
at = AppTest.from_string(code)
at = AppTest.from_function(func)

# Setup
at.secrets["KEY"] = "value"
at.session_state["var"] = value

# Run
at.run()
assert not at.exception

# Access elements
at.button[0]
at.text_input[1]
at.sidebar.selectbox[0]

# Interact
at.button[0].click().run()
at.text_input[0].input("text").run()
at.checkbox[0].check().run()
at.selectbox[0].select("option").run()
at.slider[0].set_value(50).run()

# Assert
assert at.title[0].value == "Expected"
assert "text" in at.markdown[0].value
assert at.checkbox[0].value == True
```

## Summary

Streamlit's AppTest provides a powerful, lightweight testing framework for your apps. Key takeaways:

1. **Easy setup**: Three initialization methods for different use cases
2. **Full coverage**: Test all widgets and interactions
3. **State management**: Access session state and secrets
4. **Fast execution**: No browser overhead
5. **pytest integration**: Use familiar testing tools
6. **CI/CD ready**: Run in automated pipelines

**Next steps:**
- Write tests for your existing apps
- Set up automated testing in CI/CD
- Aim for >80% test coverage
- Test both happy paths and edge cases
