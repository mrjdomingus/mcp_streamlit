"""Simple test script to verify the MCP server structure."""

import sys
from pathlib import Path
import importlib.util

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")

    modules = [
        "streamlit_mcp.server",
        "streamlit_mcp.tools.display.text",
        "streamlit_mcp.tools.display.widgets",
        "streamlit_mcp.tools.display.data",
        "streamlit_mcp.tools.display.charts",
        "streamlit_mcp.tools.display.layout",
        "streamlit_mcp.tools.display.status",
        "streamlit_mcp.tools.display.media",
        "streamlit_mcp.tools.display.chat",
        "streamlit_mcp.tools.logic.navigation",
        "streamlit_mcp.tools.logic.state",
        "streamlit_mcp.tools.logic.execution",
        "streamlit_mcp.tools.logic.auth",
        "streamlit_mcp.tools.logic.connections",
        "streamlit_mcp.tools.planner",
        "streamlit_mcp.tools.resources",
        "streamlit_mcp.utils.codegen",
        "streamlit_mcp.utils.schemas",
    ]

    for module_name in modules:
        try:
            module = importlib.import_module(module_name)
            print(f"✓ {module_name}")
        except ImportError as e:
            print(f"✗ {module_name}: {e}")
            assert False, f"Failed to import {module_name}: {e}"

    print("✓ All imports successful")


