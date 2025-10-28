#!/bin/bash

# Streamlit MCP Server - Environment Activation Script
# Usage: source activate.sh

echo "🚀 Activating Streamlit MCP Server environment..."

# Activate the UV virtual environment
source .venv/bin/activate

echo "✅ Virtual environment activated"
echo "📦 Available packages:"
echo "   - Streamlit $(python -c 'import streamlit; print(streamlit.__version__)')"
echo "   - MCP library"
echo "   - Pandas $(python -c 'import pandas; print(pandas.__version__)')"
echo "   - Plotly $(python -c 'import plotly; print(plotly.__version__)')"

echo ""
echo "🔧 Available commands:"
echo "   uv run streamlit-mcp          # Run MCP server"
echo "   uv run python -m streamlit    # Run Streamlit apps"
echo "   uv run pytest                 # Run tests"
echo "   uv run black .                # Format code"
echo "   uv run ruff .                 # Lint code"

echo ""
echo "📚 Quick test commands:"
echo "   uv run python -c \"from streamlit_mcp.tools.resources import get_api_quick_ref; print(get_api_quick_ref('button'))\""
echo "   uv run python -c \"from streamlit_mcp.tools.resources import search_develop_docs; print(search_develop_docs('cache', mode='quick'))\""

echo ""
echo "🎉 Environment ready! Use 'deactivate' to exit."