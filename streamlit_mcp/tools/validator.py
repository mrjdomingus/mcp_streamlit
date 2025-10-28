"""Validation tool - validates implementation against plans."""

import re
from typing import Dict, Any, List, Optional
from pathlib import Path


def validate_implementation(
    code: str,
    page_plan_file: Optional[str] = None,
    app_plan_file: Optional[str] = None,
    page_type: Optional[str] = None,
    validation_mode: str = "standard"
) -> Dict[str, Any]:
    """
    Validate implementation code against page and app plans.

    This tool checks:
    - Presence of planned components
    - Alignment with page type requirements
    - Best practices compliance
    - Consistency with overall app architecture (if app plan provided)

    Args:
        code: The implementation code to validate
        page_plan_file: Path to the page plan markdown file (optional)
        app_plan_file: Path to the full app plan markdown file (optional)
        page_type: Expected page type (dashboard, data_explorer, chat, form, report, custom)
        validation_mode: Validation strictness level
                        - "lenient": Check only critical requirements
                        - "standard": Check recommended practices
                        - "strict": Enforce all best practices

    Returns:
        Dictionary containing:
        - status: "passed", "warnings", or "failed"
        - score: Validation score (0-100)
        - component_validation: Results of component checks
        - best_practices_validation: Results of best practices checks
        - missing_elements: List of expected but missing elements
        - suggestions: Recommendations for improvement
        - alignment_with_plan: How well code matches the plan
    """
    results = {
        "status": "unknown",
        "score": 0,
        "component_validation": {},
        "best_practices_validation": {},
        "missing_elements": [],
        "suggestions": [],
        "alignment_with_plan": {}
    }

    # Load plans if provided
    page_plan_content = None
    app_plan_content = None

    if page_plan_file:
        try:
            page_plan_content = Path(page_plan_file).read_text()
        except Exception as e:
            results["suggestions"].append(f"Could not read page plan: {str(e)}")

    if app_plan_file:
        try:
            app_plan_content = Path(app_plan_file).read_text()
        except Exception as e:
            results["suggestions"].append(f"Could not read app plan: {str(e)}")

    # Perform validations
    component_results = _validate_components(code, page_type, page_plan_content)
    best_practices_results = _validate_best_practices(code, page_type, validation_mode)
    plan_alignment_results = _validate_plan_alignment(code, page_plan_content, app_plan_content)

    # Combine results
    results["component_validation"] = component_results
    results["best_practices_validation"] = best_practices_results
    results["alignment_with_plan"] = plan_alignment_results

    # Collect missing elements
    if component_results.get("missing_components"):
        results["missing_elements"].extend(component_results["missing_components"])

    # Calculate score (0-100)
    component_score = component_results.get("score", 0)
    practices_score = best_practices_results.get("score", 0)
    alignment_score = plan_alignment_results.get("score", 100)  # Default 100 if no plan

    # Weighted average
    results["score"] = int(
        (component_score * 0.4) + (practices_score * 0.3) + (alignment_score * 0.3)
    )

    # Generate suggestions
    results["suggestions"].extend(component_results.get("suggestions", []))
    results["suggestions"].extend(best_practices_results.get("suggestions", []))
    results["suggestions"].extend(plan_alignment_results.get("suggestions", []))

    # Determine overall status
    if results["score"] >= 90:
        results["status"] = "passed"
    elif results["score"] >= 70:
        results["status"] = "warnings"
    else:
        results["status"] = "failed"

    return results


