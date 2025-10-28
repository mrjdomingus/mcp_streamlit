# Streamlit MCP Server

A comprehensive Model Context Protocol (MCP) server for building Streamlit applications with AI assistance. This server provides **106 tools (100% COMPLETE!)** covering Streamlit components, from basic text elements to complex data visualizations, layouts, status indicators, media, chat interfaces, navigation, state management, authentication, and data connections.

## Features

### 🎯 Key Capabilities

- **🎭 End-to-End Orchestration**: Complete workflow from drawing to validated implementation
- **🎨 Drawing Interpreter**: Convert sketches and wireframes directly to code with automatic single/multi-page detection
- **✅ Built-in Validation**: Validate implementations against plans and best practices
- **AI-Powered Page Planner**: Analyzes requirements and generates complete page code with best practices
- **103 Streamlit Tools** (100% COMPLETE! 🎉): Comprehensive coverage of Streamlit components organized by official API structure
- **Code Generation**: Automatic generation of properly formatted Streamlit code
- **Template Library**: Pre-built templates for dashboards, data explorers, chat interfaces, and more
- **Best Practices**: Built-in recommendations for component usage and app architecture
- **Resource Management**: 11 tools for accessing guides, snippets, and templates

### 🔄 New Workflow Tools

#### 1. Orchestration Tool (`orchestrate_app_from_drawing`)
Complete end-to-end workflow:
1. **Get Drawing** → Interpret components and structure
2. **Understand Components** → Extract pages, features, dependencies
3. **Plan Full App** → Always start with full app plan (for multi-page)
4. **Plan Each Page** → Create individual page plans
5. **Execute** → Generate code for each page separately
6. **Validate** → Check against plans and requirements

#### 2. Drawing Interpreter (`interpret_page_drawing`)
Enhanced with multi-page detection:
- Auto-detects single-page vs multi-page apps
- Routes to appropriate planning workflow
- Creates full app plan + individual page plans for multi-page apps
- Generates code with best practices

#### 3. Validation Tool (`validate_implementation`)
Comprehensive code validation:
- Component presence checks
- Best practices compliance
- Plan alignment verification
- Scored feedback (0-100)

### 📊 Component Coverage

#### Display & Interaction (66 tools implemented ✅)
- **Text Elements** (11 tools ✅): titles, headers, markdown, code, LaTeX, dividers, badges
- **Input Widgets** (10 tools ✅): buttons, sliders, text inputs, selectors, file uploaders
- **Data Display** (6 tools ✅): dataframes, data editor, tables, metrics, JSON viewers, column config
- **Charts** (12 tools ✅): line, bar, area, scatter, map, Plotly, Altair, Vega-Lite, Bokeh, PyDeck, Graphviz, Pyplot
- **Layouts** (9 tools ✅): columns, tabs, expanders, containers, sidebar, popover, dialog, empty, forms
- **Status Elements** (10 tools ✅): progress bars, spinners, status containers, toast, success/error/info/warning messages, balloons, snow
- **Media Elements** (5 tools ✅): images, audio, video, logo, link buttons
- **Chat Elements** (3 tools ✅): chat messages, chat input, streaming output

#### Application Logic (25 tools implemented ✅)
- **Navigation** (5 tools ✅): st.navigation(), page links, page switching, query params
- **State Management** (5 tools ✅): session state init/get/set/clear, state patterns
- **Execution Flow** (5 tools ✅): fragments, reruns, stop, form submit, execution patterns
- **Authentication** (5 tools ✅): st.login(), st.logout(), st.user, auth patterns, OIDC config
- **Data Connections** (5 tools ✅): SQL, Snowflake, custom connections, connection config, patterns

## Installation

### Prerequisites

- Python 3.10 or higher
- Claude Code or another MCP client

### Install from Source

**Using UV (Recommended - Fast & Modern):**

```bash
# Clone the repository
cd mcp_streamlit

# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the package with all dependencies
uv sync --all-extras

# Or use the automated setup script
./setup.sh
```

**Using pip (Traditional):**

```bash
# Clone the repository
cd mcp_streamlit

# Install the package
pip install -e ".[dev]"
```

### Why UV?

