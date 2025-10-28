#!/bin/bash
# Streamlit MCP Server - Automated Setup Script
# This script sets up the Streamlit MCP Server environment using UV

set -e  # Exit on error

echo "🔧 Streamlit MCP Server - Setup (UV Edition)"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check for UV installation
echo -e "${BLUE}[1/7] Checking UV installation...${NC}"
if command -v uv &> /dev/null; then
    uv_version=$(uv --version | awk '{print $2}')
    echo -e "${GREEN}✓ UV $uv_version installed${NC}"
else
    echo -e "${YELLOW}⚠ UV not found. Installing UV...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ UV installed successfully${NC}"
        # Source to make uv available in current session
        export PATH="$HOME/.cargo/bin:$PATH"
    else
        echo "✗ Failed to install UV"
        echo "Please install UV manually: https://github.com/astral-sh/uv"
        exit 1
    fi
fi
echo ""

# Step 2: Check Python version
echo -e "${BLUE}[2/7] Checking Python version...${NC}"
python_version=$(python --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo -e "${GREEN}✓ Python $python_version (meets requirement: >= $required_version)${NC}"
else
    echo -e "${YELLOW}⚠ Python $python_version is below required version $required_version${NC}"
    echo "Please upgrade Python before continuing."
    exit 1
fi
echo ""

# Step 3: Install dependencies using UV
echo -e "${BLUE}[3/7] Installing dependencies with UV...${NC}"
echo "  Using: uv sync --all-extras"
uv sync --all-extras
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo "✗ Failed to install dependencies"
    echo "Trying alternative method: uv pip install -e \".[dev]\""
    uv pip install -e ".[dev]"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dependencies installed successfully (fallback method)${NC}"
    else
        echo "✗ Failed to install dependencies with both methods"
        exit 1
    fi
fi
echo ""

# Step 4: Verify installation
echo -e "${BLUE}[4/7] Verifying installation...${NC}"

# Check MCP import
uv run python -c "import mcp" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ MCP package installed${NC}"
else
    echo "✗ MCP package not found"
    exit 1
fi

# Check streamlit_mcp import
uv run python -c "import streamlit_mcp" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Streamlit MCP package installed${NC}"
else
    echo "✗ Streamlit MCP package not found"
    exit 1
fi

# Check server import
uv run python -c "from streamlit_mcp.server import run" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Server can be imported${NC}"
else
    echo "✗ Server import failed"
    exit 1
fi
echo ""

# Step 5: Run tests
echo -e "${BLUE}[5/7] Running tests...${NC}"
uv run pytest tests/ -q --tb=no
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${YELLOW}⚠ Some tests failed (this may be okay for development)${NC}"
fi
echo ""

# Step 6: Check for git repository
echo -e "${BLUE}[6/7] Checking git repository...${NC}"
if [ -d ".git" ]; then
    echo -e "${GREEN}✓ Git repository initialized${NC}"

    # Check if there are uncommitted changes
    if git diff --quiet && git diff --cached --quiet; then
        echo -e "${GREEN}✓ No uncommitted changes${NC}"
    else
        echo -e "${YELLOW}⚠ You have uncommitted changes${NC}"
        echo "  Run 'git status' to see them"
    fi
else
    echo -e "${YELLOW}⚠ Git repository not initialized${NC}"
    echo "  Run 'git init' to initialize"
fi
echo ""

# Step 7: Configuration instructions
echo -e "${BLUE}[7/7] Configuration${NC}"
echo ""
echo "To use with Claude Code:"
echo "1. Add this to your Claude Code config file:"
echo ""
echo '   {'
echo '     "mcpServers": {'
echo '       "streamlit": {'
echo '         "command": "uv",'
echo '         "args": ["run", "python", "-m", "streamlit_mcp.server"],'
echo '         "env": {}'
echo '       }'
echo '     }'
echo '   }'
echo ""
echo "2. Config file locations:"
echo "   - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   - Linux: ~/.config/Claude/claude_desktop_config.json"
echo "   - Windows: %APPDATA%\\Claude\\claude_desktop_config.json"
echo ""
echo "3. Restart Claude Code"
echo ""

# Summary
echo "=============================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=============================================="
echo ""
echo "UV Benefits:"
echo "  ⚡ 10-100x faster than pip"
echo "  🔒 Reliable lockfile-based resolution"
echo "  💾 Disk space efficient (global cache)"
echo ""
echo "Next steps:"
echo "  1. Configure Claude Code (see instructions above)"
echo "  2. Read QUICKSTART.md for usage examples"
echo "  3. Try running: uv run streamlit run examples/simple_app.py"
echo ""
echo "UV Commands:"
echo "  uv run python -m streamlit_mcp.server   # Run MCP server"
echo "  uv run pytest tests/                     # Run tests"
echo "  uv run black .                           # Format code"
echo "  uv run ruff check .                      # Lint code"
echo ""
echo "For help:"
echo "  - README.md - Full documentation"
echo "  - QUICKSTART.md - Quick start guide"
echo "  - examples/ - Example applications"
echo ""
echo "Happy coding with UV! 🚀"