def test_tool_functions():
    """Test that tool functions work."""
    print("\nTesting tool functions...")

    from streamlit_mcp.tools.display import text, widgets, data, charts, layout, status, media, chat
    from streamlit_mcp.tools.logic import navigation, state, execution, auth, connections
    from streamlit_mcp.tools import planner

    # Test text tools
    try:
        result = text.add_title("Test Title")
        assert 'st.title("Test Title")' in result
        print("✓ text.add_title")
    except Exception as e:
        print(f"✗ text.add_title: {e}")
        assert False, f"text.add_title failed: {e}"

    try:
        result = text.add_markdown("# Test Markdown")
        assert "st.markdown" in result
        print("✓ text.add_markdown")
    except Exception as e:
        print(f"✗ text.add_markdown: {e}")
        assert False, f"text.add_markdown failed: {e}"

    # Test widget tools
    try:
        result = widgets.add_button("Click Me")
        assert 'st.button("Click Me")' in result
        print("✓ widgets.add_button")
    except Exception as e:
        print(f"✗ widgets.add_button: {e}")
        assert False, f"widgets.add_button failed: {e}"

    try:
        result = widgets.add_slider("Test Slider")
        assert "st.slider" in result
        print("✓ widgets.add_slider")
    except Exception as e:
        print(f"✗ widgets.add_slider: {e}")
        assert False, f"widgets.add_slider failed: {e}"

    # Test data display tools
    try:
        result = data.add_dataframe("df")
        assert "st.dataframe(df" in result
        print("✓ data.add_dataframe")
    except Exception as e:
        print(f"✗ data.add_dataframe: {e}")
        assert False, f"data.add_dataframe failed: {e}"

    try:
        result = data.add_metric("Revenue", "$1000", delta="+10%")
        assert "st.metric" in result
        print("✓ data.add_metric")
    except Exception as e:
        print(f"✗ data.add_metric: {e}")
        assert False, f"data.add_metric failed: {e}"

    # Test chart tools
    try:
        result = charts.add_line_chart("df")
        assert "st.line_chart" in result
        print("✓ charts.add_line_chart")
    except Exception as e:
        print(f"✗ charts.add_line_chart: {e}")
        assert False, f"charts.add_line_chart failed: {e}"

    try:
        result = charts.add_plotly_chart("fig")
        assert "st.plotly_chart(fig" in result
        print("✓ charts.add_plotly_chart")
    except Exception as e:
        print(f"✗ charts.add_plotly_chart: {e}")
        assert False, f"charts.add_plotly_chart failed: {e}"

    # Test layout tools
    try:
        result = layout.add_columns(3)
        assert "st.columns" in result
        print("✓ layout.add_columns")
    except Exception as e:
        print(f"✗ layout.add_columns: {e}")
        assert False, f"layout.add_columns failed: {e}"

    try:
        result = layout.add_tabs(["Tab 1", "Tab 2"])
        assert "st.tabs" in result
        print("✓ layout.add_tabs")
    except Exception as e:
        print(f"✗ layout.add_tabs: {e}")
        assert False, f"layout.add_tabs failed: {e}"

    # Test status tools
    try:
        result = status.add_progress(0.5)
        assert "st.progress" in result
        print("✓ status.add_progress")
    except Exception as e:
        print(f"✗ status.add_progress: {e}")
        assert False, f"status.add_progress failed: {e}"

    try:
        result = status.add_success("Operation completed!")
        assert "st.success" in result
        print("✓ status.add_success")
    except Exception as e:
        print(f"✗ status.add_success: {e}")
        assert False, f"status.add_success failed: {e}"

    # Test media tools
    try:
        result = media.add_image("image.png")
        assert "st.image" in result
        print("✓ media.add_image")
    except Exception as e:
        print(f"✗ media.add_image: {e}")
        assert False, f"media.add_image failed: {e}"

    try:
        result = media.add_link_button("Visit", "https://example.com")
        assert "st.link_button" in result
        print("✓ media.add_link_button")
    except Exception as e:
        print(f"✗ media.add_link_button: {e}")
        assert False, f"media.add_link_button failed: {e}"

    # Test chat tools
    try:
        result = chat.add_chat_message("user")
        assert "st.chat_message" in result
        print("✓ chat.add_chat_message")
    except Exception as e:
        print(f"✗ chat.add_chat_message: {e}")
        assert False, f"chat.add_chat_message failed: {e}"

    try:
        result = chat.add_chat_input("Type a message")
        assert "st.chat_input" in result
        print("✓ chat.add_chat_input")
    except Exception as e:
        print(f"✗ chat.add_chat_input: {e}")
        assert False, f"chat.add_chat_input failed: {e}"

    # Test navigation tools
    try:
        result = navigation.add_navigation(["Home", "Settings"])
        assert "st.navigation" in result
        print("✓ navigation.add_navigation")
    except Exception as e:
        print(f"✗ navigation.add_navigation: {e}")
        assert False, f"navigation.add_navigation failed: {e}"

    try:
        result = navigation.switch_page("pages/settings.py")
        assert "st.switch_page" in result
        print("✓ navigation.switch_page")
    except Exception as e:
        print(f"✗ navigation.switch_page: {e}")
        assert False, f"navigation.switch_page failed: {e}"

    # Test state management tools
    try:
        result = state.init_session_state("counter", 0)
        assert "st.session_state" in result
        print("✓ state.init_session_state")
    except Exception as e:
        print(f"✗ state.init_session_state: {e}")
        assert False, f"state.init_session_state failed: {e}"

    try:
        result = state.manage_state_pattern("counter")
        assert "count" in result
        print("✓ state.manage_state_pattern")
    except Exception as e:
        print(f"✗ state.manage_state_pattern: {e}")
        assert False, f"state.manage_state_pattern failed: {e}"

    # Test execution flow tools
    try:
        result = execution.add_fragment()
        assert "@st.fragment" in result
        print("✓ execution.add_fragment")
    except Exception as e:
        print(f"✗ execution.add_fragment: {e}")
        assert False, f"execution.add_fragment failed: {e}"

    try:
        result = execution.add_rerun()
        assert "st.rerun()" in result
        print("✓ execution.add_rerun")
    except Exception as e:
        print(f"✗ execution.add_rerun: {e}")
        assert False, f"execution.add_rerun failed: {e}"

    # Test authentication tools
    try:
        result = auth.add_login()
        assert "st.login()" in result
        print("✓ auth.add_login")
    except Exception as e:
        print(f"✗ auth.add_login: {e}")
        assert False, f"auth.add_login failed: {e}"

    try:
        result = auth.add_logout()
        assert "st.logout()" in result
        print("✓ auth.add_logout")
    except Exception as e:
        print(f"✗ auth.add_logout: {e}")
        assert False, f"auth.add_logout failed: {e}"

    try:
        result = auth.check_user_status()
        assert "st.user.is_logged_in" in result
        print("✓ auth.check_user_status")
    except Exception as e:
        print(f"✗ auth.check_user_status: {e}")
        assert False, f"auth.check_user_status failed: {e}"

    # Test connection tools
    try:
        result = connections.add_sql_connection()
        assert "st.connection" in result
        print("✓ connections.add_sql_connection")
    except Exception as e:
        print(f"✗ connections.add_sql_connection: {e}")
        assert False, f"connections.add_sql_connection failed: {e}"

    try:
        result = connections.add_snowflake_connection()
        assert "st.connection" in result
        print("✓ connections.add_snowflake_connection")
    except Exception as e:
        print(f"✗ connections.add_snowflake_connection: {e}")
        assert False, f"connections.add_snowflake_connection failed: {e}"

    try:
        result = connections.add_custom_connection("my_conn")
        assert "st.connection" in result
        print("✓ connections.add_custom_connection")
    except Exception as e:
        print(f"✗ connections.add_custom_connection: {e}")
        assert False, f"connections.add_custom_connection failed: {e}"

    # Test planner
    try:
        result = planner.plan_streamlit_page(
            description="A simple dashboard",
            page_type="dashboard",
            features=["metrics", "charts"],
            data_source="example",
        )
        assert "layout" in result
        assert "components" in result
        assert "code" in result
        print("✓ planner.plan_streamlit_page")
    except Exception as e:
        print(f"✗ planner.plan_streamlit_page: {e}")
        assert False, f"planner.plan_streamlit_page failed: {e}"

    # Test app planner
    try:
        from streamlit_mcp.tools import app_planner

        # Test create_app_plan
        result = app_planner.create_app_plan(
            app_name="Test App",
            description="A test application",
            pages=[
                {"name": "Home", "description": "Main page", "type": "dashboard"},
                {"name": "Settings", "description": "Settings page", "type": "form"},
            ],
        )
        assert result["status"] == "success"
        assert "file_path" in result
        print("✓ app_planner.create_app_plan")
    except Exception as e:
        print(f"✗ app_planner.create_app_plan: {e}")
        assert False, f"app_planner.create_app_plan failed: {e}"

    try:
        # Test create_page_plan
        result = app_planner.create_page_plan(
            page_name="Test Page",
            page_type="dashboard",
            description="A test page",
            features=["metrics", "charts"],
            data_source="example",
        )
        assert result["status"] == "success"
        assert "file_path" in result
        print("✓ app_planner.create_page_plan")
    except Exception as e:
        print(f"✗ app_planner.create_page_plan: {e}")
        assert False, f"app_planner.create_page_plan failed: {e}"

    print("✓ All tool functions working correctly")


