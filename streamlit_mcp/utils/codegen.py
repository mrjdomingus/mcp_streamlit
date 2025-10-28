"""Code generation utilities for Streamlit MCP server."""

from typing import Any, Dict, List, Optional, Set
import textwrap


class StreamlitCodeGenerator:
    """Utility class for generating Streamlit code."""

    def __init__(self):
        self.imports: Set[str] = {"import streamlit as st"}
        self.code_blocks: List[str] = []

    def add_import(self, import_stmt: str) -> None:
        """Add an import statement."""
        self.imports.add(import_stmt)

    def add_code(self, code: str, indent_level: int = 0) -> None:
        """Add a code block with proper indentation."""
        indented = textwrap.indent(code, "    " * indent_level)
        self.code_blocks.append(indented)

    def generate(self) -> str:
        """Generate the complete code with imports and blocks."""
        parts = []

        # Add imports
        if self.imports:
            parts.append("\n".join(sorted(self.imports)))
            parts.append("")

        # Add code blocks
        if self.code_blocks:
            parts.append("\n\n".join(self.code_blocks))

        return "\n".join(parts)

    def reset(self) -> None:
        """Reset the generator."""
        self.imports = {"import streamlit as st"}
        self.code_blocks = []


def format_kwargs(kwargs: Dict[str, Any]) -> str:
    """Format keyword arguments for function calls."""
    if not kwargs:
        return ""

    parts = []
    for key, value in kwargs.items():
        if isinstance(value, str):
            parts.append(f'{key}="{value}"')
        elif isinstance(value, bool):
            parts.append(f"{key}={value}")
        elif isinstance(value, (int, float)):
            parts.append(f"{key}={value}")
        elif isinstance(value, list):
            parts.append(f"{key}={value}")
        elif isinstance(value, dict):
            parts.append(f"{key}={value}")
        elif value is None:
            parts.append(f"{key}=None")
        else:
            parts.append(f"{key}={repr(value)}")

    return ", ".join(parts)


def generate_text_element(
    element_type: str, content: str, kwargs: Optional[Dict[str, Any]] = None
) -> str:
    """Generate code for text elements like st.title(), st.header(), etc."""
    kwargs_str = format_kwargs(kwargs or {})
    if kwargs_str:
        return f'st.{element_type}("{content}", {kwargs_str})'
    return f'st.{element_type}("{content}")'


def generate_widget(widget_type: str, label: str, kwargs: Optional[Dict[str, Any]] = None) -> str:
    """Generate code for input widgets."""
    kwargs_str = format_kwargs(kwargs or {})
    if kwargs_str:
        return f'st.{widget_type}("{label}", {kwargs_str})'
    return f'st.{widget_type}("{label}")'


def generate_chart(
    chart_type: str, data_var: str = "data", kwargs: Optional[Dict[str, Any]] = None
) -> str:
    """Generate code for charts."""
    kwargs_str = format_kwargs(kwargs or {})
    if kwargs_str:
        return f"st.{chart_type}({data_var}, {kwargs_str})"
    return f"st.{chart_type}({data_var})"


def generate_layout(layout_type: str, kwargs: Optional[Dict[str, Any]] = None) -> str:
    """Generate code for layout elements."""
    kwargs_str = format_kwargs(kwargs or {})
    if kwargs_str:
        return f"st.{layout_type}({kwargs_str})"
    return f"st.{layout_type}()"


def generate_data_loader(data_type: str) -> tuple[str, str]:
    """Generate example data loading code."""
    if data_type == "csv":
        imports = "import pandas as pd"
        code = """# Load data from CSV
data = pd.read_csv("your_data.csv")
st.dataframe(data)"""
        return imports, code

    elif data_type == "api":
        imports = "import pandas as pd\nimport requests"
        code = """# Load data from API
response = requests.get("https://api.example.com/data")
data = pd.DataFrame(response.json())
st.dataframe(data)"""
        return imports, code

    elif data_type == "sql":
        imports = ""
        code = """# Load data from SQL
conn = st.connection("sql")
data = conn.query("SELECT * FROM your_table")
st.dataframe(data)"""
        return imports, code

    elif data_type == "example":
        imports = "import pandas as pd\nimport numpy as np"
        code = """# Generate example data
data = pd.DataFrame({
    'column_1': np.random.randn(100),
    'column_2': np.random.randn(100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})
st.dataframe(data)"""
        return imports, code

    else:
        return "", "data = None  # Replace with your data source"