def _validate_components(
    code: str,
    page_type: Optional[str],
    page_plan_content: Optional[str]
) -> Dict[str, Any]:
    """Validate presence of expected components."""
    results = {
        "score": 0,
        "found_components": [],
        "missing_components": [],
        "suggestions": []
    }

    # Define expected components by page type
    expected_by_type = {
        "dashboard": ["st.metric", "st.plotly_chart|st.altair_chart|st.line_chart|st.bar_chart", "st.dataframe"],
        "data_explorer": ["st.dataframe|st.data_editor", "st.file_uploader|load_data", "st.selectbox|st.multiselect"],
        "chat": ["st.chat_message", "st.chat_input", "st.session_state"],
        "form": ["st.form", "st.text_input|st.number_input", "st.form_submit_button"],
        "report": ["st.metric", "st.tabs", "st.markdown|st.write"]
    }

    expected_components = expected_by_type.get(page_type, []) if page_type else []

    # Check for expected components
    found_count = 0
    for expected in expected_components:
        # Handle OR patterns (e.g., "st.line_chart|st.bar_chart")
        if "|" in expected:
            patterns = expected.split("|")
            if any(re.search(rf'\b{re.escape(p)}\b', code) for p in patterns):
                found_count += 1
                results["found_components"].append(expected)
            else:
                results["missing_components"].append(f"One of: {expected}")
        else:
            if re.search(rf'\b{re.escape(expected)}\b', code):
                found_count += 1
                results["found_components"].append(expected)
            else:
                results["missing_components"].append(expected)

    # Calculate component score
    if expected_components:
        results["score"] = int((found_count / len(expected_components)) * 100)
    else:
        results["score"] = 100  # No specific requirements

    # Extract requirements from page plan if available
    if page_plan_content:
        plan_components = _extract_components_from_plan(page_plan_content)
        for component in plan_components:
            if component not in code:
                results["suggestions"].append(
                    f"Page plan mentions '{component}' but it's not found in code"
                )

    return results


def _validate_best_practices(
    code: str,
    page_type: Optional[str],
    validation_mode: str
) -> Dict[str, Any]:
    """Validate Streamlit best practices."""
    results = {
        "score": 100,
        "practices_checked": [],
        "violations": [],
        "suggestions": []
    }

    checks = []

    # Critical checks (all modes)
    checks.append({
        "name": "Page configuration",
        "pattern": r"st\.set_page_config",
        "severity": "critical",
        "message": "Missing st.set_page_config() - should be first Streamlit command"
    })

    # Standard checks
    if validation_mode in ["standard", "strict"]:
        checks.extend([
            {
                "name": "Session state initialization",
                "pattern": r"if .* not in st\.session_state:",
                "severity": "warning",
                "message": "Consider initializing session_state before accessing",
                "context": "st.session_state" in code
            },
            {
                "name": "Data caching",
                "pattern": r"@st\.cache_data|@st\.cache_resource",
                "severity": "warning",
                "message": "Consider using @st.cache_data for data loading functions",
                "context": "def load" in code or "def get_data" in code or "pd.read" in code
            },
        ])

    # Strict checks
    if validation_mode == "strict":
        checks.extend([
            {
                "name": "Type hints",
                "pattern": r"def \w+\([^)]*:[^)]+\) ->",
                "severity": "info",
                "message": "Add type hints to functions for better code quality"
            },
            {
                "name": "Docstrings",
                "pattern": r'""".*?"""',
                "severity": "info",
                "message": "Add docstrings to document your functions"
            }
        ])

    # Run checks
    points_deducted = 0
    for check in checks:
        # Skip context-dependent checks if context not met
        if "context" in check and not check["context"]:
            continue

        results["practices_checked"].append(check["name"])

        if not re.search(check["pattern"], code, re.DOTALL):
            results["violations"].append({
                "practice": check["name"],
                "severity": check["severity"],
                "message": check["message"]
            })

            # Deduct points based on severity
            if check["severity"] == "critical":
                points_deducted += 30
            elif check["severity"] == "warning":
                points_deducted += 15
            else:  # info
                points_deducted += 5

            results["suggestions"].append(f"⚠️ {check['message']}")

    results["score"] = max(0, 100 - points_deducted)

    return results


