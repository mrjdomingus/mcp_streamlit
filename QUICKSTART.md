# Quick Start Guide - Streamlit MCP Server

Get up and running with the Streamlit MCP Server in under 5 minutes!

## Prerequisites

- Python 3.10 or higher
- Claude Code (or another MCP-compatible client)
- Basic familiarity with Streamlit (helpful but not required)

## Installation

### 1. Install UV (Recommended)

UV is a modern, fast Python package manager. Install it first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install the Package

**Option A: Using UV (Fast & Recommended)**

```bash
cd mcp_streamlit

# Automated setup (installs UV if needed, runs tests)
./setup.sh

# Or manual installation
uv sync --all-extras
```

**Option B: Using pip (Traditional)**

```bash
cd mcp_streamlit
pip install -e ".[dev]"
```

This will install:
- The MCP server and all dependencies
- Development tools (pytest, black, ruff, mypy)

### 3. Verify Installation

**With UV:**
```bash
# Test that the server can be imported
uv run python -c "from streamlit_mcp.server import run; print('✅ Server ready!')"

# Run tests to ensure everything works
uv run pytest tests/ -v
```

**With pip:**
```bash
# Test that the server can be imported
python -c "from streamlit_mcp.server import run; print('✅ Server ready!')"

# Run tests to ensure everything works
pytest tests/ -v
```

You should see all tests passing.

### Why UV?

- ⚡ **10-100x faster** than pip
- 🔒 **Reliable** lockfile-based resolution
- 💾 **Efficient** global caching
- 🎯 **Better** dependency resolution

## Configuration

### For Claude Code

1. Add to your Claude Code MCP settings file (usually `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

**Using UV (Recommended):**

```json
{
  "mcpServers": {
    "streamlit": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "-m",
        "streamlit_mcp.server"
      ],
      "env": {}
    }
  }
}
```

**Using Python directly:**

```json
{
  "mcpServers": {
    "streamlit": {
      "command": "python",
      "args": [
        "-m",
        "streamlit_mcp.server"
      ],
      "env": {}
    }
  }
}
```

2. Restart Claude Code

3. Verify the server is connected:
   - In Claude Code, type: "List available MCP servers"
   - You should see `streamlit` in the list

### For Other MCP Clients

The server uses stdio for communication. Configure your client to run:

**With UV:**
```bash
uv run python -m streamlit_mcp.server
```

**With Python:**
```bash
python -m streamlit_mcp.server
```

## Your First Streamlit App

### Method 1: Use the Orchestrator (Recommended)

Ask Claude Code:

```
Use the streamlit MCP to orchestrate an app from this drawing:

Dashboard with:
- Title "Sales Dashboard"
- 4 metrics showing Sales, Revenue, Customers, Orders
- A line chart showing trends over time
- A data table at the bottom
```

The orchestrator will:
1. Interpret your description
2. Create a plan
3. Generate complete, runnable code
4. Validate the implementation

### Method 2: Component-by-Component

Ask Claude Code step by step:

```
1. "Use streamlit MCP to add a title 'My First App'"
2. "Add 3 columns"
3. "In each column, add a metric"
4. "Add a line chart below the metrics"
```

### Method 3: Use the Page Planner

Ask Claude Code:

```
Use the streamlit MCP planner to create a dashboard page with:
- Metrics for KPIs
- Interactive charts
- Data filtering
```

## Example Workflows

### Create a Simple Dashboard

```
Use streamlit MCP orchestrator with this description:

Single-page dashboard:
- Header with app title
- 4 KPI metrics in a row
- 2 charts side by side (line and bar)
- Data table showing raw data
```

### Create a Multi-Page App

```
Use streamlit MCP orchestrator for a multi-page app:

1. Home - Overview dashboard with metrics and charts
2. Data Explorer - Upload CSV and filter data
3. Settings - Configuration options
```

### Build a Chat Interface

```
Use streamlit MCP planner to create a chat page with:
- Message history display
- Chat input at the bottom
- Session state for messages
```

## Running Your App

1. Save the generated code to a file (e.g., `app.py`)

2. Run with Streamlit:

```bash
streamlit run app.py
```

3. Your app will open in your browser at `http://localhost:8501`

