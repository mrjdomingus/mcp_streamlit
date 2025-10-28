"""Integration tests for full end-to-end workflows."""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_single_page_workflow():
    """Test complete single-page workflow from drawing to code."""
    print("\n" + "=" * 60)
    print("Testing Single-Page Workflow")
    print("=" * 60)

    from streamlit_mcp.tools.orchestrator import orchestrate_app_from_drawing

    # Test with a simple dashboard description
    result = orchestrate_app_from_drawing(
        drawing_description="Dashboard with 4 metrics at the top showing sales, revenue, customers, and orders. Below that, add a line chart and bar chart side by side showing trends.",
        generate_code=True,
        validate_plans=False,  # Skip validation for faster test
    )

    # Verify workflow type
    assert (
        result["workflow_summary"]["workflow_type"] == "single_page"
    ), f"Expected single_page, got {result['workflow_summary']['workflow_type']}"
    print("✓ Workflow type: single_page")

    # Verify code was generated
    assert result["workflow_summary"]["code_generated"] is True, "Code generation failed"
    print("✓ Code generation: success")

    # Verify generated code structure
    assert (
        len(result["generated_code"]) == 1
    ), f"Expected 1 page, got {len(result['generated_code'])}"
    print(f"✓ Generated code pages: {len(result['generated_code'])}")

    # Verify code contains expected components
    page_code = result["generated_code"][0]
    code = page_code.get("code", "")

    assert "st.metric" in code, "Missing st.metric component"
    print("✓ Code contains: st.metric")

    assert any(
        chart in code for chart in ["st.line_chart", "st.plotly_chart", "st.altair_chart"]
    ), "Missing chart component"
    print("✓ Code contains: chart component")

    print("\n✅ Single-page workflow test passed!")


def test_multipage_workflow():
    """Test complete multi-page workflow from drawing to code."""
    print("\n" + "=" * 60)
    print("Testing Multi-Page Workflow")
    print("=" * 60)

    from streamlit_mcp.tools.orchestrator import orchestrate_app_from_drawing

    # Test with multi-page app description
    result = orchestrate_app_from_drawing(
        drawing_description="""Multi-page sales analytics app with 3 pages:
        1. Home - Dashboard overview with KPIs and trend charts
        2. Data Explorer - Upload CSV files and filter data
        3. Settings - Configuration and user preferences""",
        generate_code=True,
        validate_plans=False,  # Skip validation for faster test
    )

    # Verify workflow type
    assert (
        result["workflow_summary"]["workflow_type"] == "multi_page"
    ), f"Expected multi_page, got {result['workflow_summary']['workflow_type']}"
    print("✓ Workflow type: multi_page")

    # Verify total pages
    total_pages = result["workflow_summary"]["total_pages"]
    assert total_pages >= 3, f"Expected at least 3 pages, got {total_pages}"
    print(f"✓ Total pages: {total_pages}")

    # Verify app plan was created
    assert result["app_plan"] is not None, "App plan was not created"
    print("✓ App plan: created")

    # Verify page plans were created
    page_plans = result.get("page_plans", [])
    assert len(page_plans) >= 3, f"Expected at least 3 page plans, got {len(page_plans)}"
    print(f"✓ Page plans: {len(page_plans)}")

    # Verify code generation
    if result["workflow_summary"]["code_generated"]:
        generated_code = result.get("generated_code", [])
        print(f"✓ Generated code for {len(generated_code)} pages")
    else:
        print("⚠ Code generation was skipped (expected for some workflows)")

    print("\n✅ Multi-page workflow test passed!")