UV is a modern Python package manager that's:
- ⚡ **10-100x faster** than pip
- 🔒 **More reliable** with lockfile-based resolution
- 💾 **Disk efficient** with global caching
- 🎯 **Better at resolving** complex dependencies

Learn more: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

## Configuration

### For Claude Code

**Using UV (Recommended):**

```json
{
  "mcpServers": {
    "streamlit": {
      "command": "uv",
      "args": ["run", "python", "-m", "streamlit_mcp.server"],
      "env": {}
    }
  }
}
```

**Using Python directly (if not using UV):**

```json
{
  "mcpServers": {
    "streamlit": {
      "command": "python",
      "args": ["-m", "streamlit_mcp.server"],
      "env": {}
    }
  }
}
```

### For Other MCP Clients

The server uses stdio for communication.

**With UV:**
```bash
uv run python -m streamlit_mcp.server
```

**With Python directly:**
```bash
python -m streamlit_mcp.server
```

## Usage

### 🔄 Recommended Workflow: Drawing to Production

#### **NEW: Full Orchestration (Easiest Way!)**

Use the orchestration tool for complete end-to-end workflow:

```
Ask Claude: "Use orchestrate_app_from_drawing with this description:

Multi-page sales dashboard app with 3 pages:
1. Home - Overview dashboard with KPIs and trend charts
2. Data Explorer - Upload and filter sales data
3. Settings - Configuration and user preferences
"
```

The orchestrator will:
1. ✅ Interpret your drawing/description
2. ✅ Auto-detect single vs multi-page app
3. ✅ Create full application plan (for multi-page)
4. ✅ Create individual page plans
5. ✅ Generate code for each page
6. ✅ Validate everything against plans

#### **Alternative: Step-by-Step Workflow**

For more control, use tools individually:

**Step 1: Interpret Drawing**
```
interpret_page_drawing(
  drawing_description="Dashboard with sidebar, 4 metrics, 2 charts, data table"
)
```

**Step 2: Review Plans** (auto-created in ./plans/)
- `full_plan.md` - Overall architecture (multi-page only)
- `page_*.md` - Individual page plans

**Step 3: Generate Code for Each Page**
```
plan_streamlit_page(
  description="Home dashboard page",
  page_type="dashboard"
)
```

**Step 4: Validate Implementation**
```
validate_implementation(
  code=your_page_code,
  page_plan_file="./plans/page_home.md",
  page_type="dashboard"
)
```

### 1. Page Planning (Classic Approach)

Use the AI-powered page planner to get started:

```
Ask Claude: "Plan a dashboard page with metrics, charts, and data filtering"
```

The planner will:
- Analyze your requirements
- Recommend optimal components
- Suggest layout structure
- Generate complete, runnable code

### 2. Component-by-Component Building

Add individual components as needed:

```
Ask Claude: "Add a title saying 'Sales Dashboard'"
→ Generates: st.title("Sales Dashboard")

Ask Claude: "Add a slider from 0 to 100"
→ Generates: st.slider("Label", min_value=0, max_value=100)

Ask Claude: "Add a Plotly chart for the data"
→ Generates: st.plotly_chart(data, use_container_width=True)
```

### 3. Example Workflows

#### Creating a Data Dashboard

```
1. "Plan a dashboard page with data upload, metrics, and charts"
2. "Add file uploader for CSV files"
3. "Add 4 metric cards in columns"
4. "Add a line chart and bar chart side by side"
5. "Add a data table at the bottom"
```

#### Building a Chat Interface

```
1. "Plan a chat page with message history"
2. "Add chat message display"
3. "Add chat input widget"
4. "Add session state for message history"
```

#### Creating a Multi-Page App

```
1. "Plan a multi-page app structure"
2. "Add navigation with pages for Home, Data, Settings"
3. "Add page configuration for wide layout"
```

## Available Tools

### 🔄 Workflow & Planning Tools (NEW!)

#### Orchestration
- `orchestrate_app_from_drawing` - **Complete end-to-end workflow from drawing to validated implementation**
  - Auto-detects single vs multi-page apps
  - Creates full app plan + individual page plans
  - Generates code for each page
  - Validates everything