## Common Commands

### Discovery

- **List all tools**: "What tools does the streamlit MCP provide?"
- **Get help**: "How do I use the streamlit MCP orchestrator?"
- **View examples**: "Show me examples of streamlit MCP usage"

### Code Generation

- **Single component**: "Add a st.metric showing revenue"
- **Layout**: "Create a 3-column layout"
- **Charts**: "Add a Plotly scatter chart"
- **Forms**: "Create a form with text input and submit button"

### Resources

- **Get guides**: "Show me the caching guide from streamlit MCP"
- **Code snippets**: "Get navigation code snippets"
- **Templates**: "Load the dashboard template"

## Next Steps

### Learn More

1. **Read the full README**: `README.md` for comprehensive documentation
2. **Explore examples**: Check `examples/` directory
3. **Browse templates**: Check `streamlit_mcp/templates/`
4. **Read guides**: Access via MCP resources or `streamlit_mcp/resources/guides/`

### Advanced Usage

1. **Validation**: Use `validate_implementation` to check your code
2. **Planning**: Create detailed plans with `create_app_plan` and `create_page_plan`
3. **Customization**: Modify generated code to fit your needs

### Get Help

- **Documentation**: See `README.md`
- **Examples**: Browse `examples/` directory
- **Tests**: Look at `tests/` for usage patterns
- **Issues**: Report problems on GitHub

## Tips & Tricks

1. **Be specific in descriptions**: "4 metrics in columns" is better than "some metrics"

2. **Use page types**: Mention "dashboard", "data_explorer", "chat", etc. for better results

3. **Iterate**: Start simple, then ask for additions:
   - "Add a title"
   - "Now add 3 metrics below it"
   - "Add a chart under the metrics"

4. **Validate often**: Use the validation tool to check your code

5. **Reference examples**: Ask "Show me an example of X" before implementing

## Troubleshooting

### Server won't start

- Check Python version: `python --version` (need 3.10+)
- **With UV**:
  - Verify dependencies: `uv pip list | grep mcp`
  - Try reinstalling: `uv sync --all-extras`
- **With pip**:
  - Verify dependencies: `pip list | grep mcp`
  - Try reinstalling: `pip install -e ".[dev]" --force-reinstall`

### Claude Code doesn't see the server

- Check config file location
- Verify JSON syntax in config
- Restart Claude Code
- Check logs in Claude Code console

### Generated code has errors

- Use the validator: "Validate this code with streamlit MCP"
- Check Streamlit version: `pip show streamlit`
- Review error messages carefully
- Ask for specific fixes

## Quick Reference

### Tool Categories

- **Text**: 11 tools for text elements
- **Widgets**: 10 tools for input controls
- **Data**: 6 tools for data display
- **Charts**: 12 tools for visualizations
- **Layouts**: 9 tools for page structure
- **Status**: 10 tools for feedback
- **Media**: 5 tools for images/audio/video
- **Chat**: 3 tools for chat interfaces
- **Navigation**: 5 tools for multi-page apps
- **State**: 5 tools for session state
- **Execution**: 5 tools for control flow
- **Auth**: 5 tools for authentication
- **Connections**: 5 tools for data sources
- **Planning**: 3 tools for app design
- **Resources**: 11 tools for guides/templates

### Most Used Tools

1. `orchestrate_app_from_drawing` - Complete end-to-end workflow
2. `plan_streamlit_page` - AI-powered page designer
3. `validate_implementation` - Code validation
4. `create_app_plan` - Full app planning
5. `create_page_plan` - Individual page planning

---

**Ready to build?** Try this:

```
Use streamlit MCP orchestrator to create a dashboard showing:
- 3 metrics (Sales, Revenue, Customers)
- A line chart
- A bar chart
- A data table
```

Happy coding! 🚀
