"""Authentication tools for Streamlit MCP server.

This module provides tools for user authentication with OIDC providers:
- Login with st.login()
- Logout with st.logout()
- User information with st.user
- Authentication patterns
"""




def add_login(provider: str | None = None, button_text: str = "Log in") -> str:
    """Generate code for st.login() - authenticate with OIDC provider.

    Args:
        provider: OIDC provider name (if using multiple providers, e.g., 'google', 'microsoft')
        button_text: Text for the login button

    Returns:
        str: Generated Streamlit code with login flow
    """
    if provider:
        return f"""# Login with specific OIDC provider
if not st.user.is_logged_in:
    if st.button("{button_text}"):
        st.login("{provider}")
    st.stop()

# User is logged in - continue with app
st.write(f"Welcome, {{st.user.name}}!")"""
    else:
        return f"""# Login with default OIDC provider
if not st.user.is_logged_in:
    if st.button("{button_text}"):
        st.login()
    st.stop()

# User is logged in - continue with app
st.write(f"Welcome, {{st.user.name}}!")"""


def add_logout(button_text: str = "Log out") -> str:
    """Generate code for st.logout() - log out and clear identity.

    Args:
        button_text: Text for the logout button

    Returns:
        str: Generated Streamlit code
    """
    return f"""# Logout button
if st.button("{button_text}"):
    st.logout()"""


def check_user_status() -> str:
    """Generate code to check st.user authentication status and display user info.

    Returns:
        str: Generated Streamlit code with user status check
    """
    return """# Check user authentication status
if st.user.is_logged_in:
    st.success(f"Logged in as: {st.user.name}")
    st.write(f"Email: {st.user.email}")

    # Access all user info as dict
    user_dict = st.user.to_dict()
    st.json(user_dict)
else:
    st.warning("Not logged in")"""


def generate_auth_pattern(pattern: str = "single_provider") -> str:
    """Generate code for common authentication patterns.

    Args:
        pattern: Pattern name - 'single_provider', 'multi_provider', 'protected_page', 'admin_check'

    Returns:
        str: Generated Streamlit code with authentication pattern
    """
    if pattern == "single_provider":
        return """# Single OIDC provider authentication
import streamlit as st

if not st.user.is_logged_in:
    st.title("Welcome!")
    st.write("Please log in to continue.")
    if st.button("Log in with Google"):
        st.login()
    st.stop()

# Main app content for logged-in users
st.title("Dashboard")
st.write(f"Hello, {st.user.name}!")

if st.button("Log out"):
    st.logout()"""

    elif pattern == "multi_provider":
        return """# Multiple OIDC provider authentication
import streamlit as st

if not st.user.is_logged_in:
    st.title("Welcome!")
    st.write("Please log in with your preferred provider.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Log in with Google"):
            st.login("google")
    with col2:
        if st.button("Log in with Microsoft"):
            st.login("microsoft")
    st.stop()

# Main app content
st.title("Dashboard")
st.write(f"Hello, {st.user.name}!")

if st.button("Log out"):
    st.logout()"""

    elif pattern == "protected_page":
        return """# Protected page with authentication
import streamlit as st

# Redirect to login if not authenticated
if not st.user.is_logged_in:
    st.error("This page requires authentication")
    if st.button("Go to Login"):
        st.login()
    st.stop()

# Protected content
st.title("Protected Dashboard")
st.write(f"Welcome back, {st.user.name}!")
st.write("This content is only visible to authenticated users.")

# Logout option
with st.sidebar:
    if st.button("Log out"):
        st.logout()"""

    elif pattern == "admin_check":
        return """# Admin role check with authentication
import streamlit as st

# Check if user is logged in
if not st.user.is_logged_in:
    st.error("Please log in")
    if st.button("Log in"):
        st.login()
    st.stop()

# Check if user is admin (customize based on your provider's claims)
admin_emails = ["admin@example.com", "superuser@example.com"]
is_admin = st.user.email in admin_emails

if is_admin:
    st.title("Admin Dashboard")
    st.success(f"Welcome, Admin {st.user.name}")

    # Admin-only features
    st.header("Admin Controls")
    st.button("Manage Users")
    st.button("View Analytics")
else:
    st.title("User Dashboard")
    st.info(f"Welcome, {st.user.name}")
    st.write("Standard user access")

# Logout for all users
if st.button("Log out"):
    st.logout()"""

    else:
        return """# Custom authentication pattern
import streamlit as st

if not st.user.is_logged_in:
    if st.button("Log in"):
        st.login()
    st.stop()

st.write(f"Hello, {st.user.name}!")"""


