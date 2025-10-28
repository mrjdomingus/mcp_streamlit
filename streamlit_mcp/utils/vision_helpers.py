"""Vision and drawing analysis helpers for interpreting page layouts."""

import re
from typing import Dict, List, Any


# Component label mappings for text-based identification
COMPONENT_KEYWORDS = {
    # Charts and visualizations
    "chart": "charts",
    "graph": "charts",
    "plot": "charts",
    "visualization": "charts",
    "viz": "charts",
    # Data handling
    "upload": "data_upload",
    "file": "data_upload",
    "import": "data_upload",
    "filter": "data_filtering",
    "search": "data_filtering",
    "query": "data_filtering",
    "download": "file_download",
    "export": "file_download",
    # Metrics and data display
    "metric": "metrics",
    "kpi": "metrics",
    "stat": "metrics",
    "number": "metrics",
    "table": "charts",
    "dataframe": "charts",
    "grid": "charts",
    # Interactive elements
    "button": "user_input",
    "input": "user_input",
    "form": "user_input",
    "submit": "user_input",
    "select": "user_input",
    "dropdown": "user_input",
    "slider": "user_input",
    # Chat and messaging
    "chat": "chat_interface",
    "message": "chat_interface",
    "conversation": "chat_interface",
    # Auth
    "login": "authentication",
    "auth": "authentication",
    "sign in": "authentication",
    "user": "authentication",
    # Advanced features
    "wizard": "multi_step_form",
    "stepper": "multi_step_form",
    "multi-step": "multi_step_form",
    "realtime": "real_time_updates",
    "live": "real_time_updates",
    "stream": "real_time_updates",
}


# Page type indicators
PAGE_TYPE_KEYWORDS = {
    "dashboard": ["dashboard", "overview", "metrics", "kpi", "analytics"],
    "data_explorer": ["explorer", "data", "analysis", "browse", "investigate"],
    "chat": ["chat", "chatbot", "conversation", "ai", "assistant"],
    "form": ["form", "input", "wizard", "survey", "questionnaire"],
    "report": ["report", "summary", "findings", "document"],
    "custom": [],  # default fallback
}


# Data source indicators
DATA_SOURCE_KEYWORDS = {
    "upload": ["upload", "file", "csv", "import", "local"],
    "api": ["api", "fetch", "request", "endpoint", "rest", "http"],
    "database": ["database", "db", "sql", "query", "postgres", "mysql"],
    "example": ["example", "sample", "demo", "mock", "placeholder"],
    "none": [],
}


def analyze_drawing_text(drawing_description: str, canvas_data: Dict = None) -> Dict[str, Any]:
    """
    Analyze text description and canvas data to extract page components.

    Args:
        drawing_description: Text description of the drawing
        canvas_data: Optional structured canvas data (from Excalidraw, Miro, etc.)

    Returns:
        Dictionary with extracted information
    """
    description_lower = drawing_description.lower()

    # Extract features from text
    features = extract_features_from_text(description_lower)

    # If canvas data provided, enhance with structured information
    if canvas_data:
        canvas_features = extract_features_from_canvas(canvas_data)
        features = list(set(features + canvas_features))

    # Infer page type
    page_type = infer_page_type(description_lower)

    # Detect data source
    data_source = detect_data_source(description_lower)

    # Analyze layout preferences
    layout_pref = analyze_layout_preference(description_lower, canvas_data)

    return {
        "features": features,
        "page_type": page_type,
        "data_source": data_source,
        "layout_preference": layout_pref,
        "confidence": calculate_confidence(features, page_type, data_source),
    }


def extract_features_from_text(text: str) -> List[str]:
    """Extract feature list from text description using keyword matching."""
    features = set()

    for keyword, feature in COMPONENT_KEYWORDS.items():
        if keyword in text:
            features.add(feature)

    return list(features)


def extract_features_from_canvas(canvas_data: Dict) -> List[str]:
    """
    Extract features from structured canvas data.

    Expected canvas_data format:
    {
        "elements": [
            {"type": "text", "text": "Upload Button", "x": 100, "y": 200},
            {"type": "rectangle", "label": "Chart Area", "width": 500, "height": 300},
            ...
        ]
    }
    """
    features = set()

    if "elements" in canvas_data:
        for element in canvas_data["elements"]:
            # Check text content
            text_content = element.get("text", "") + " " + element.get("label", "")
            text_lower = text_content.lower()

            for keyword, feature in COMPONENT_KEYWORDS.items():
                if keyword in text_lower:
                    features.add(feature)

    return list(features)