#### Planning
- `create_app_plan` - Create comprehensive full application plan for multi-page apps
- `create_page_plan` - Create detailed plan for individual pages
- `interpret_page_drawing` - Convert sketches/wireframes to code with smart routing
- `plan_streamlit_page` - AI-powered page designer (original planner)

#### Validation
- `validate_implementation` - Validate code against plans and best practices
  - Component validation
  - Best practices checks
  - Plan alignment verification
  - Scored feedback (0-100)

### Text Elements

- `add_title` - Add a title (st.title)
- `add_header` - Add a header (st.header)
- `add_subheader` - Add a subheader (st.subheader)
- `add_markdown` - Add markdown text (st.markdown)
- `add_text` - Add plain text (st.text)
- `add_caption` - Add caption text (st.caption)
- `add_code` - Display code with syntax highlighting (st.code)
- `add_latex` - Display LaTeX equations (st.latex)
- `add_divider` - Add horizontal divider (st.divider)
- `add_html` - Display raw HTML (st.html)
- `add_badge` - Add a badge (st.badge)

### Input Widgets

- `add_button` - Add a button (st.button)
- `add_checkbox` - Add a checkbox (st.checkbox)
- `add_toggle` - Add a toggle switch (st.toggle)
- `add_radio` - Add radio buttons (st.radio)
- `add_selectbox` - Add a dropdown (st.selectbox)
- `add_multiselect` - Add multi-select (st.multiselect)
- `add_slider` - Add a slider (st.slider)
- `add_select_slider` - Add a select slider (st.select_slider)
- `add_text_input` - Add text input (st.text_input)
- `add_text_area` - Add text area (st.text_area)
- `add_number_input` - Add number input (st.number_input)
- `add_date_input` - Add date picker (st.date_input)
- `add_time_input` - Add time picker (st.time_input)
- `add_file_uploader` - Add file uploader (st.file_uploader)
- `add_camera_input` - Add camera input (st.camera_input)
- `add_color_picker` - Add color picker (st.color_picker)

### Page Planning

- `plan_streamlit_page` - **AI-powered page designer**
  - Analyzes requirements
  - Recommends components
  - Suggests layout
  - Generates complete code
  - Provides alternatives

## Architecture

### Project Structure

```
streamlit_mcp/
├── server.py                   # Main MCP server
├── tools/
│   ├── display/               # Display & interaction tools
│   │   ├── text.py           # Text elements
│   │   ├── widgets.py        # Input widgets
│   │   ├── data.py           # Data display
│   │   ├── charts.py         # Charts & visualizations
│   │   ├── media.py          # Media elements
│   │   ├── layout.py         # Layouts & containers
│   │   ├── chat.py           # Chat elements
│   │   └── status.py         # Status elements
│   ├── logic/                 # Application logic tools
│   │   ├── auth.py           # Authentication
│   │   ├── navigation.py     # Navigation & pages
│   │   ├── execution.py      # Execution flow
│   │   ├── state.py          # State management
│   │   ├── connections.py    # Data connections
│   │   └── components.py     # Custom components
│   ├── config/                # Configuration tools
│   │   ├── page_config.py
│   │   └── theme.py
│   ├── planner.py            # Page planner (KEY TOOL)
│   └── runtime.py            # Server management
├── templates/                 # Template resources
├── resources/                 # MCP resources
└── utils/                     # Utilities
    ├── codegen.py            # Code generation
    └── schemas.py            # JSON schemas
```

### Code Generation

The server uses a sophisticated code generation system that:
- Manages imports automatically
- Handles proper indentation
- Validates parameters
- Generates example data when needed
- Follows Streamlit best practices

### Tool Organization

Tools are organized following Streamlit's official API structure:
1. **Display & Interaction** - Page elements (text, data, charts, widgets, media, layouts, chat, status)
2. **Application Logic** - Authentication, navigation, execution, state, connections, components
3. **Configuration** - Page config, theming, options
4. **Developer Tools** - Testing, CLI

## Examples

### Example 1: Simple Dashboard

```python
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard")

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Sales", "$45.2K", "+12%")
with col2:
    st.metric("Customers", "1,234", "+5%")
with col3:
    st.metric("Orders", "567", "-2%")
with col4:
    st.metric("Revenue", "$89.4K", "+8%")

# Charts
data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
st.line_chart(data)
```

