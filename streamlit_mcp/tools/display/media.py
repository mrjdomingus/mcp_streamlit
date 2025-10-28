"""Media element tools for Streamlit MCP server.

This module provides tools for displaying media content:
- Images
- Audio files
- Video files
- App logo
- External links
"""


from ...utils.codegen import format_kwargs


def add_image(
    image_source: str,
    caption: str | None = None,
    width: int | None = None,
    use_column_width: bool | None = None,
    channels: str = "RGB",
    output_format: str = "auto",
) -> str:
    """Generate code for st.image() - display an image.

    Args:
        image_source: Image source - file path, URL, or variable name
        caption: Optional caption text below the image
        width: Image width in pixels (None = original size)
        use_column_width: If True/False/None, controls column width behavior
        channels: Channel order - 'RGB' or 'BGR' (default: 'RGB')
        output_format: Output format - 'JPEG', 'PNG', or 'auto' (default: 'auto')

    Returns:
        str: Generated Streamlit code
    """
    kwargs = {}
    if caption:
        kwargs["caption"] = caption
    if width is not None:
        kwargs["width"] = width
    if use_column_width is not None:
        kwargs["use_column_width"] = use_column_width
    if channels != "RGB":
        kwargs["channels"] = channels
    if output_format != "auto":
        kwargs["output_format"] = output_format

    # Determine if source is a URL/path (string) or variable
    if image_source.startswith(("http://", "https://", "/", "./")):
        source_str = f'"{image_source}"'
    else:
        source_str = image_source

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f"st.image({source_str}, {kwargs_str})"
    return f"st.image({source_str})"


def add_audio(
    audio_source: str,
    format: str = "audio/wav",
    start_time: int = 0,
    sample_rate: int | None = None,
    end_time: int | None = None,
    loop: bool = False,
    autoplay: bool = False,
) -> str:
    """Generate code for st.audio() - display an audio player.

    Args:
        audio_source: Audio source - file path, URL, or variable name
        format: MIME type (e.g., 'audio/wav', 'audio/mp3', 'audio/ogg')
        start_time: Start time in seconds (default: 0)
        sample_rate: Sample rate in Hz (optional)
        end_time: End time in seconds (optional)
        loop: Whether to loop the audio (default: False)
        autoplay: Whether to autoplay (default: False)

    Returns:
        str: Generated Streamlit code
    """
    kwargs = {}
    if format != "audio/wav":
        kwargs["format"] = format
    if start_time != 0:
        kwargs["start_time"] = start_time
    if sample_rate is not None:
        kwargs["sample_rate"] = sample_rate
    if end_time is not None:
        kwargs["end_time"] = end_time
    if loop:
        kwargs["loop"] = loop
    if autoplay:
        kwargs["autoplay"] = autoplay

    # Determine if source is a URL/path (string) or variable
    if audio_source.startswith(("http://", "https://", "/", "./")):
        source_str = f'"{audio_source}"'
    else:
        source_str = audio_source

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f"st.audio({source_str}, {kwargs_str})"
    return f"st.audio({source_str})"


def add_video(
    video_source: str,
    format: str = "video/mp4",
    start_time: int = 0,
    end_time: int | None = None,
    loop: bool = False,
    autoplay: bool = False,
    muted: bool = False,
    subtitles: str | None = None,
) -> str:
    """Generate code for st.video() - display a video player.

    Args:
        video_source: Video source - file path, URL, or variable name
        format: MIME type (e.g., 'video/mp4', 'video/webm', 'video/ogg')
        start_time: Start time in seconds (default: 0)
        end_time: End time in seconds (optional)
        loop: Whether to loop the video (default: False)
        autoplay: Whether to autoplay (default: False)
        muted: Whether to mute audio (default: False)
        subtitles: Path to subtitles file (optional)

    Returns:
        str: Generated Streamlit code
    """
    kwargs = {}
    if format != "video/mp4":
        kwargs["format"] = format
    if start_time != 0:
        kwargs["start_time"] = start_time
    if end_time is not None:
        kwargs["end_time"] = end_time
    if loop:
        kwargs["loop"] = loop
    if autoplay:
        kwargs["autoplay"] = autoplay
    if muted:
        kwargs["muted"] = muted
    if subtitles:
        kwargs["subtitles"] = subtitles

    # Determine if source is a URL/path (string) or variable
    if video_source.startswith(("http://", "https://", "/", "./")):
        source_str = f'"{video_source}"'
    else:
        source_str = video_source

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f"st.video({source_str}, {kwargs_str})"
    return f"st.video({source_str})"