def test_tool_definitions():
    """Test that tool definitions are valid."""
    print("\nTesting tool definitions...")

    from streamlit_mcp.tools.display import text, widgets, data, charts, layout, status, media, chat
    from streamlit_mcp.tools.logic import navigation, state, execution, auth, connections
    from streamlit_mcp.tools import planner

    # Check text tools
    assert len(text.TOOLS) == 11, f"Expected 11 text tools, got {len(text.TOOLS)}"
    print(f"✓ text.TOOLS ({len(text.TOOLS)} tools)")

    # Check widget tools
    assert len(widgets.TOOLS) >= 10, f"Expected at least 10 widget tools, got {len(widgets.TOOLS)}"
    print(f"✓ widgets.TOOLS ({len(widgets.TOOLS)} tools)")

    # Check data display tools
    assert len(data.TOOLS) == 6, f"Expected 6 data tools, got {len(data.TOOLS)}"
    print(f"✓ data.TOOLS ({len(data.TOOLS)} tools)")

    # Check chart tools
    assert len(charts.TOOLS) == 12, f"Expected 12 chart tools, got {len(charts.TOOLS)}"
    print(f"✓ charts.TOOLS ({len(charts.TOOLS)} tools)")

    # Check layout tools
    assert len(layout.TOOLS) == 9, f"Expected 9 layout tools, got {len(layout.TOOLS)}"
    print(f"✓ layout.TOOLS ({len(layout.TOOLS)} tools)")

    # Check status tools
    assert len(status.TOOLS) == 10, f"Expected 10 status tools, got {len(status.TOOLS)}"
    print(f"✓ status.TOOLS ({len(status.TOOLS)} tools)")

    # Check media tools
    assert len(media.TOOLS) == 5, f"Expected 5 media tools, got {len(media.TOOLS)}"
    print(f"✓ media.TOOLS ({len(media.TOOLS)} tools)")

    # Check chat tools
    assert len(chat.TOOLS) == 3, f"Expected 3 chat tools, got {len(chat.TOOLS)}"
    print(f"✓ chat.TOOLS ({len(chat.TOOLS)} tools)")

    # Check navigation tools
    assert len(navigation.TOOLS) == 5, f"Expected 5 navigation tools, got {len(navigation.TOOLS)}"
    print(f"✓ navigation.TOOLS ({len(navigation.TOOLS)} tools)")

    # Check state management tools
    assert len(state.TOOLS) == 5, f"Expected 5 state tools, got {len(state.TOOLS)}"
    print(f"✓ state.TOOLS ({len(state.TOOLS)} tools)")

    # Check execution flow tools
    assert len(execution.TOOLS) == 5, f"Expected 5 execution tools, got {len(execution.TOOLS)}"
    print(f"✓ execution.TOOLS ({len(execution.TOOLS)} tools)")

    # Check authentication tools
    assert len(auth.TOOLS) == 5, f"Expected 5 auth tools, got {len(auth.TOOLS)}"
    print(f"✓ auth.TOOLS ({len(auth.TOOLS)} tools)")

    # Check connection tools
    assert len(connections.TOOLS) == 5, f"Expected 5 connection tools, got {len(connections.TOOLS)}"
    print(f"✓ connections.TOOLS ({len(connections.TOOLS)} tools)")

    # Check planner tool
    assert planner.TOOL["name"] == "plan_streamlit_page"
    print("✓ planner.TOOL")

    # Check app planner tools
    from streamlit_mcp.tools import app_planner

    assert (
        len(app_planner.TOOLS) == 2
    ), f"Expected 2 app planner tools, got {len(app_planner.TOOLS)}"
    print(f"✓ app_planner.TOOLS ({len(app_planner.TOOLS)} tools)")

    # Calculate total tools
    total = (
        len(text.TOOLS)
        + len(widgets.TOOLS)
        + len(data.TOOLS)
        + len(charts.TOOLS)
        + len(layout.TOOLS)
        + len(status.TOOLS)
        + len(media.TOOLS)
        + len(chat.TOOLS)
        + len(navigation.TOOLS)
        + len(state.TOOLS)
        + len(execution.TOOLS)
        + len(auth.TOOLS)
        + len(connections.TOOLS)
    )
    print(f"\n📊 Total component tools: {total}")
    print("   + 2 app planner tools")
    print("   + 1 planner tool")
    print("   + 11 resource tools")
    print(f"   = {total + 2 + 1 + 11} total tools")

    print("✓ All tool definitions valid")


