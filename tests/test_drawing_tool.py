#!/usr/bin/env python3
"""Test script for the drawing interpreter tool."""

import sys
from pathlib import Path
import json

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from streamlit_mcp.tools.drawing_interpreter import interpret_page_drawing, format_interpretation_output


def test_simple_dashboard():
    """Test with a simple dashboard description."""
    print("=" * 80)
    print("TEST 1: Simple Dashboard")
    print("=" * 80)

    result = interpret_page_drawing(
        drawing_description=(
            "Dashboard layout with sidebar on the left containing filters. "
            "Main area has 4 metric cards in a row at the top showing KPIs. "
            "Below that are two charts side by side - a line chart on the left "
            "and a bar chart on the right. At the bottom is a data table."
        ),
        auto_plan=True
    )

    print(format_interpretation_output(result))
    print("\n")


def test_data_explorer():
    """Test with a data explorer description."""
    print("=" * 80)
    print("TEST 2: Data Explorer")
    print("=" * 80)

    result = interpret_page_drawing(
        drawing_description=(
            "Data explorer page with upload button at top. Below that are "
            "filters for selecting categories. Main area shows a data table "
            "with search functionality. At the bottom is a download button "
            "to export the filtered data as CSV."
        ),
        auto_plan=True
    )

    print(format_interpretation_output(result))
    print("\n")


def test_chat_interface():
    """Test with a chat interface description."""
    print("=" * 80)
    print("TEST 3: Chat Interface")
    print("=" * 80)

    result = interpret_page_drawing(
        drawing_description=(
            "Simple chat interface. Main area shows chat messages with "
            "alternating user and assistant bubbles. At the bottom is a "
            "text input field for the user to type messages."
        ),
        auto_plan=True
    )

    print(format_interpretation_output(result))
    print("\n")


def test_with_canvas_data():
    """Test with structured canvas data."""
    print("=" * 80)
    print("TEST 4: With Canvas Data")
    print("=" * 80)

    canvas_data = {
        "elements": [
            {"type": "text", "text": "Upload Button", "x": 50, "y": 50},
            {"type": "rectangle", "label": "Line Chart", "x": 100, "y": 200, "width": 400, "height": 300},
            {"type": "text", "text": "Filter Sidebar", "x": 10, "y": 300},
            {"type": "rectangle", "label": "Metrics Row", "x": 100, "y": 100, "width": 600, "height": 80}
        ]
    }

    result = interpret_page_drawing(
        drawing_description=(
            "Dashboard with sidebar and metrics. Main visualization area "
            "with charts and data upload capability."
        ),
        canvas_data=json.dumps(canvas_data),
        auto_plan=True
    )

    print(format_interpretation_output(result))
    print("\n")


def test_low_confidence():
    """Test with minimal description to trigger low confidence."""
    print("=" * 80)
    print("TEST 5: Low Confidence (Minimal Description)")
    print("=" * 80)

    result = interpret_page_drawing(
        drawing_description="A page with some stuff on it.",
        confidence_threshold="medium",
        auto_plan=True
    )

    print(format_interpretation_output(result))
    print("\n")


if __name__ == "__main__":
    print("\n")
    print("🎨 DRAWING INTERPRETER TOOL TESTS")
    print("=" * 80)
    print("\n")

    try:
        test_simple_dashboard()
        test_data_explorer()
        test_chat_interface()
        test_with_canvas_data()
        test_low_confidence()

        print("=" * 80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