def _validate_plan_alignment(
    code: str,
    page_plan_content: Optional[str],
    app_plan_content: Optional[str]
) -> Dict[str, Any]:
    """Validate alignment with plans."""
    results = {
        "score": 100,
        "suggestions": [],
        "plan_requirements_met": 0,
        "plan_requirements_total": 0
    }

    if not page_plan_content and not app_plan_content:
        # No plans to validate against
        return results

    requirements_met = 0
    requirements_total = 0

    if page_plan_content:
        # Extract key requirements from page plan
        plan_requirements = _extract_requirements_from_plan(page_plan_content)
        requirements_total += len(plan_requirements)

        for req in plan_requirements:
            if req.lower() in code.lower():
                requirements_met += 1
            else:
                results["suggestions"].append(
                    f"Plan requirement not implemented: {req}"
                )

    if app_plan_content:
        # Check for shared dependencies mentioned in app plan
        shared_deps = _extract_shared_dependencies(app_plan_content)
        if shared_deps:
            results["suggestions"].append(
                f"Remember to implement shared dependencies: {', '.join(shared_deps)}"
            )

    # Calculate alignment score
    if requirements_total > 0:
        results["score"] = int((requirements_met / requirements_total) * 100)

    results["plan_requirements_met"] = requirements_met
    results["plan_requirements_total"] = requirements_total

    return results


def _extract_components_from_plan(plan_content: str) -> List[str]:
    """Extract component names mentioned in plan."""
    components = []

    # Look for component mentions in backticks or code blocks
    patterns = [
        r"`(st\.\w+)`",
        r"```python\n(.*?)```"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, plan_content, re.DOTALL)
        for match in matches:
            if match.startswith("st."):
                components.append(match)

    return list(set(components))


def _extract_requirements_from_plan(plan_content: str) -> List[str]:
    """Extract key requirements from plan."""
    requirements = []

    # Look for bullet points or numbered items
    lines = plan_content.split('\n')
    for line in lines:
        # Check for implementation steps or requirements
        if re.match(r'^\s*[-*\d.]+\s+', line):
            clean_line = re.sub(r'^\s*[-*\d.]+\s+', '', line).strip()
            if clean_line and len(clean_line) > 10:  # Meaningful requirement
                requirements.append(clean_line[:100])  # Truncate long lines

    return requirements[:10]  # Limit to top 10


def _extract_shared_dependencies(app_plan_content: str) -> List[str]:
    """Extract shared dependencies from app plan."""
    dependencies = []

    # Look for shared dependencies section
    if "shared dependencies" in app_plan_content.lower():
        lines = app_plan_content.split('\n')
        in_section = False

        for line in lines:
            if "shared dependencies" in line.lower():
                in_section = True
                continue

            if in_section:
                if line.startswith('#'):  # New section
                    break
                if line.strip().startswith('-'):
                    dep = re.sub(r'^\s*-\s*', '', line).strip()
                    if dep:
                        dependencies.append(dep[:50])  # Truncate

    return dependencies


# Tool definition
TOOL = {
    "name": "validate_implementation",
    "description": """
    Validate Streamlit implementation code against plans and best practices.

    This tool performs comprehensive validation:
    - **Component Validation**: Checks for presence of expected components based on page type
    - **Best Practices**: Validates adherence to Streamlit best practices
    - **Plan Alignment**: Compares code against page and app plans
    - **Scoring**: Provides 0-100 score with actionable feedback

    **Validation Modes**:
    - `lenient`: Checks only critical requirements
    - `standard`: Checks recommended practices (default)
    - `strict`: Enforces all best practices including type hints and docstrings

    **Use this tool to**:
    - Verify implementation matches plans
    - Catch missing components early
    - Ensure best practices are followed
    - Get improvement suggestions

    **Example usage**:
    ```python
    validate_implementation(
        code=my_page_code,
        page_plan_file="./plans/page_dashboard.md",
        app_plan_file="./plans/full_plan.md",
        page_type="dashboard",
        validation_mode="standard"
    )
    ```

    **Returns**: Validation report with score, status, missing elements, and suggestions
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The implementation code to validate"
            },
            "page_plan_file": {
                "type": "string",
                "description": "Path to the page plan markdown file (e.g., './plans/page_dashboard.md')"
            },
            "app_plan_file": {
                "type": "string",
                "description": "Path to the full app plan markdown file (e.g., './plans/full_plan.md')"
            },
            "page_type": {
                "type": "string",
                "enum": ["dashboard", "data_explorer", "chat", "form", "report", "custom"],
                "description": "Expected page type for component validation"
            },
            "validation_mode": {
                "type": "string",
                "enum": ["lenient", "standard", "strict"],
                "description": "Validation strictness level",
                "default": "standard"
            }
        },
        "required": ["code"]
    }
}
