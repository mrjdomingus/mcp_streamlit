"""Orchestration tool - end-to-end workflow from drawing to validated implementation."""

from typing import Dict, Any, List, Optional
from .drawing_interpreter import interpret_page_drawing
from .planner import plan_streamlit_page
from .app_planner import create_app_plan, create_page_plan


def orchestrate_app_from_drawing(
    drawing_description: str,
    app_name: Optional[str] = None,
    generate_code: bool = True,
    validate_plans: bool = True,
    image_data: Optional[str] = None,
    canvas_data: Optional[str] = None
) -> Dict[str, Any]:
    """
    Complete orchestration workflow from drawing to validated implementation.

    This tool implements the full workflow:
    1. Get Drawing → Interpret components and structure
    2. Understand Components → Extract pages, features, dependencies
    3. Plan Full App → Always start with create_app_plan (for multi-page) or analyze requirements (for single page)
    4. Plan Each Page → Use create_page_plan for each identified page (multi-page only)
    5. Execute → Generate code for each page separately
    6. Validate → Check generated plans against requirements

    Args:
        drawing_description: Text description of the application drawing
        app_name: Optional custom app name (auto-detected if not provided)
        generate_code: If True, generate implementation code for each page
        validate_plans: If True, validate plans for completeness and consistency
        image_data: Optional base64-encoded image data
        canvas_data: Optional JSON canvas data

    Returns:
        Dictionary containing:
        - workflow_summary: Overview of workflow execution
        - interpretation_result: Drawing interpretation results
        - app_plan: Full application plan (if multi-page)
        - page_plans: List of individual page plans
        - generated_code: Code for each page (if generate_code=True)
        - validation_results: Validation report (if validate_plans=True)
        - next_steps: Recommended next actions
    """
    workflow_steps = []
    warnings = []

    # Step 1: Interpret the drawing (auto-detect single vs multi-page)
    workflow_steps.append("Interpreting drawing and detecting app structure...")

    interpretation_result = interpret_page_drawing(
        drawing_description=drawing_description,
        image_data=image_data,
        canvas_data=canvas_data,
        auto_plan=True,  # This will create app/page plans automatically
        workflow_mode="auto"  # Auto-detect single vs multi-page
    )

    workflow_type = interpretation_result.get("workflow_type", "single_page")
    workflow_steps.append(f"Detected workflow type: {workflow_type}")

    # Collect all plans
    app_plan_result = None
    page_plans = []
    generated_code = []

    if workflow_type == "multi_page":
        # Multi-page workflow
        workflow_steps.append("Multi-page app detected - following full app planning workflow")

        # The interpretation already created plans, extract them
        app_plan_result = interpretation_result.get("app_plan_result")
        page_plans = interpretation_result.get("page_plans", [])

        workflow_steps.append(f"✓ Full app plan created: {app_plan_result.get('file_path') if app_plan_result else 'N/A'}")
        workflow_steps.append(f"✓ Created {len(page_plans)} individual page plans")

        # Step 5: Generate code for each page if requested
        if generate_code and page_plans:
            workflow_steps.append("Generating implementation code for each page...")

            for page_plan in page_plans:
                page_name = page_plan.get("page_name", "Unknown")
                page_type = page_plan.get("page_type", "custom")

                try:
                    # Generate code using plan_streamlit_page
                    code_result = plan_streamlit_page(
                        description=f"{page_name} - {page_plan.get('description', '')}",
                        page_type=page_type,
                        features=[],  # Could be extracted from page plan
                        data_source="none",
                        layout_preference="centered"
                    )

                    generated_code.append({
                        "page_name": page_name,
                        "page_type": page_type,
                        "code": code_result.get("code", "# Code generation failed"),
                        "components": code_result.get("components", []),
                        "file_path": page_plan.get("file_path")
                    })

                    workflow_steps.append(f"  ✓ Generated code for {page_name}")

                except Exception as e:
                    warnings.append(f"Failed to generate code for {page_name}: {str(e)}")
                    workflow_steps.append(f"  ✗ Failed to generate code for {page_name}")

    else:
        # Single-page workflow
        workflow_steps.append("Single page detected - following single-page workflow")

        # Extract the generated code from interpretation result
        planner_result = interpretation_result.get("planner_result")

        if planner_result:
            workflow_steps.append("✓ Page plan and code generated")

            generated_code.append({
                "page_name": "Main Page",
                "page_type": interpretation_result["interpretation"].get("detected_page_type", "custom"),
                "code": planner_result.get("code", ""),
                "components": planner_result.get("components", [])
            })

    # Step 6: Validate plans if requested
    validation_results = None
    if validate_plans:
        workflow_steps.append("Validating plans for completeness and consistency...")

        validation_results = _validate_workflow_outputs(
            workflow_type=workflow_type,
            interpretation=interpretation_result.get("interpretation"),
            app_plan=app_plan_result,
            page_plans=page_plans,
            generated_code=generated_code
        )

        workflow_steps.append(f"✓ Validation complete: {validation_results['status']}")

    # Build next steps
    next_steps = _generate_next_steps(
        workflow_type=workflow_type,
        has_code=len(generated_code) > 0,
        app_plan_path=app_plan_result.get("file_path") if app_plan_result else None,
        page_count=len(page_plans) if workflow_type == "multi_page" else 1
    )

    # Build final result
    result = {
        "workflow_summary": {
            "workflow_type": workflow_type,
            "steps_completed": workflow_steps,
            "warnings": warnings,
            "total_pages": len(page_plans) if workflow_type == "multi_page" else 1,
            "code_generated": len(generated_code) > 0
        },
        "interpretation_result": interpretation_result,
        "app_plan": app_plan_result,
        "page_plans": page_plans,
        "generated_code": generated_code,
        "validation_results": validation_results,
        "next_steps": next_steps
    }

    return result


