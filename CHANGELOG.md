# Changelog

All notable changes to the Streamlit MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-28

### Added
- **Initial Release** - Comprehensive MCP server for building Streamlit applications
- **106 Tools** covering complete Streamlit API surface
  - 11 text elements (title, header, markdown, code, latex, etc.)
  - 10 input widgets (button, slider, text input, file uploader, etc.)
  - 6 data display tools (dataframe, data editor, metric, etc.)
  - 12 chart tools (line, bar, plotly, altair, bokeh, etc.)
  - 9 layout tools (columns, tabs, expander, sidebar, etc.)
  - 10 status elements (progress, spinner, toast, success, error, etc.)
  - 5 media elements (image, audio, video, logo, etc.)
  - 3 chat elements (chat message, chat input, write stream)
  - 5 navigation tools (st.navigation, page link, switch page, etc.)
  - 5 state management tools (session state init/get/set/clear, patterns)
  - 5 execution flow tools (fragments, reruns, stop, form submit)
  - 5 authentication tools (login, logout, user status, patterns, config)
  - 5 data connection tools (SQL, Snowflake, custom connections, config)
  - 2 app planning tools (create_app_plan, create_page_plan)
  - 1 page planner tool (plan_streamlit_page)
  - 11 resource management tools (guides, snippets, templates, docs)

- **Orchestration System** - End-to-end workflow automation
  - `orchestrate_app_from_drawing` - Complete workflow from drawing to validated code
  - Auto-detection of single-page vs multi-page apps
  - Full application planning with individual page plans
  - Code generation for each page
  - Built-in validation with scoring

- **Drawing Interpreter** - Convert sketches and wireframes to code
  - Text description analysis
  - Support for image data (base64)
  - Canvas data support (Excalidraw, Miro)
  - Smart routing to single/multi-page workflows
  - Component and layout detection

- **Validation System** - Code quality and plan alignment checking
  - Component presence validation
  - Best practices compliance (3 strictness levels)
  - Plan alignment verification
  - Scored feedback (0-100)
  - Actionable suggestions

- **Resource Management**
  - Comprehensive caching guides (cache_data vs cache_resource)
  - Architecture guides (execution model, fragments, forms)
  - Code snippets library (caching, navigation, state, data loading)
  - Template library (dashboard, multi-page apps)
  - Official Streamlit documentation integration

- **Code Generation**
  - Automatic import management
  - Proper indentation handling
  - Parameter validation
  - Example data generation
  - Security-focused (path traversal protection, string escaping)

- **Test Suite**
  - 12 comprehensive tests
  - Import verification
  - Tool function testing
  - Security vulnerability tests
  - Drawing interpreter tests
  - 100% test pass rate

- **Documentation**
  - Comprehensive README with examples
  - Tool usage documentation
  - Workflow guides
  - Example applications
  - API quick reference

### Security
- Path traversal protection in template and resource loading
- Safe string escaping using `repr()` for code generation
- Input validation for all tool parameters
- Comprehensive error handling

### Developer Experience
- Clean MCP protocol implementation
- Modular tool organization following Streamlit API structure
- Formatted outputs with progress tracking
- Clear error messages
- Type hints throughout codebase

## [Unreleased]

### Planned Features
- Vision support for actual image analysis (OpenAI/Anthropic APIs)
- Canvas data parsing (Excalidraw, Figma native support)
- Streaming progress for long operations
- Code preview before generation
- Dependency graph analysis
- Runtime management tools
- CLI wrapper for the MCP server
- Additional templates (chat interface, form builder, data explorer)
- Integration tests for full workflows
- Performance benchmarks

---

[0.1.0]: https://github.com/youruser/streamlit-mcp-server/releases/tag/v0.1.0