def test_code_generation():
    """Test code generation utilities."""
    print("\nTesting code generation...")

    from streamlit_mcp.utils.codegen import (
        StreamlitCodeGenerator,
        format_kwargs,
    )

    # Test code generator
    try:
        gen = StreamlitCodeGenerator()
        gen.add_import("import pandas as pd")
        gen.add_code("df = pd.DataFrame()")
        code = gen.generate()
        assert "import streamlit as st" in code
        assert "import pandas as pd" in code
        assert "df = pd.DataFrame()" in code
        print("✓ StreamlitCodeGenerator")
    except Exception as e:
        print(f"✗ StreamlitCodeGenerator: {e}")
        assert False, f"StreamlitCodeGenerator failed: {e}"

    # Test format_kwargs
    try:
        result = format_kwargs({"key": "value", "num": 42, "flag": True})
        assert 'key="value"' in result
        assert "num=42" in result
        assert "flag=True" in result
        print("✓ format_kwargs")
    except Exception as e:
        print(f"✗ format_kwargs: {e}")
        assert False, f"format_kwargs failed: {e}"

    print("✓ All code generation utilities working")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Streamlit MCP Server Test Suite")
    print("=" * 60)

    tests = [
        ("Import Test", test_imports),
        ("Tool Functions Test", test_tool_functions),
        ("Tool Definitions Test", test_tool_definitions),
        ("Code Generation Test", test_code_generation),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