def add_logo(
    image_source: str, link: str | None = None, icon_image: str | None = None, size: str = "medium"
) -> str:
    """Generate code for st.logo() - display a logo in the sidebar and navigation.

    Args:
        image_source: Logo image source - file path, URL, or variable name
        link: Optional URL to navigate to when clicking the logo
        icon_image: Optional icon image for collapsed sidebar
        size: Logo size - 'small', 'medium', or 'large' (default: 'medium')

    Returns:
        str: Generated Streamlit code
    """
    kwargs = {}
    if link:
        kwargs["link"] = link
    if icon_image:
        kwargs["icon_image"] = icon_image
    if size != "medium":
        kwargs["size"] = size

    # Determine if source is a URL/path (string) or variable
    if image_source.startswith(("http://", "https://", "/", "./")):
        source_str = f'"{image_source}"'
    else:
        source_str = image_source

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f"st.logo({source_str}, {kwargs_str})"
    return f"st.logo({source_str})"


def add_link_button(
    label: str,
    url: str,
    help: str | None = None,
    type: str = "secondary",
    disabled: bool = False,
    use_container_width: bool = False,
    icon: str | None = None,
) -> str:
    """Generate code for st.link_button() - display a button that opens a URL.

    Args:
        label: Button text
        url: URL to open when clicked
        help: Optional tooltip text
        type: Button type - 'primary', 'secondary', or 'tertiary' (default: 'secondary')
        disabled: Whether button is disabled (default: False)
        use_container_width: Whether to expand to container width (default: False)
        icon: Optional emoji icon (e.g., '🔗', '🌐')

    Returns:
        str: Generated Streamlit code
    """
    kwargs = {}
    if help:
        kwargs["help"] = help
    if type != "secondary":
        kwargs["type"] = type
    if disabled:
        kwargs["disabled"] = disabled
    if use_container_width:
        kwargs["use_container_width"] = use_container_width
    if icon:
        kwargs["icon"] = icon

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'st.link_button("{label}", "{url}", {kwargs_str})'
    return f'st.link_button("{label}", "{url}")'