def _validate_workflow_outputs(
    workflow_type: str,
    interpretation: Dict[str, Any],
    app_plan: Optional[Dict[str, Any]],
    page_plans: List[Dict[str, Any]],
    generated_code: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Validate workflow outputs for completeness and consistency."""
    issues = []
    suggestions = []

    if workflow_type == "multi_page":
        # Validate multi-page workflow outputs
        if not app_plan:
            issues.append("Missing full application plan")

        expected_page_count = interpretation.get("page_count", 0)
        actual_page_count = len(page_plans)

        if actual_page_count < expected_page_count:
            issues.append(
                f"Expected {expected_page_count} page plans, but only {actual_page_count} were created"
            )

        if generated_code:
            if len(generated_code) < len(page_plans):
                issues.append(
                    f"Code generated for {len(generated_code)}/{len(page_plans)} pages"
                )

        # Check for common missing elements
        page_names = [p.get("page_name", "") for p in page_plans]
        if "Home" not in page_names and "home" not in str(page_names).lower():
            suggestions.append("Consider adding a Home/Landing page to your app")

    else:
        # Validate single-page workflow
        if not generated_code:
            issues.append("No code generated for the page")

    # Determine overall status
    if issues:
        status = "issues_found"
    else:
        status = "passed"

    return {
        "status": status,
        "issues": issues,
        "suggestions": suggestions,
        "page_count_validation": {
            "expected": interpretation.get("page_count", 1) if workflow_type == "multi_page" else 1,
            "actual": len(page_plans) if workflow_type == "multi_page" else 1
        }
    }


def _generate_next_steps(
    workflow_type: str,
    has_code: bool,
    app_plan_path: Optional[str],
    page_count: int
) -> List[str]:
    """Generate recommended next steps based on workflow results."""
    steps = []

    if workflow_type == "multi_page":
        steps.append("📋 **Review Plans**")
        if app_plan_path:
            steps.append(f"   - Open and read `{app_plan_path}` for overall architecture")
        steps.append("   - Review individual page plans in `./plans/page_*.md`")
        steps.append("")

        if has_code:
            steps.append("💻 **Implement Pages**")
            steps.append(f"   - You have code for {page_count} page(s)")
            steps.append("   - Copy each page code to appropriate .py files")
            steps.append("   - Create an app.py for navigation using st.navigation()")
            steps.append("")
        else:
            steps.append("💻 **Generate Code**")
            steps.append("   - Use `plan_streamlit_page` tool for each page")
            steps.append("   - Follow the page plans created")
            steps.append("")

        steps.append("🧪 **Test & Integrate**")
        steps.append("   - Test each page independently first")
        steps.append("   - Set up navigation between pages")
        steps.append("   - Run with: `streamlit run app.py`")

    else:
        # Single page
        if has_code:
            steps.append("💻 **Implement**")
            steps.append("   - Copy the generated code to a .py file (e.g., app.py)")
            steps.append("   - Customize based on your specific needs")
            steps.append("")

        steps.append("🧪 **Test**")
        steps.append("   - Run with: `streamlit run app.py`")
        steps.append("   - Test all interactions")
        steps.append("   - Refine as needed")

    return steps


# Tool definition
TOOL = {
    "name": "orchestrate_app_from_drawing",
    "description": """
    Complete end-to-end orchestration workflow from drawing to validated implementation.

    This tool implements the full recommended workflow:
    1. **Get Drawing** → Interpret components and structure
    2. **Understand Components** → Extract pages, features, dependencies
    3. **Plan Full App** → Always start with create_app_plan (understands whole picture)
    4. **Plan Each Page** → Use create_page_plan for each identified page
    5. **Execute** → Generate code for each page separately
    6. **Validate** → Check generated plans and code against requirements

    **Key Features**:
    - Auto-detects single-page vs multi-page apps
    - Enforces "full plan first" approach for multi-page apps
    - Generates individual page plans before code generation
    - Optional validation of plans and code
    - Provides structured progress tracking
    - Returns actionable next steps

    **Use this tool when**:
    - Starting a new Streamlit project from a drawing/sketch
    - You want a guided, step-by-step workflow
    - You need validation and consistency checks
    - Building a multi-page application

    **Example usage**:
    ```
    orchestrate_app_from_drawing(
        drawing_description="Multi-page sales dashboard app with 3 pages:
        1. Home - Overview with KPIs and charts
        2. Data Explorer - Upload and filter sales data
        3. Settings - Configuration and preferences",
        app_name="Sales Dashboard",
        generate_code=True,
        validate_plans=True
    )
    ```
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "drawing_description": {
                "type": "string",
                "description": (
                    "Text description of your application drawing. For multi-page apps, "
                    "explicitly list all pages. For single pages, describe the layout "
                    "and components in detail."
                )
            },
            "app_name": {
                "type": "string",
                "description": "Optional custom name for the application (auto-detected if not provided)"
            },
            "generate_code": {
                "type": "boolean",
                "description": "If True, generate implementation code for each page",
                "default": True
            },
            "validate_plans": {
                "type": "boolean",
                "description": "If True, validate plans for completeness and consistency",
                "default": True
            },
            "image_data": {
                "type": "string",
                "description": "Optional base64-encoded image data of the drawing"
            },
            "canvas_data": {
                "type": "string",
                "description": "Optional JSON canvas data from drawing tools"
            }
        },
        "required": ["drawing_description"]
    }
}
