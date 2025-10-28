# Streamlit MCP Server - Examples

This directory contains example applications and configuration files.

## Files

### Application Examples

#### `simple_app.py`
A basic dashboard demonstrating:
- Page configuration
- Metrics display in columns
- Line and bar charts
- Data tables
- Layout components

**To run:**
```bash
streamlit run examples/simple_app.py
```

#### `dashboard_example.py`
More comprehensive dashboard (already exists in this directory)

### Configuration

#### `claude_code_config.json`
Example Claude Code MCP configuration file (configured for UV).

**To use:**
1. Copy contents to your Claude Code config file
2. If not using UV, change `"command": "uv"` to `"command": "python"` and remove `"run"` from args
3. Restart Claude Code
4. Verify connection with: "List MCP servers"

**Config file locations:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**UV vs Python:**
- **With UV** (recommended): `"command": "uv", "args": ["run", "python", "-m", "streamlit_mcp.server"]`
- **With Python**: `"command": "python", "args": ["-m", "streamlit_mcp.server"]`

## Usage Examples

### 1. Generate a Dashboard

Ask Claude Code:
```
Use streamlit MCP orchestrator to create a dashboard with:
- Title "My Dashboard"
- 3 metrics showing KPIs
- A line chart
- A data table
```

### 2. Build Multi-Page App

Ask Claude Code:
```
Use streamlit MCP orchestrator for multi-page app:
1. Home - Overview with metrics
2. Data - Data explorer with file upload
3. Settings - Configuration page
```

### 3. Component by Component

Ask Claude Code:
```
1. "Add title 'Sales App'"
2. "Create 4 columns"
3. "In each column add a metric"
4. "Add line chart below"
```

## Example Prompts

### For Dashboards
- "Create a financial dashboard with metrics and charts"
- "Build a monitoring dashboard with real-time indicators"
- "Design an analytics dashboard with filters and visualizations"

### For Data Apps
- "Create a data explorer with CSV upload and filtering"
- "Build a data analysis app with pandas operations"
- "Design a data visualization tool with multiple chart types"

### For Chat Apps
- "Create a chatbot interface with message history"
- "Build a Q&A app with chat interface"
- "Design a conversation interface with streaming responses"

## Tips

1. **Be specific**: Describe layout, components, and data clearly
2. **Use keywords**: Mention "dashboard", "data_explorer", "chat" for better detection
3. **Iterate**: Start simple, then add features incrementally
4. **Validate**: Use the validation tool to check generated code

## Next Steps

- Read `../QUICKSTART.md` for detailed setup
- Check `../README.md` for full documentation
- Browse `../streamlit_mcp/templates/` for more examples
- Run `../tests/` to see usage patterns