def generate_session_state_code(var_name: str, initial_value: Any = None) -> str:
    """Generate session state code."""
    if initial_value is None:
        return f"""# Initialize session state
if "{var_name}" not in st.session_state:
    st.session_state.{var_name} = None"""
    else:
        return f"""# Initialize session state
if "{var_name}" not in st.session_state:
    st.session_state.{var_name} = {repr(initial_value)}"""


def generate_cache_decorator(cache_type: str, kwargs: Optional[Dict[str, Any]] = None) -> str:
    """Generate cache decorator code."""
    kwargs_str = format_kwargs(kwargs or {})
    if kwargs_str:
        return f"@st.{cache_type}({kwargs_str})"
    return f"@st.{cache_type}"


def generate_multipage_structure() -> Dict[str, str]:
    """Generate a multi-page app structure using modern st.navigation API."""
    return {
        "app.py": """import streamlit as st

# ===================================================================
# MODERN MULTIPAGE APP USING st.navigation()
# ===================================================================
# This approach uses st.navigation() with st.Page() instead of the
# legacy pages/ folder. Benefits:
# - Full control over navigation
# - Can pass functions or file paths
# - No magic folder structure required
# ===================================================================

st.set_page_config(
    page_title="My Multi-Page App",
    page_icon="🏠",
    layout="wide"
)

# Define page functions
def home():
    st.title("🏠 Welcome to My Multi-Page App")
    st.markdown("Use the sidebar to navigate between pages.")
    st.info("This app uses st.navigation() for modern page management.")

def page_one():
    st.title("📊 Page One")
    st.write("This is the first page of your multi-page app.")
    st.write("You can add charts, data, and interactive elements here.")

def page_two():
    st.title("📈 Page Two")
    st.write("This is the second page of your multi-page app.")
    st.write("Each page can have its own unique content and functionality.")

# Define navigation
pages = {
    "Main": [
        st.Page(home, title="Home", icon="🏠"),
    ],
    "Pages": [
        st.Page(page_one, title="Page One", icon="📊"),
        st.Page(page_two, title="Page Two", icon="📈"),
    ]
}

pg = st.navigation(pages)
pg.run()

# ===================================================================
# ALTERNATIVE: Use separate files instead of functions
# ===================================================================
# If you prefer separate files, you can do:
# pages = {
#     "Main": [
#         st.Page("home.py", title="Home", icon="🏠"),
#     ],
#     "Pages": [
#         st.Page("page_one.py", title="Page One", icon="📊"),
#         st.Page("page_two.py", title="Page Two", icon="📈"),
#     ]
# }
# Note: Files can be anywhere, no pages/ folder needed!
# ===================================================================
"""
    }


def generate_form_code(form_key: str, submit_label: str = "Submit") -> tuple[str, str]:
    """Generate form boilerplate code."""
    open_code = f'with st.form(key="{form_key}"):'
    close_code = f'    submitted = st.form_submit_button("{submit_label}")\n    if submitted:\n        st.success("Form submitted!")'
    return open_code, close_code


def generate_column_config(column_name: str, config_type: str, **kwargs) -> str:
    """Generate column configuration for st.dataframe or st.data_editor."""
    config_dict = {"label": column_name}
    config_dict.update(kwargs)

    return f'"{column_name}": st.column_config.{config_type}(**{config_dict})'


def generate_data_display(
    display_type: str, data_var: str = "data", kwargs: Optional[Dict[str, Any]] = None
) -> str:
    """Generate code for data display elements like dataframe, table, etc."""
    kwargs_str = format_kwargs(kwargs or {})
    if kwargs_str:
        return f"st.{display_type}({data_var}, {kwargs_str})"
    return f"st.{display_type}({data_var})"


def generate_metric(label: str, value: Any, kwargs: Optional[Dict[str, Any]] = None) -> str:
    """Generate code for st.metric()."""
    if isinstance(value, str):
        value_str = f'"{value}"'
    else:
        value_str = str(value)

    kwargs_str = format_kwargs(kwargs or {})
    if kwargs_str:
        return f'st.metric("{label}", {value_str}, {kwargs_str})'
    return f'st.metric("{label}", {value_str})'


def generate_layout_context(
    layout_type: str, *args, kwargs: Optional[Dict[str, Any]] = None
) -> str:
    """Generate code for layout context managers (columns, tabs, expander, etc.)."""
    args_str = ", ".join(str(arg) for arg in args)
    kwargs_str = format_kwargs(kwargs or {})

    if args_str and kwargs_str:
        return f"with st.{layout_type}({args_str}, {kwargs_str}):\n    pass"
    elif args_str:
        return f"with st.{layout_type}({args_str}):\n    pass"
    elif kwargs_str:
        return f"with st.{layout_type}({kwargs_str}):\n    pass"
    else:
        return f"with st.{layout_type}():\n    pass"
