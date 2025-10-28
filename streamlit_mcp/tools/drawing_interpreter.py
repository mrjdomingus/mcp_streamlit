"""Drawing interpretation tool - converts page sketches to planner parameters."""

import json
from typing import Dict, Any, Optional, List
from ..utils.vision_helpers import (
    analyze_drawing_text,
    analyze_image_layout_structure,
    create_enhanced_description,
)
from .planner import plan_streamlit_page
from .app_planner import create_app_plan, create_page_plan


def _detect_multipage_intent(
    description: str, canvas_dict: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Detect if the drawing describes a multi-page app or single page.

    Returns dict with:
    - is_multipage: bool
    - pages: List[Dict] if multipage, else []
    - app_name: str if multipage
    """
    description_lower = description.lower()

    # Keywords that indicate multi-page
    multipage_indicators = [
        "multi-page",
        "multipage",
        "multiple pages",
        "navigation",
        "home page",
        "dashboard page",
        "settings page",
        "pages:",
        "page 1",
        "page 2",
        "page 3",
        "sidebar navigation",
        "nav menu",
        "menu items",
    ]

    # Check for page indicators
    has_multipage_keywords = any(
        indicator in description_lower for indicator in multipage_indicators
    )

    # Try to extract page names
    pages = []
    app_name = "App"

    if has_multipage_keywords:
        # Look for explicit page mentions
        lines = description.split("\n")
        for line in lines:
            line_lower = line.lower()
            # Match patterns like "Home page", "Dashboard:", "1. Settings"
            if any(word in line_lower for word in ["page", "screen", "view"]):
                # Extract page name
                for page_type in [
                    "home",
                    "dashboard",
                    "settings",
                    "about",
                    "data",
                    "analytics",
                    "profile",
                    "admin",
                    "reports",
                    "visualizations",
                    "chat",
                ]:
                    if page_type in line_lower:
                        page_name = page_type.title()
                        if not any(p["name"] == page_name for p in pages):
                            pages.append(
                                {
                                    "name": page_name,
                                    "description": line.strip(),
                                    "type": _infer_page_type(page_type),
                                }
                            )

        # Try to extract app name from first lines
        first_line = lines[0] if lines else ""
        if "app" in first_line.lower() or "application" in first_line.lower():
            app_name = first_line.strip()

    is_multipage = len(pages) >= 2 or has_multipage_keywords

    return {
        "is_multipage": is_multipage,
        "pages": pages if is_multipage else [],
        "app_name": app_name if is_multipage else None,
    }


def _infer_page_type(page_name_lower: str) -> str:
    """Infer page type from page name."""
    if any(word in page_name_lower for word in ["dashboard", "analytics", "metrics", "kpi"]):
        return "dashboard"
    elif any(word in page_name_lower for word in ["data", "explorer", "browse", "search"]):
        return "data_explorer"
    elif any(word in page_name_lower for word in ["chat", "messages", "conversation"]):
        return "chat"
    elif any(
        word in page_name_lower for word in ["settings", "config", "preferences", "profile", "form"]
    ):
        return "form"
    elif any(word in page_name_lower for word in ["report", "summary", "results"]):
        return "report"
    else:
        return "custom"


def interpret_page_drawing(
    drawing_description: str,
    image_data: Optional[str] = None,
    canvas_data: Optional[str] = None,
    confidence_threshold: str = "medium",
    auto_plan: bool = True,
    workflow_mode: str = "auto",
) -> Dict[str, Any]:
    """
    Interpret a page drawing (sketch/wireframe) and translate it to planner parameters.

    This tool analyzes drawings of Streamlit pages (hand-drawn, digital sketches, or
    whiteboard captures) and automatically determines the appropriate page type,
    components, layout, and features. It intelligently routes to either single-page
    or multi-page planning workflows.

    Args:
        drawing_description: Text description of the drawing (required). Describe what
                           you see in the sketch: layout, components, labels, etc.
        image_data: Optional base64-encoded image data (PNG/JPG). Future enhancement
                   for vision-based analysis.
        canvas_data: Optional JSON string with structured canvas data from tools like
                    Excalidraw or Miro with format: {"elements": [{"type": "text",
                    "text": "...", "x": 0, "y": 0}, ...]}
        confidence_threshold: Minimum confidence level (low/medium/high). If interpretation
                            confidence is below threshold, a warning is included.
        auto_plan: If True (default), automatically calls appropriate planner with
                  interpreted parameters. If False, only returns interpretation.
        workflow_mode: Workflow routing mode:
                      - "auto" (default): Auto-detect single vs multi-page
                      - "single": Force single-page workflow
                      - "multi": Force multi-page workflow

    Returns:
        Dictionary containing:
        - workflow_type: "single_page" or "multi_page"
        - interpretation: Analysis of the drawing
        - planner_parameters: Extracted parameters for the planner
        - app_plan_result: Full app plan (if multi-page)
        - page_plans: Individual page plans (if multi-page)
        - planner_result: Full planning results (if single-page and auto_plan=True)
        - confidence: Confidence level in interpretation
        - warnings: Any warnings or suggestions

    Example usage:
        >>> # Single page
        >>> interpret_page_drawing(
        ...     drawing_description="Dashboard with sidebar on left. Main area has "
        ...                        "4 metric cards at top, then 2 charts side by side..."
        ... )

        >>> # Multi-page app
        >>> interpret_page_drawing(
        ...     drawing_description="Multi-page app with 3 pages:\\n"
        ...                        "1. Home - Dashboard with metrics\\n"
        ...                        "2. Data - Data explorer with upload\\n"
        ...                        "3. Settings - Configuration form"
        ... )
    """
    warnings = []

    # Parse canvas data if provided
    canvas_dict = None
    if canvas_data:
        try:
            canvas_dict = json.loads(canvas_data) if isinstance(canvas_data, str) else canvas_data
        except json.JSONDecodeError:
            warnings.append("Could not parse canvas_data JSON. Proceeding with text analysis only.")

    # Detect if this is a multi-page or single-page drawing
    multipage_detection = _detect_multipage_intent(drawing_description, canvas_dict)

    # Determine workflow based on mode and detection
    if workflow_mode == "auto":
        is_multipage = multipage_detection["is_multipage"]
    elif workflow_mode == "multi":
        is_multipage = True
    else:  # "single"
        is_multipage = False

    # Route to appropriate workflow
    if is_multipage:
        return _handle_multipage_workflow(
            drawing_description,
            multipage_detection,
            canvas_dict,
            confidence_threshold,
            auto_plan,
            warnings,
        )
    else:
        return _handle_single_page_workflow(
            drawing_description, canvas_dict, confidence_threshold, auto_plan, warnings, image_data
        )


def _handle_single_page_workflow(
    drawing_description: str,
    canvas_dict: Optional[Dict],
    confidence_threshold: str,
    auto_plan: bool,
    warnings: List[str],
    image_data: Optional[str] = None,
) -> Dict[str, Any]:
    """Handle single-page workflow (existing logic)."""
    # Analyze the drawing text and canvas structure
    extracted_info = analyze_drawing_text(drawing_description, canvas_dict)

    # Analyze layout structure
    layout_structure = analyze_image_layout_structure(drawing_description)

    # Handle image data (future enhancement)
    if image_data:
        warnings.append(
            "Image analysis is currently limited. The tool relies primarily on text "
            "descriptions and canvas data. For best results, provide detailed text "
            "descriptions of your drawing."
        )
        # Future: Call vision API to analyze image
        # vision_analysis = analyze_image_with_vision(image_data)
        # extracted_info = merge_analysis(extracted_info, vision_analysis)

    # Check confidence threshold
    confidence = extracted_info["confidence"]
    confidence_levels = {"low": 1, "medium": 2, "high": 3}

    if confidence_levels.get(confidence, 0) < confidence_levels.get(confidence_threshold, 2):
        warnings.append(
            f"Interpretation confidence ({confidence}) is below threshold ({confidence_threshold}). "
            f"Consider providing more details in your drawing description. Mention specific "
            f"component types, layout structure, and data requirements."
        )

    # Build planner parameters
    planner_params = {
        "description": create_enhanced_description(drawing_description, extracted_info),
        "page_type": extracted_info["page_type"],
        "features": extracted_info["features"],
        "data_source": extracted_info["data_source"],
        "layout_preference": extracted_info["layout_preference"],
        "multipage": False,  # Could be inferred from drawing in future
        "include_testing": False,
    }

    # Add data freshness and performance hints if data source detected
    if extracted_info["data_source"] != "none":
        planner_params["data_freshness"] = "medium"
        planner_params["performance_priority"] = "balanced"

    # Build result
    result = {
        "interpretation": {
            "detected_page_type": extracted_info["page_type"],
            "identified_features": extracted_info["features"],
            "data_source": extracted_info["data_source"],
            "layout_preference": extracted_info["layout_preference"],
            "layout_structure": layout_structure,
            "confidence": confidence,
        },
        "planner_parameters": planner_params,
        "warnings": warnings,
    }

    # Call planner if auto_plan is True
    if auto_plan:
        try:
            planner_result = plan_streamlit_page(**planner_params)
            result["planner_result"] = planner_result
        except Exception as e:
            warnings.append(f"Error calling planner: {str(e)}")
            result["warnings"] = warnings

    # Add workflow type
    result["workflow_type"] = "single_page"
    return result


def _handle_multipage_workflow(
    drawing_description: str,
    multipage_detection: Dict[str, Any],
    canvas_dict: Optional[Dict],
    confidence_threshold: str,
    auto_plan: bool,
    warnings: List[str],
) -> Dict[str, Any]:
    """
    Handle multi-page workflow.

    Workflow:
    1. Create full app plan (always first!)
    2. Create individual page plans for each page
    3. Return structured planning results
    """
    app_name = multipage_detection.get("app_name", "Multi-Page App")
    detected_pages = multipage_detection.get("pages", [])

    # If no pages detected, try to provide a default structure
    if not detected_pages:
        warnings.append(
            "No specific pages detected. Providing default structure. "
            "For better results, explicitly list pages in your description."
        )
        detected_pages = [
            {"name": "Home", "description": "Main landing page", "type": "dashboard"},
            {"name": "Data", "description": "Data exploration page", "type": "data_explorer"},
            {"name": "Settings", "description": "Settings page", "type": "form"},
        ]

    # Build result structure
    result = {
        "workflow_type": "multi_page",
        "interpretation": {
            "app_name": app_name,
            "detected_pages": detected_pages,
            "page_count": len(detected_pages),
            "confidence": "medium",  # Multi-page detection is generally medium confidence
        },
        "warnings": warnings,
        "app_plan_result": None,
        "page_plans": [],
    }

    if auto_plan:
        try:
            # Step 1: Create full app plan (ALWAYS FIRST!)
            app_plan_result = create_app_plan(
                app_name=app_name, description=drawing_description, pages=detected_pages
            )
            result["app_plan_result"] = app_plan_result

            # Step 2: Create individual page plans
            page_plans = []
            for page in detected_pages:
                try:
                    page_plan = create_page_plan(
                        page_name=page["name"],
                        page_type=page.get("type", "custom"),
                        description=page.get("description", f"{page['name']} page"),
                        data_source="none",  # Can be inferred from description in future
                        layout_preference="centered",
                    )
                    page_plans.append(page_plan)
                except Exception as e:
                    warnings.append(f"Error creating plan for page '{page['name']}': {str(e)}")

            result["page_plans"] = page_plans

        except Exception as e:
            warnings.append(f"Error creating app plan: {str(e)}")
            result["warnings"] = warnings

    return result


def format_interpretation_output(result: Dict[str, Any]) -> str:
    """
    Format the interpretation result in a readable way for display.

    Args:
        result: Result dictionary from interpret_page_drawing

    Returns:
        Formatted string output
    """
    workflow_type = result.get("workflow_type", "single_page")

    # Route to appropriate formatter
    if workflow_type == "multi_page":
        return _format_multipage_output(result)
    else:
        return _format_single_page_output(result)


def _format_single_page_output(result: Dict[str, Any]) -> str:
    """Format single-page interpretation output."""
    interpretation = result["interpretation"]
    params = result.get("planner_parameters", {})
    warnings = result.get("warnings", [])

    output = []

    # Header
    output.append("# 🎨 Drawing Interpretation Results")
    output.append("")

    # Warnings (if any)
    if warnings:
        output.append("## ⚠️ Warnings")
        for warning in warnings:
            output.append(f"- {warning}")
        output.append("")

    # Interpretation summary
    output.append("## 📊 Interpretation Summary")
    output.append(f"**Confidence Level**: {interpretation['confidence'].upper()}")
    output.append(f"**Detected Page Type**: {interpretation['detected_page_type']}")
    output.append(f"**Layout Preference**: {interpretation['layout_preference']}")
    output.append(f"**Data Source**: {interpretation['data_source']}")
    output.append("")

    # Layout structure
    layout_struct = interpretation.get("layout_structure", {})
    output.append("### Layout Structure")
    output.append(f"- **Columns**: {layout_struct.get('columns', 1)}")
    output.append(f"- **Sidebar**: {'Yes' if layout_struct.get('has_sidebar') else 'No'}")
    output.append(f"- **Complexity**: {layout_struct.get('complexity', 'simple').title()}")
    if layout_struct.get("sections"):
        output.append(f"- **Sections**: {', '.join(layout_struct['sections'])}")
    output.append("")

    # Identified features
    features = interpretation.get("identified_features", [])
    if features:
        output.append("### Identified Features")
        for feature in features:
            output.append(f"- {feature.replace('_', ' ').title()}")
        output.append("")

    # Planner parameters
    output.append("## 🔧 Generated Planner Parameters")
    output.append("```json")
    output.append(json.dumps(params, indent=2))
    output.append("```")
    output.append("")

    # Planner result (if available)
    if "planner_result" in result:
        planner_result = result["planner_result"]

        output.append("## 📝 Generated Page Code")
        output.append("")
        output.append(
            "The planner has generated complete implementation code based on your drawing:"
        )
        output.append("")
        output.append("```python")
        output.append(planner_result.get("code", "# Code generation failed"))
        output.append("```")
        output.append("")

        # Best practices
        if "best_practices" in planner_result:
            output.append("## 💡 Best Practices & Tips")
            best_practices = planner_result["best_practices"]

            if "architecture_notes" in best_practices:
                output.append("### Architecture Notes")
                for note in best_practices["architecture_notes"]:
                    output.append(f"- {note}")
                output.append("")

            if "performance_tips" in best_practices:
                output.append("### Performance Tips")
                for tip in best_practices["performance_tips"]:
                    output.append(f"- {tip}")
                output.append("")

    # Next steps
    output.append("## 🚀 Next Steps")
    output.append("")
    output.append("1. **Review the generated code** above and make any necessary adjustments")
    output.append("2. **Copy to a .py file** (e.g., `app.py` or `page.py`)")
    output.append("3. **Customize** based on your specific requirements")
    output.append("4. **Run** with: `streamlit run your_app.py`")
    output.append("")

    if interpretation["confidence"] == "low":
        output.append(
            "💡 **Tip**: Since confidence was low, consider providing more details about:"
        )
        output.append("   - Specific component types (e.g., 'line chart', 'upload button')")
        output.append("   - Data requirements (e.g., 'load data from API', 'user uploads CSV')")
        output.append("   - Layout details (e.g., 'sidebar on left', 'three columns')")
        output.append("")

    return "\n".join(output)


def _format_multipage_output(result: Dict[str, Any]) -> str:
    """Format multi-page interpretation output."""
    interpretation = result["interpretation"]
    warnings = result.get("warnings", [])
    app_plan_result = result.get("app_plan_result")
    page_plans = result.get("page_plans", [])

    output = []

    # Header
    output.append("# 🎨 Multi-Page App Interpretation Results")
    output.append("")

    # Workflow info
    output.append("**Workflow**: Multi-Page Application Planning")
    output.append("")

    # Warnings (if any)
    if warnings:
        output.append("## ⚠️ Warnings")
        for warning in warnings:
            output.append(f"- {warning}")
        output.append("")

    # Interpretation summary
    output.append("## 📊 App Overview")
    output.append(f"**App Name**: {interpretation['app_name']}")
    output.append(f"**Total Pages**: {interpretation['page_count']}")
    output.append(f"**Confidence Level**: {interpretation['confidence'].upper()}")
    output.append("")

    # Detected pages
    output.append("### Detected Pages")
    for i, page in enumerate(interpretation.get("detected_pages", []), 1):
        output.append(f"{i}. **{page['name']}** ({page.get('type', 'custom')})")
        output.append(f"   - {page.get('description', 'No description')}")
    output.append("")

    # App Plan Result
    if app_plan_result:
        output.append("## 📋 Full Application Plan")
        output.append("")
        output.append(f"✅ **Status**: {app_plan_result.get('status', 'unknown')}")
        output.append(f"📁 **Plan File**: `{app_plan_result.get('file_path', 'N/A')}`")
        output.append("")
        output.append("The full application plan has been created at `./plans/full_plan.md`")
        output.append("")

    # Individual Page Plans
    if page_plans:
        output.append("## 📄 Individual Page Plans")
        output.append("")
        for i, page_plan in enumerate(page_plans, 1):
            page_name = page_plan.get("page_name", f"Page {i}")
            page_type = page_plan.get("page_type", "custom")
            status = page_plan.get("status", "unknown")
            file_path = page_plan.get("file_path", "N/A")

            output.append(f"### {i}. {page_name}")
            output.append(f"- **Type**: {page_type}")
            output.append(f"- **Status**: {status}")
            output.append(f"- **Plan File**: `{file_path}`")

            # Recommendations
            if "recommendations" in page_plan:
                rec = page_plan["recommendations"]
                output.append("- **Recommendations**:")
                if rec.get("caching"):
                    output.append(f"  - Use `{rec['caching']}` for data caching")
                if rec.get("use_fragments"):
                    output.append("  - Consider using `@st.fragment` for performance")
                if rec.get("use_forms"):
                    output.append("  - Use `st.form` to batch inputs")
            output.append("")

    # Next Steps
    output.append("## 🚀 Next Steps")
    output.append("")
    output.append("**Recommended Workflow**:")
    output.append("")
    output.append("1. **Review Plans**")
    output.append("   - Read `./plans/full_plan.md` to understand the overall architecture")
    output.append("   - Review individual page plans in `./plans/page_*.md`")
    output.append("")
    output.append("2. **Implement Pages** (one at a time)")
    output.append("   - Use the `plan_streamlit_page` tool for each page to generate code")
    output.append("   - Or manually build based on page plans")
    output.append("")
    output.append("3. **Validate Implementation**")
    output.append("   - Check each page against its plan")
    output.append("   - Ensure alignment with overall app architecture")
    output.append("")
    output.append("4. **Test & Integrate**")
    output.append("   - Test each page independently")
    output.append("   - Integrate navigation using `st.navigation()`")
    output.append("   - Run with: `streamlit run app.py`")
    output.append("")

    # Tips
    output.append("## 💡 Tips for Multi-Page Apps")
    output.append("")
    output.append("- **Follow the plan**: Always refer back to the full app plan for consistency")
    output.append("- **Build incrementally**: Implement one page at a time and test")
    output.append(
        "- **Share state carefully**: Use `st.session_state` for data shared across pages"
    )
    output.append("- **Keep navigation simple**: Use clear, descriptive page names")
    output.append("")

    return "\n".join(output)


# Tool definition for MCP server
TOOL = {
    "name": "interpret_page_drawing",
    "description": """
    Interpret a drawing/sketch of a Streamlit page and automatically generate implementation code.

    This AI-powered tool analyzes page sketches (hand-drawn, digital wireframes, or whiteboard
    captures) and translates them into working Streamlit code. It identifies layout structure,
    components, features, and automatically determines the best implementation approach.

    **How it works**:
    1. You describe your drawing in text (e.g., "Dashboard with sidebar, 4 metrics, 2 charts")
    2. Optionally provide structured canvas data from tools like Excalidraw/Miro
    3. The tool analyzes the description to identify page type, components, and layout
    4. Automatically calls the page planner with optimized parameters
    5. Returns complete, runnable Streamlit code with best practices

    **Best for**:
    - Converting whiteboard sketches to code
    - Rapid prototyping from wireframes
    - Translating design mockups to Streamlit
    - Quick POC development from rough ideas

    **Input tips for best results**:
    - Mention specific component types (chart, button, upload, filter, etc.)
    - Describe layout clearly (sidebar, columns, sections)
    - Note data requirements (upload files, API data, database)
    - Label key sections in your drawing

    **Example descriptions**:
    - "Dashboard with 3 columns: left sidebar with filters, main area with 4 KPI cards at
       top and line chart below, right panel with data table"
    - "Simple form with text inputs for name/email, dropdown for category, file upload
       button, and submit button at bottom"
    - "Chat interface with messages on left taking up 2/3 width, conversation history
       sidebar on right with timestamps"
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "drawing_description": {
                "type": "string",
                "description": (
                    "Text description of your page drawing/sketch. Describe the layout, "
                    "components, labels, and structure. Be specific about component types "
                    "(e.g., 'line chart', 'upload button', 'metric cards') and layout "
                    "(e.g., 'sidebar on left', 'three columns', '4 metrics in a row'). "
                    "Example: 'Dashboard layout with sidebar containing filters. Main area "
                    "has 4 metric cards at top, two charts side by side (line and bar), "
                    "and a data table at the bottom.'"
                ),
            },
            "image_data": {
                "type": "string",
                "description": (
                    "Optional base64-encoded image data (PNG or JPG format). Currently "
                    "used for reference only. Future versions will support full vision "
                    "analysis. Providing a detailed text description is recommended."
                ),
            },
            "canvas_data": {
                "type": "string",
                "description": (
                    "Optional JSON string containing structured canvas data from drawing "
                    "tools like Excalidraw or Miro. Expected format: "
                    '{"elements": [{"type": "text", "text": "Upload Button", '
                    '"x": 100, "y": 200}, ...]}. This enhances interpretation accuracy '
                    "when available."
                ),
            },
            "confidence_threshold": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": (
                    "Minimum confidence level required for interpretation. If the tool's "
                    "confidence in its interpretation is below this threshold, a warning "
                    "will be included suggesting more details. Default: 'medium'."
                ),
                "default": "medium",
            },
            "auto_plan": {
                "type": "boolean",
                "description": (
                    "If true (default), automatically calls the appropriate planner "
                    "(single-page or multi-page) with interpreted parameters. "
                    "If false, only returns the interpretation and planner parameters "
                    "for review before planning."
                ),
                "default": True,
            },
            "workflow_mode": {
                "type": "string",
                "enum": ["auto", "single", "multi"],
                "description": (
                    "Workflow routing mode:\\n"
                    "- 'auto' (default): Automatically detect if description is for single "
                    "page or multi-page app\\n"
                    "- 'single': Force single-page workflow (uses plan_streamlit_page)\\n"
                    "- 'multi': Force multi-page workflow (uses create_app_plan + "
                    "create_page_plan for each page)"
                ),
                "default": "auto",
            },
        },
        "required": ["drawing_description"],
    },
}