def infer_page_type(text: str) -> str:
    """Infer page type from text description."""
    scores = {}

    for page_type, keywords in PAGE_TYPE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text)
        scores[page_type] = score

    # Return page type with highest score, default to 'custom'
    best_type = max(scores.items(), key=lambda x: x[1])
    return best_type[0] if best_type[1] > 0 else "custom"


def detect_data_source(text: str) -> str:
    """Detect likely data source from text description."""
    scores = {}

    for source_type, keywords in DATA_SOURCE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text)
        scores[source_type] = score

    # Return source with highest score, default to 'example'
    best_source = max(scores.items(), key=lambda x: x[1])
    return best_source[0] if best_source[1] > 0 else "example"


def analyze_layout_preference(text: str, canvas_data: Dict = None) -> str:
    """Analyze layout preference from description and structure."""
    # Check for explicit mentions
    if "wide" in text or "full width" in text or "full-width" in text:
        return "wide"
    elif "sidebar" in text or "side bar" in text or "side panel" in text:
        return "sidebar"

    # Check for multiple columns indicator (suggests wide layout)
    if re.search(r"\d+\s+column", text) or "multi-column" in text or "multicolumn" in text:
        return "wide"

    # Analyze canvas data if available
    if canvas_data and "elements" in canvas_data:
        # Check for sidebar-like structures (narrow column on left/right)
        elements = canvas_data.get("elements", [])

        # Look for elements labeled as sidebar
        for element in elements:
            label = (element.get("text", "") + " " + element.get("label", "")).lower()
            if "sidebar" in label or "menu" in label:
                return "sidebar"

        # Check for wide layout indicators (many columns)
        if len(elements) > 6:  # Many elements suggest complex layout
            return "wide"

    # Default to centered for simple layouts
    return "centered"


def calculate_confidence(features: List[str], page_type: str, data_source: str) -> str:
    """Calculate confidence level in the interpretation."""
    # High confidence: Clear features identified, specific page type
    if len(features) >= 3 and page_type != "custom":
        return "high"

    # Medium confidence: Some features identified
    elif len(features) >= 1:
        return "medium"

    # Low confidence: Limited information
    else:
        return "low"


def analyze_image_layout_structure(description: str) -> Dict[str, Any]:
    """
    Analyze layout structure from image description.

    Since we don't have direct vision API access, this function extracts
    layout clues from the text description that would typically come from
    a vision model analysis.

    Args:
        description: Text description of the image (user-provided or from vision analysis)

    Returns:
        Dictionary with layout structure information
    """
    desc_lower = description.lower()

    # Detect number of columns
    columns = 1
    if "two column" in desc_lower or "2 column" in desc_lower:
        columns = 2
    elif "three column" in desc_lower or "3 column" in desc_lower:
        columns = 3
    elif "four column" in desc_lower or "4 column" in desc_lower:
        columns = 4
    elif "multi" in desc_lower and "column" in desc_lower:
        columns = 3  # Default for multi-column

    # Detect sidebar
    has_sidebar = (
        "sidebar" in desc_lower
        or "side panel" in desc_lower
        or "left menu" in desc_lower
        or "navigation panel" in desc_lower
    )

    # Detect sections
    sections = []
    section_keywords = ["header", "title", "footer", "main", "content", "top", "bottom"]
    for keyword in section_keywords:
        if keyword in desc_lower:
            sections.append(keyword)

    return {
        "columns": columns,
        "has_sidebar": has_sidebar,
        "sections": sections,
        "complexity": "complex" if (columns > 2 or has_sidebar) else "simple",
    }


def create_enhanced_description(original_description: str, extracted_info: Dict[str, Any]) -> str:
    """
    Create an enhanced description combining user input and extracted information.

    Args:
        original_description: User's original drawing description
        extracted_info: Information extracted from analysis

    Returns:
        Enhanced description for the planner
    """
    features_str = ", ".join(extracted_info.get("features", []))
    page_type = extracted_info.get("page_type", "custom")

    enhanced = f"{original_description}\n\n"
    enhanced += f"Detected page type: {page_type}.\n"

    if features_str:
        enhanced += f"Identified components: {features_str}.\n"

    layout = extracted_info.get("layout_preference", "centered")
    enhanced += f"Layout style: {layout}."

    return enhanced