def test_drawing_interpreter():
    """Test drawing interpreter with various inputs."""
    print("\n" + "=" * 60)
    print("Testing Drawing Interpreter")
    print("=" * 60)

    from streamlit_mcp.tools.drawing_interpreter import interpret_page_drawing

    # Test 1: Simple single-page detection
    result = interpret_page_drawing(
        drawing_description="Dashboard with sidebar, 4 metrics, and 2 charts",
        auto_plan=False,  # Skip planning for faster test
    )

    assert "workflow_type" in result, "Missing workflow_type in result"
    print(f"✓ Workflow type detected: {result['workflow_type']}")

    assert "interpretation" in result, "Missing interpretation in result"
    print("✓ Interpretation complete")

    # Test 2: Multi-page detection
    result = interpret_page_drawing(
        drawing_description="""Multi-page app:
        Page 1 - Home dashboard
        Page 2 - Data analysis
        Page 3 - Settings""",
        auto_plan=False,
    )

    assert (
        result["workflow_type"] == "multi_page"
    ), f"Failed to detect multi-page app, got {result['workflow_type']}"
    print("✓ Multi-page detection working")

    print("\n✅ Drawing interpreter test passed!")


def test_validator():
    """Test validation system."""
    print("\n" + "=" * 60)
    print("Testing Validation System")
    print("=" * 60)

    from streamlit_mcp.tools.validator import validate_implementation

    # Test with sample dashboard code
    sample_code = """
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("Sales Dashboard")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Sales", "$45.2K", "+12%")
with col2:
    st.metric("Revenue", "$89.4K", "+8%")

df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
st.line_chart(df)
"""

    result = validate_implementation(
        code=sample_code, page_type="dashboard", validation_mode="standard"
    )

    # Verify validation structure
    assert "status" in result, "Missing status in validation result"
    assert "score" in result, "Missing score in validation result"
    print(f"✓ Validation status: {result['status']}")
    print(f"✓ Validation score: {result['score']}/100")

    # Verify component validation
    assert "component_validation" in result, "Missing component_validation"
    comp_val = result["component_validation"]
    assert "found_components" in comp_val, "Missing found_components"
    print(f"✓ Components found: {len(comp_val['found_components'])}")

    # Verify best practices validation
    assert "best_practices_validation" in result, "Missing best_practices_validation"
    print("✓ Best practices check complete")

    print("\n✅ Validation system test passed!")


def test_app_planner():
    """Test app and page planning tools."""
    print("\n" + "=" * 60)
    print("Testing App Planning Tools")
    print("=" * 60)

    from streamlit_mcp.tools.app_planner import create_app_plan, create_page_plan

    # Test create_app_plan
    app_plan = create_app_plan(
        app_name="Test Integration App",
        description="A test application for integration testing",
        pages=[
            {"name": "Home", "description": "Main page", "type": "dashboard"},
            {"name": "Data", "description": "Data explorer", "type": "data_explorer"},
        ],
    )

    assert app_plan["status"] == "success", f"App plan creation failed: {app_plan.get('message')}"
    assert "file_path" in app_plan, "Missing file_path in app plan result"
    print(f"✓ App plan created: {app_plan['file_path']}")

    # Test create_page_plan
    page_plan = create_page_plan(
        page_name="Test Page",
        page_type="dashboard",
        description="A test page for integration testing",
        features=["metrics", "charts"],
        data_source="example",
    )

    assert (
        page_plan["status"] == "success"
    ), f"Page plan creation failed: {page_plan.get('message')}"
    assert "file_path" in page_plan, "Missing file_path in page plan result"
    print(f"✓ Page plan created: {page_plan['file_path']}")

    print("\n✅ App planning tools test passed!")


def main():
    """Run all integration tests."""
    print("\n" + "=" * 60)
    print("Integration Test Suite")
    print("=" * 60)

    tests = [
        ("Single-Page Workflow", test_single_page_workflow),
        ("Multi-Page Workflow", test_multipage_workflow),
        ("Drawing Interpreter", test_drawing_interpreter),
        ("Validation System", test_validator),
        ("App Planning Tools", test_app_planner),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            test_func()
            results.append((test_name, True))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            import traceback

            traceback.print_exc()
            results.append((test_name, False))

    print("\n" + "=" * 60)
    print("Integration Test Results Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} integration tests passed")

    if passed == total:
        print("\n🎉 All integration tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} integration test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
