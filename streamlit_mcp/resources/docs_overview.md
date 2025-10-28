
---
title: "Streamlit Documentation Index"
type: "reference"
category: "documentation"
version: "1.0"
mcp_resource_id: "streamlit_docs_index"
last_updated: "2025-10-26"
description: "Comprehensive index of Streamlit documentation for MCP integration"
tags: ["streamlit", "documentation", "api", "reference", "tutorials"]
source_path: "streamlit_mcp/resources/develop_resources"
---

# Streamlit Documentation Index for MCP

> **MCP Resource Type**: Documentation Index  
> **Purpose**: Provide structured access to Streamlit documentation for MCP tools and workflows  
> **Usage**: Reference this index to locate specific documentation, API guides, and tutorials

This resource provides a comprehensive, machine-readable breakdown of the Streamlit documentation in the `develop_resources` folder, with detailed summaries for key files and subtopics to support MCP development and tool integration.

## Quick Navigation

- [API Reference](#api-reference) - Detailed API documentation
- [Concepts](#concepts) - Core architectural concepts  
- [Quick References](#quick-references) - Cheat sheets and references
- [Tutorials](#tutorials) - Step-by-step implementation guides

---

## API Reference (`develop_resources/api-reference/`)
**Path**: `develop_resources/api-reference/`  
**Type**: Technical Documentation  
**MCP Usage**: Primary reference for implementing Streamlit features in MCP tools

Detailed guides and API docs for all major features:

### Caching and State
**Priority**: High | **MCP Relevance**: Critical for performance optimization

- `_index.md`: Overview of caching and state management strategies
- `cache-data.md`: Implementation guide for `@st.cache_data` decorator
- `cache-resource.md`: Resource-level caching with `@st.cache_resource`
- `context.md`: Context management for shared state across components
- `session_state.md`: Persistent user data with `st.session_state`
- `experimental_get_query_params.md`, `experimental_set_query_params.md`, `query_params.md`: URL parameter handling for deep linking

### Charts
**Priority**: Medium | **MCP Relevance**: Data visualization in dashboards

- `_index.md`: Overview of supported chart types and integration patterns
- `altair_chart.md`: Declarative visualization with Altair grammar
- `bar_chart.md`, `line_chart.md`, `area_chart.md`, `scatter_chart.md`: Native chart widgets
- `plotly_chart.md`: Interactive Plotly chart integration
- `pyplot.md`: Matplotlib figure embedding
- `bokeh_chart.md`, `pydeck_chart.md`, `graphviz_chart.md`, `vega_lite_chart.md`: Specialized visualization libraries
- `map.md`: Geospatial data visualization

### Chat
**Priority**: High | **MCP Relevance**: Conversational interfaces

- `_index.md`: Chat system overview and patterns
- `chat-input.md`: User input handling with `st.chat_input`
- `chat-message.md`: Message display with `st.chat_message`

### Command-Line
**Priority**: Low | **MCP Relevance**: Deployment and automation

- `_index.md`: CLI overview for automation workflows
- `cache.md`: Cache management commands
- `config.md`: Configuration via CLI
- `docs.md`: Documentation access
- `hello.md`, `help.md`: Getting started commands
- `init.md`: Project initialization
- `run.md`: App execution parameters
- `version.md`: Version management

### Configuration
**Priority**: Medium | **MCP Relevance**: Environment setup

- `_index.md`: Configuration system overview
- `config-toml.md`: TOML-based configuration files
- `get_option.md`, `set_option.md`: Runtime configuration management
- `set_page_config.md`: Page-level customization (title, icon, layout)

### Connections
**Priority**: High | **MCP Relevance**: Data source integration

- `_index.md`: Connection architecture overview
- `connection.md`: Base connection interface
- `connections-baseconnection.md`, `connections-experimentalbaseconnection.md`: Advanced connection patterns
- `connections-snowflake.md`, `connections-snowpark.md`, `connections-sql.md`: Database-specific implementations
- `experimental-connection.md`: Experimental connection features
- `secrets-toml.md`, `secrets.md`: Secure credential management

### Control Flow
**Priority**: High | **MCP Relevance**: User interaction and app flow

- `_index.md`: Control flow patterns overview
- `dialog.md`: Modal dialog implementation
- `form.md`, `form_submit_button.md`: Form handling and submission
- `fragment.md`: Partial page updates
- `rerun.md`, `experimental_rerun.md`: App state refresh mechanisms
- `stop.md`: Execution control and early termination

### Custom Components
**Priority**: Medium | **MCP Relevance**: Extensibility

- `_index.md`: Component development overview
- `declare_component.md`: Custom component registration
- `html.md`: Raw HTML embedding
- `iframe.md`: External content integration

### Data
**Priority**: High | **MCP Relevance**: Core data handling

- `_index.md`: Data handling patterns and best practices
- `data_editor.md`, `experimental_data_editor.md`: Interactive data editing interfaces
- `dataframe.md`: DataFrame display and manipulation
- `json.md`: JSON data visualization
- `metric.md`: Key performance indicator display
- `table.md`: Tabular data presentation
- `column_config/`: Advanced column configuration options

### Layout
**Priority**: High | **MCP Relevance**: UI organization

- `_index.md`: Layout system overview
- `columns.md`: Multi-column layouts with `st.columns`
- `container.md`: Logical content grouping
- `empty.md`: Placeholder elements
- `expander.md`: Collapsible content sections
- `popover.md`: Contextual information overlays
- `sidebar.md`: Sidebar navigation and controls
- `tabs.md`: Tabbed interface organization

### Media
**Priority**: Low | **MCP Relevance**: Content presentation

- `_index.md`: Media integration overview
- `audio.md`, `video.md`: Audio/video embedding
- `image.md`, `logo.md`: Image display and branding
- `pdf.md`: PDF document embedding

### Navigation
**Priority**: High | **MCP Relevance**: Multi-page applications

- `_index.md`: Navigation system overview
- `navigation.md`: Navigation component configuration
- `page.md`: Page definition and registration
- `switch_page.md`: Programmatic page switching

### Status
**Priority**: Medium | **MCP Relevance**: User feedback

- `_index.md`: Status indication patterns
- `balloons.md`: Success animations
- `error.md`, `exception.md`: Error handling and display

### Testing, Text, User, Widgets, Write Magic
**Priority**: Variable | **MCP Relevance**: Supporting features

- Each category includes `_index.md` with overview and specific feature documentation

---

---

## Concepts (`develop_resources/concepts/`)
**Path**: `develop_resources/concepts/`  
**Type**: Conceptual Documentation  
**MCP Usage**: Understanding architectural patterns and best practices

- `_index.md`: Concepts overview and learning path
- `app-design/`: Design principles, UX patterns, and user-centered development
- `app-testing/`: Testing strategies, unit tests, and quality assurance
- `architecture/`: System architecture, component relationships, and design patterns
- `configuration/`: Configuration management strategies and environment setup
- `connections/`: Connection architecture and data integration patterns
- `custom-components/`: Component development lifecycle and integration
- `multipage-apps/`: Multi-page application architecture and navigation patterns

---

## Quick References (`develop_resources/quick-references/`)
**Path**: `develop_resources/quick-references/`  
**Type**: Reference Material  
**MCP Usage**: Quick lookup for development and troubleshooting

- `_index.md`: Quick reference index and usage guide
- `api-cheat-sheet.md`: Concise API reference with common patterns
- `prerelease-features.md`: Experimental features and upcoming releases
- `release-notes/`: Version history, breaking changes, and migration guides

---

## Tutorials (`develop_resources/tutorials/`)
**Path**: `develop_resources/tutorials/`  
**Type**: Step-by-Step Guides  
**MCP Usage**: Implementation examples and learning resources

- `_index.md`: Tutorial roadmap and learning path
- `authentication/`: User authentication patterns and security implementation
- `databases/`: Database integration, query optimization, and data management
- `elements/`: UI element usage, customization, and best practices
- `execution-flow/`: App lifecycle, state management, and performance optimization
- `llms/`: Large language model integration and conversational interfaces
- `multipage-apps/`: Multi-page application development and deployment
- `theming/`: Custom styling, branding, and visual customization

---

## MCP Integration Guidelines

### For MCP Tool Developers
1. **Reference Format**: Use dot notation for file paths (e.g., `api-reference.caching-and-state.cache-data`)
2. **Priority Levels**: Focus on High priority sections for core functionality
3. **Context Injection**: Include relevant documentation snippets in tool responses
4. **Version Tracking**: Reference the `last_updated` metadata for currency

### For MCP Resource Queries
```
Query Format: "streamlit.{section}.{subsection}.{file}"
Examples:
- streamlit.api-reference.caching-and-state.session_state
- streamlit.concepts.app-design
- streamlit.tutorials.llms

Resource Path: streamlit_mcp/resources/develop_resources/{section}/{file}
```

### Available Tools
1. **get_docs_overview()**: Complete documentation index
2. **get_api_quick_ref(api_name)**: Quick reference for specific APIs (signature, description, example)
3. **search_develop_docs(query, mode="quick")**: Search documentation
   - `mode="quick"`: Brief file list with descriptions (recommended for initial lookups)
   - `mode="detailed"`: Full context around matches (for implementation details)

### Common Use Cases
- **Dashboard Creation**: Focus on `data`, `charts`, `layout`, `caching-and-state`
- **Chat Applications**: Prioritize `chat`, `control-flow`, `session_state`
- **Data Analysis**: Emphasize `connections`, `data`, `charts`, `caching-and-state`
- **Multi-page Apps**: Reference `navigation`, `multipage-apps`, `concepts.multipage-apps`

---

## Resource Metadata
- **Total Files**: 100+ documentation files
- **Coverage**: Complete Streamlit API and conceptual documentation
- **Format**: Markdown with frontmatter metadata
- **Maintenance**: Auto-synced with official documentation
- **Access Pattern**: Hierarchical browsing and direct file access

---

## Usage in MCP Tools

### Direct File Access
```python
# Example MCP tool usage
doc_path = get_resource("streamlit_docs_index")
section = doc_path.get_section("api-reference.caching-and-state")
```

### Context Enhancement
- Include relevant documentation snippets in responses
- Link to specific files for detailed implementation guidance
- Provide contextual examples from tutorials

### Error Resolution
- Reference troubleshooting sections in `concepts` and `tutorials`
- Link to API documentation for parameter clarification
- Suggest related examples and patterns

---

*This resource is designed to be a living index for MCP documentation needs. Update the `last_updated` field when making changes.*