# MCP tool definitions
TOOLS = [
    {
        "name": "add_image",
        "description": "Add an image display (st.image). Supports local files, URLs, PIL images, numpy arrays. Use for photos, charts, diagrams, logos.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_source": {
                    "type": "string",
                    "description": "Image source - file path (e.g., 'image.png'), URL, or variable name (e.g., 'img_array')",
                },
                "caption": {
                    "type": "string",
                    "description": "Optional caption text to display below the image",
                },
                "width": {
                    "type": "integer",
                    "description": "Image width in pixels (None = original size)",
                },
                "use_column_width": {
                    "type": "boolean",
                    "description": "If True, fit to column width. If 'auto', fit to column for large images",
                },
                "channels": {
                    "type": "string",
                    "description": "Channel order for numpy arrays",
                    "enum": ["RGB", "BGR"],
                    "default": "RGB",
                },
                "output_format": {
                    "type": "string",
                    "description": "Output image format",
                    "enum": ["JPEG", "PNG", "auto"],
                    "default": "auto",
                },
            },
            "required": ["image_source"],
        },
    },
    {
        "name": "add_audio",
        "description": "Add an audio player (st.audio). Supports WAV, MP3, OGG formats. Use for music, podcasts, sound effects, voice recordings.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "audio_source": {
                    "type": "string",
                    "description": "Audio source - file path (e.g., 'audio.mp3'), URL, or variable name (e.g., 'audio_bytes')",
                },
                "format": {
                    "type": "string",
                    "description": "MIME type of the audio",
                    "enum": ["audio/wav", "audio/mp3", "audio/ogg", "audio/flac"],
                    "default": "audio/wav",
                },
                "start_time": {
                    "type": "integer",
                    "description": "Start playback at this time (seconds)",
                    "default": 0,
                },
                "sample_rate": {
                    "type": "integer",
                    "description": "Sample rate in Hz (for numpy arrays)",
                },
                "end_time": {
                    "type": "integer",
                    "description": "End playback at this time (seconds)",
                },
                "loop": {
                    "type": "boolean",
                    "description": "Whether to loop the audio",
                    "default": False,
                },
                "autoplay": {
                    "type": "boolean",
                    "description": "Whether to autoplay when rendered",
                    "default": False,
                },
            },
            "required": ["audio_source"],
        },
    },
    {
        "name": "add_video",
        "description": "Add a video player (st.video). Supports MP4, WebM, OGG formats. Use for tutorials, demos, presentations, recordings.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_source": {
                    "type": "string",
                    "description": "Video source - file path (e.g., 'video.mp4'), URL (YouTube, Vimeo), or variable name",
                },
                "format": {
                    "type": "string",
                    "description": "MIME type of the video",
                    "enum": ["video/mp4", "video/webm", "video/ogg"],
                    "default": "video/mp4",
                },
                "start_time": {
                    "type": "integer",
                    "description": "Start playback at this time (seconds)",
                    "default": 0,
                },
                "end_time": {
                    "type": "integer",
                    "description": "End playback at this time (seconds)",
                },
                "loop": {
                    "type": "boolean",
                    "description": "Whether to loop the video",
                    "default": False,
                },
                "autoplay": {
                    "type": "boolean",
                    "description": "Whether to autoplay when rendered",
                    "default": False,
                },
                "muted": {
                    "type": "boolean",
                    "description": "Whether to mute audio",
                    "default": False,
                },
                "subtitles": {"type": "string", "description": "Path to VTT subtitles file"},
            },
            "required": ["video_source"],
        },
    },
    {
        "name": "add_logo",
        "description": "Add a logo image to sidebar and navigation (st.logo). Use for branding, company logo, app identity. Appears in sidebar and page navigation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_source": {
                    "type": "string",
                    "description": "Logo image source - file path (e.g., 'logo.png'), URL, or variable name",
                },
                "link": {
                    "type": "string",
                    "description": "Optional URL to navigate to when clicking the logo",
                },
                "icon_image": {
                    "type": "string",
                    "description": "Optional icon image for collapsed sidebar (file path or URL)",
                },
                "size": {
                    "type": "string",
                    "description": "Logo size",
                    "enum": ["small", "medium", "large"],
                    "default": "medium",
                },
            },
            "required": ["image_source"],
        },
    },
    {
        "name": "add_link_button",
        "description": "Add a button that opens a URL (st.link_button). Use for external links, documentation, social media, download links.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "label": {"type": "string", "description": "Button text label"},
                "url": {"type": "string", "description": "URL to open when clicked"},
                "help": {"type": "string", "description": "Optional tooltip text shown on hover"},
                "type": {
                    "type": "string",
                    "description": "Button visual style",
                    "enum": ["primary", "secondary", "tertiary"],
                    "default": "secondary",
                },
                "disabled": {
                    "type": "boolean",
                    "description": "Whether the button is disabled",
                    "default": False,
                },
                "use_container_width": {
                    "type": "boolean",
                    "description": "Whether to expand button to container width",
                    "default": False,
                },
                "icon": {
                    "type": "string",
                    "description": "Optional emoji icon (e.g., '🔗', '🌐', '📄')",
                },
            },
            "required": ["label", "url"],
        },
    },
]