### Example 2: Data Explorer with Upload

```python
import streamlit as st
import pandas as pd

st.title("🔍 Data Explorer")

uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.metric("Rows", len(df))
    st.metric("Columns", len(df.columns))

    st.subheader("Data Preview")
    st.dataframe(df)

    st.subheader("Summary Statistics")
    st.dataframe(df.describe())
```

### Example 3: Chat Interface

```python
import streamlit as st

st.title("💬 Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    response = f"Echo: {prompt}"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
```

## Development

### Running Tests

Run all tests:
```bash
pytest tests/
```

Run individual test files:
```bash
# Comprehensive server and tool tests
python tests/test_server.py

# Security vulnerability verification tests
python tests/test_security_fixes.py

# Drawing interpreter tests
python tests/test_drawing_tool.py
```

### Adding New Tools

1. Create tool function in appropriate module
2. Add tool definition to TOOLS list
3. Register in server.py
4. Update documentation

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Run `black` and `ruff` for formatting

## Roadmap

### Phase 1 ✅ COMPLETE
- ✅ Core server infrastructure
- ✅ Text elements (11 tools)
- ✅ Input widgets (10 tools)
- ✅ Page planner (key tool)
- ✅ Code generation utilities
- ✅ Resource management (11 tools)

### Phase 2 ✅ COMPLETE
- ✅ Charts & visualizations (12 tools)
- ✅ Layouts & containers (9 tools)
- ✅ Data display (6 tools)

### Phase 3 ✅ COMPLETE
- ✅ Status elements (10 tools)
- ✅ Media elements (5 tools)

### Phase 4 ✅ COMPLETE
- ✅ Chat elements (3 tools)
- ✅ Navigation (5 tools)
- ✅ State management (5 tools)
- ✅ Execution flow (5 tools)

### Phase 5 ✅ COMPLETE (100% MILESTONE!)
- ✅ Authentication (5 tools): st.login(), st.logout(), st.user, patterns, OIDC config
- ✅ Data connections (5 tools): SQL, Snowflake, custom connections, config, patterns

**🎉 ALL 103 CORE TOOLS IMPLEMENTED! 100% COMPLETE!**

### Phase 6 (Future Enhancement)
- ⏳ Runtime management (3 tools)
- ⏳ Additional templates
- ⏳ Testing utilities
- ⏳ CLI commands

## Troubleshooting

### Server Won't Start

**Problem**: `ModuleNotFoundError: No module named 'mcp'`

**Solution (with UV):**
```bash
# Install dependencies
uv sync --all-extras

# Verify installation
uv run python -c "from streamlit_mcp.server import run; print('✅ Server ready!')"
```

**Solution (with pip):**
```bash
# Install dependencies
pip install -e ".[dev]"

# Verify installation
python -c "from streamlit_mcp.server import run; print('✅ Server ready!')"
```

**Problem**: `ImportError` or other Python errors

**Solution**:
- Check Python version: `python --version` (need 3.10+)
- With UV: `uv sync --all-extras`
- With pip: Try reinstalling: `pip install -e ".[dev]" --force-reinstall`
- Check for conflicting packages in your environment

### Claude Code Integration Issues

**Problem**: Claude Code doesn't see the MCP server

**Solution**:
1. Check config file location:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Verify JSON syntax (use a JSON validator)

3. Ensure the command path in config is correct:

   **With UV:**
   ```json
   {
     "mcpServers": {
       "streamlit": {
         "command": "uv",
         "args": ["run", "python", "-m", "streamlit_mcp.server"],
         "env": {}
       }
     }
   }
   ```

   **With Python:**
   ```json
   {
     "mcpServers": {
       "streamlit": {
         "command": "python",  // or full path: "/usr/bin/python3"
         "args": ["-m", "streamlit_mcp.server"],
         "env": {}
       }
     }
   }
   ```

4. Restart Claude Code completely

5. Check Claude Code logs/console for error messages

**Problem**: Server starts but commands don't work

**Solution**:
- Verify the server is listed: Ask Claude "List MCP servers"
- Try a simple command: "Use streamlit MCP to add a title"
- Check if other MCP servers work to isolate the issue

### Generated Code Issues

