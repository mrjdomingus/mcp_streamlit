"""Chat element tools for Streamlit MCP server.

This module provides tools for building chat interfaces:
- Chat message display
- Chat input widget
- Streaming text output
"""

from typing import Any, Dict, List, Optional

from ...utils.codegen import format_kwargs


def add_chat_message(role: str = "user", avatar: str | None = None) -> str:
    """Generate code for st.chat_message() - display a chat message bubble.

    Args:
        role: Message role - 'user', 'assistant', or 'ai' (default: 'user')
        avatar: Optional avatar - emoji, image path, or URL

    Returns:
        str: Generated Streamlit code with context manager
    """
    kwargs = {}
    if avatar:
        kwargs["avatar"] = avatar

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'''with st.chat_message("{role}", {kwargs_str}):
    st.write("Your message here")'''
    return f'''with st.chat_message("{role}"):
    st.write("Your message here")'''


def add_chat_input(placeholder: str = "Your message", key: str | None = None,
                   max_chars: int | None = None, disabled: bool = False,
                   on_submit: str | None = None) -> str:
    """Generate code for st.chat_input() - chat input widget at bottom of app.

    Args:
        placeholder: Placeholder text (default: "Your message")
        key: Widget key for session state
        max_chars: Maximum character limit
        disabled: Whether input is disabled (default: False)
        on_submit: Callback function name to call on submit

    Returns:
        str: Generated Streamlit code
    """
    kwargs = {}
    if key:
        kwargs["key"] = key
    if max_chars:
        kwargs["max_chars"] = max_chars
    if disabled:
        kwargs["disabled"] = disabled
    if on_submit:
        kwargs["on_submit"] = on_submit

    kwargs_str = format_kwargs(kwargs)
    if kwargs_str:
        return f'''prompt = st.chat_input("{placeholder}", {kwargs_str})
if prompt:
    # Handle user input
    st.write(f"User said: {{prompt}}")'''
    return f'''prompt = st.chat_input("{placeholder}")
if prompt:
    # Handle user input
    st.write(f"User said: {{prompt}}")'''


def add_write_stream(stream_source: str = "response_generator") -> str:
    """Generate code for st.write_stream() - stream text output with typewriter effect.

    Args:
        stream_source: Generator or iterable variable name (default: "response_generator")

    Returns:
        str: Generated Streamlit code
    """
    return f'''# Stream text with typewriter effect
st.write_stream({stream_source})

# Example generator:
# def response_generator():
#     for word in "Hello world! This is a streaming response.".split():
#         yield word + " "
#         time.sleep(0.1)'''


# MCP tool definitions
TOOLS = [
    {
        "name": "add_chat_message",
        "description": "Add a chat message bubble (st.chat_message). Use with context manager to display user or assistant messages in chat interfaces. Supports custom avatars.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "role": {
                    "type": "string",
                    "description": "Message role - 'user' for human messages, 'assistant' or 'ai' for bot messages",
                    "enum": ["user", "assistant", "ai"],
                    "default": "user"
                },
                "avatar": {
                    "type": "string",
                    "description": "Optional avatar - emoji (e.g., '👤', '🤖'), image path, or URL"
                }
            }
        }
    },
    {
        "name": "add_chat_input",
        "description": "Add a chat input widget (st.chat_input). Displays a fixed input box at the bottom of the app. Use for chat interfaces, Q&A bots, messaging apps.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "placeholder": {
                    "type": "string",
                    "description": "Placeholder text shown when input is empty",
                    "default": "Your message"
                },
                "key": {
                    "type": "string",
                    "description": "Widget key for accessing value in session state"
                },
                "max_chars": {
                    "type": "integer",
                    "description": "Maximum number of characters allowed"
                },
                "disabled": {
                    "type": "boolean",
                    "description": "Whether the input is disabled",
                    "default": False
                },
                "on_submit": {
                    "type": "string",
                    "description": "Callback function name to call when user submits"
                }
            }
        }
    },
    {
        "name": "add_write_stream",
        "description": "Add streaming text output (st.write_stream). Displays text with typewriter effect from a generator. Use for AI responses, live updates, streaming data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stream_source": {
                    "type": "string",
                    "description": "Generator or iterable variable name that yields text chunks",
                    "default": "response_generator"
                }
            }
        }
    }
]