def generate_secrets_config(provider: str = "google", multi_provider: bool = False) -> str:
    """Generate secrets.toml configuration for authentication.

    Args:
        provider: OIDC provider - 'google', 'microsoft', 'auth0', 'okta', 'generic'
        multi_provider: Whether to generate config for multiple providers

    Returns:
        str: TOML configuration example
    """
    if multi_provider:
        return '''# .streamlit/secrets.toml - Multiple OIDC providers
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-strong-random-secret-here"

[auth.google]
client_id = "your-google-client-id"
client_secret = "your-google-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

[auth.microsoft]
client_id = "your-microsoft-client-id"
client_secret = "your-microsoft-client-secret"
server_metadata_url = "https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration"

# For production, update redirect_uri to your deployed app URL
# redirect_uri = "https://your-app.streamlit.app/oauth2callback"'''

    else:
        if provider == "google":
            return '''# .streamlit/secrets.toml - Google Identity
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-strong-random-secret-here"
client_id = "your-google-client-id.apps.googleusercontent.com"
client_secret = "your-google-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

# For production, update redirect_uri to your deployed app URL
# redirect_uri = "https://your-app.streamlit.app/oauth2callback"'''

        elif provider == "microsoft":
            return """# .streamlit/secrets.toml - Microsoft Entra ID
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-strong-random-secret-here"
client_id = "your-microsoft-client-id"
client_secret = "your-microsoft-client-secret"
server_metadata_url = "https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration"

# Replace {tenant} with: common, organizations, consumers, or your tenant ID
# For production, update redirect_uri to your deployed app URL"""

        elif provider == "auth0":
            return """# .streamlit/secrets.toml - Auth0
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-strong-random-secret-here"
client_id = "your-auth0-client-id"
client_secret = "your-auth0-client-secret"
server_metadata_url = "https://{account}.{region}.auth0.com/.well-known/openid-configuration"
client_kwargs = { "prompt" = "login" }

# Replace {account} and {region} with your Auth0 values
# For production, update redirect_uri to your deployed app URL"""

        elif provider == "okta":
            return """# .streamlit/secrets.toml - Okta
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-strong-random-secret-here"
client_id = "your-okta-client-id"
client_secret = "your-okta-client-secret"
server_metadata_url = "https://{your-okta-domain}/oauth2/default/.well-known/openid-configuration"

# Replace {your-okta-domain} with your Okta domain
# For production, update redirect_uri to your deployed app URL"""

        else:  # generic
            return """# .streamlit/secrets.toml - Generic OIDC Provider
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "your-strong-random-secret-here"
client_id = "your-client-id"
client_secret = "your-client-secret"
server_metadata_url = "https://your-provider.com/.well-known/openid-configuration"

# Optional: Customize OIDC parameters
# client_kwargs = { "prompt" = "select_account", "scope" = "openid profile email" }

# For production, update redirect_uri to your deployed app URL"""


# MCP tool definitions
TOOLS = [
    {
        "name": "add_login",
        "description": "Add user login (st.login). Redirects to OIDC provider for authentication. Use for apps requiring user identity, authentication flows, protected content.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "provider": {
                    "type": "string",
                    "description": "OIDC provider name (e.g., 'google', 'microsoft', 'auth0'). Required only if using multiple providers.",
                },
                "button_text": {
                    "type": "string",
                    "description": "Text for the login button",
                    "default": "Log in",
                },
            },
        },
    },
    {
        "name": "add_logout",
        "description": "Add user logout (st.logout). Removes identity cookie and starts new session. Use for sign-out functionality, session termination.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "button_text": {
                    "type": "string",
                    "description": "Text for the logout button",
                    "default": "Log out",
                }
            },
        },
    },
    {
        "name": "check_user_status",
        "description": "Check user authentication status (st.user). Display user info like name, email, login status. Use for personalizing content, showing user profile.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "generate_auth_pattern",
        "description": "Generate common authentication patterns. Pre-built implementations for single/multi-provider login, protected pages, admin checks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Authentication pattern to generate",
                    "enum": ["single_provider", "multi_provider", "protected_page", "admin_check"],
                    "default": "single_provider",
                }
            },
        },
    },
    {
        "name": "generate_secrets_config",
        "description": "Generate secrets.toml configuration for OIDC authentication. Creates configuration template for Google, Microsoft, Auth0, Okta, or generic providers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "provider": {
                    "type": "string",
                    "description": "OIDC provider to configure",
                    "enum": ["google", "microsoft", "auth0", "okta", "generic"],
                    "default": "google",
                },
                "multi_provider": {
                    "type": "boolean",
                    "description": "Whether to generate config for multiple providers",
                    "default": False,
                },
            },
        },
    },
]