**Problem**: Generated code has syntax errors

**Solution**:
- Use the validator: "Use streamlit MCP validator to check this code"
- Copy the error message and ask Claude to fix it
- Check for missing imports or incorrect indentation

**Problem**: Streamlit raises deprecation warnings

**Solution**:
- Check your Streamlit version: `uv run pip show streamlit` or `pip show streamlit`
- Update if needed (UV): `uv sync --upgrade` or (pip): `pip install --upgrade streamlit`
- Some features require Streamlit ≥1.40.0

**Problem**: Code runs but doesn't match expectations

**Solution**:
- Validate against the plan: Use `validate_implementation` tool
- Check the generated code carefully
- Try regenerating with more specific description

### Orchestrator/Planner Issues

**Problem**: Multi-page app detected as single-page (or vice versa)

**Solution**:
- Be explicit in description: "Multi-page app with 3 pages: ..."
- Use keywords: "pages", "navigation", "multi-page"
- Use workflow_mode parameter: `workflow_mode="multi"` or `"single"`

**Problem**: Generated plans are missing details

**Solution**:
- Provide more detailed descriptions
- Mention specific components: "4 metrics", "line chart", "data table"
- Specify page types: "dashboard", "data_explorer", "chat"

**Problem**: Validation scores are low

**Solution**:
- Check the suggestions in validation output
- Ensure required components are present
- Follow Streamlit best practices (caching, page config, etc.)
- Use appropriate page type for validation

### Common Errors

**Error**: `FileNotFoundError` when loading templates or resources

**Solution**:
- Ensure you're in the project directory
- Check that `streamlit_mcp/resources/` and `streamlit_mcp/templates/` exist
- Reinstall the package: `uv sync` or `pip install -e .`

**Error**: Test failures

**Solution**:
```bash
# Run tests with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_server.py -v

# Check for import issues
python -c "import streamlit_mcp"
```

**Error**: Permission denied errors

**Solution**:
- Check file permissions
- On Unix/Mac: `chmod +x script.sh`
- With UV: Try `uv sync --user` (if supported)
- With pip: Try `pip install --user -e ".[dev]"`

### Performance Issues

**Problem**: Orchestrator is slow

**Solution**:
- Set `validate_plans=False` for faster execution
- Set `generate_code=False` if you only need plans
- Break large apps into smaller chunks

**Problem**: Large apps take too long

**Solution**:
- Use `create_page_plan` for individual pages instead of full orchestration
- Generate pages separately
- Cache intermediate results

### Getting More Help

If problems persist:

1. **Check the logs**: Look for error messages in console output
2. **Run diagnostics**: `python tests/test_server.py`
3. **Verify environment**: `pip list | grep -E "(mcp|streamlit)"`
4. **Review examples**: Check `examples/` directory for working code
5. **Report issues**: Create a GitHub issue with:
   - Error message
   - Steps to reproduce
   - Python version
   - Environment details

### Quick Diagnostics

Run this diagnostic script:

**With UV:**
```bash
# Check UV installation
uv --version

# Check Python version
python --version

# Check package installation
uv run python -c "import streamlit_mcp; print('✅ Package imported')"

# Check MCP installation
uv run python -c "import mcp; print('✅ MCP installed')"

# Run server import test
uv run python -c "from streamlit_mcp.server import run; print('✅ Server can run')"

# Run basic tests
uv run pytest tests/test_server.py::test_imports -v
```

**With pip:**
```bash
# Check Python version
python --version

# Check package installation
python -c "import streamlit_mcp; print('✅ Package imported')"

# Check MCP installation
python -c "import mcp; print('✅ MCP installed')"

# Run server import test
python -c "from streamlit_mcp.server import run; print('✅ Server can run')"

# Run basic tests
pytest tests/test_server.py::test_imports -v
```

## Contributing

Contributions welcome! Areas of focus:
- Implementing remaining tools
- Adding templates
- Improving code generation
- Writing tests
- Documentation

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit GitHub](https://github.com/streamlit/streamlit)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Claude Code](https://claude.com/claude-code)

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions:
- GitHub Issues: [Create an issue]
- Documentation: See README.md
- Examples: See examples/ directory

---

Built with ❤️ for the Streamlit and AI community
