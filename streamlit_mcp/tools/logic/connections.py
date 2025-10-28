"""Data connection tools for Streamlit MCP server.

This module provides tools for connecting to data sources:
- st.connection() for various data sources
- SQL database connections
- Snowflake connections
- Custom connection implementations
"""




def add_sql_connection(
    connection_name: str = "sql", query: str | None = None, ttl: int | None = 600
) -> str:
    """Generate code for SQL database connection (st.connection with SQLConnection).

    Args:
        connection_name: Connection name defined in secrets.toml
        query: SQL query to execute (optional, generates example if not provided)
        ttl: Cache TTL in seconds (default: 600)

    Returns:
        str: Generated Streamlit code with SQL connection
    """
    if query:
        if ttl:
            return f'''# SQL database connection with caching
conn = st.connection("{connection_name}", type="sql")

# Query with caching (TTL: {ttl} seconds)
@st.cache_data(ttl={ttl})
def run_query(query):
    return conn.query(query, ttl={ttl})

df = run_query("""{query}""")
st.dataframe(df)'''
        else:
            return f'''# SQL database connection
conn = st.connection("{connection_name}", type="sql")
df = conn.query("""{query}""")
st.dataframe(df)'''
    else:
        return f"""# SQL database connection
conn = st.connection("{connection_name}", type="sql")

# Query with caching
@st.cache_data(ttl={ttl or 600})
def get_data():
    return conn.query("SELECT * FROM your_table LIMIT 100")

df = get_data()
st.dataframe(df)

# Alternative: Direct query without caching
# df = conn.query("SELECT * FROM your_table", ttl={ttl or 600})
# st.dataframe(df)"""


def add_snowflake_connection(
    connection_name: str = "snowflake", query: str | None = None, use_snowpark: bool = False
) -> str:
    """Generate code for Snowflake connection (st.connection with SnowflakeConnection).

    Args:
        connection_name: Connection name defined in secrets.toml
        query: SQL query to execute (optional)
        use_snowpark: Whether to use Snowpark session (default: False)

    Returns:
        str: Generated Streamlit code with Snowflake connection
    """
    if use_snowpark:
        return f"""# Snowflake connection with Snowpark
conn = st.connection("{connection_name}", type="snowflake")

# Use Snowpark session for DataFrame operations
@st.cache_data(ttl=600)
def get_data_snowpark():
    session = conn.session()
    df = session.table("your_table").limit(100).to_pandas()
    return df

df = get_data_snowpark()
st.dataframe(df)"""
    else:
        if query:
            return f'''# Snowflake connection
conn = st.connection("{connection_name}", type="snowflake")

# Query Snowflake
@st.cache_data(ttl=600)
def run_query(query):
    return conn.query(query)

df = run_query("""{query}""")
st.dataframe(df)'''
        else:
            return f"""# Snowflake connection
conn = st.connection("{connection_name}", type="snowflake")

# Query with caching
@st.cache_data(ttl=600)
def get_data():
    return conn.query("SELECT * FROM your_database.your_schema.your_table LIMIT 100")

df = get_data()
st.dataframe(df)

# Write data back to Snowflake (optional)
# conn.write_pandas(df, "target_table", auto_create_table=True)"""


def add_custom_connection(connection_name: str, connection_type: str | None = None) -> str:
    """Generate code for custom or generic data connection (st.connection).

    Args:
        connection_name: Connection name defined in secrets.toml
        connection_type: Connection type (e.g., 'sql', 'snowflake', custom class name)

    Returns:
        str: Generated Streamlit code with custom connection
    """
    if connection_type:
        return f"""# Custom data connection
conn = st.connection("{connection_name}", type="{connection_type}")

# Use connection methods based on your custom implementation
# Example: conn.query(), conn.cursor(), conn.session()

@st.cache_data(ttl=600)
def get_data():
    # Replace with your connection's data access method
    data = conn.query("your query or method call")
    return data

result = get_data()
st.write(result)"""
    else:
        return f"""# Generic data connection
conn = st.connection("{connection_name}")

# Access connection methods
@st.cache_data(ttl=600)
def get_data():
    # Replace with your connection's specific methods
    return conn.query("SELECT * FROM table")

df = get_data()
st.dataframe(df)"""


def generate_connection_config(connection_type: str = "sql", database: str = "postgresql") -> str:
    """Generate secrets.toml configuration for data connections.

    Args:
        connection_type: Type of connection - 'sql', 'snowflake', 'custom'
        database: For SQL connections - 'postgresql', 'mysql', 'sqlite', 'mssql', 'oracle'

    Returns:
        str: TOML configuration example
    """
    if connection_type == "sql":
        if database == "postgresql":
            return '''# .streamlit/secrets.toml - PostgreSQL Connection
[connections.sql]
dialect = "postgresql"
host = "localhost"
port = 5432
database = "your_database"
username = "your_username"
password = "your_password"

# Alternative: Use connection URL
# url = "postgresql://username:password@localhost:5432/database"'''

        elif database == "mysql":
            return '''# .streamlit/secrets.toml - MySQL Connection
[connections.sql]
dialect = "mysql"
host = "localhost"
port = 3306
database = "your_database"
username = "your_username"
password = "your_password"

# Alternative: Use connection URL
# url = "mysql://username:password@localhost:3306/database"'''

        elif database == "sqlite":
            return '''# .streamlit/secrets.toml - SQLite Connection
[connections.sql]
url = "sqlite:///your_database.db"

# For in-memory database:
# url = "sqlite:///:memory:"'''

        elif database == "mssql":
            return '''# .streamlit/secrets.toml - Microsoft SQL Server Connection
[connections.sql]
dialect = "mssql"
host = "localhost"
port = 1433
database = "your_database"
username = "your_username"
password = "your_password"
driver = "ODBC Driver 17 for SQL Server"

# Alternative: Use connection URL
# url = "mssql+pyodbc://username:password@localhost:1433/database?driver=ODBC+Driver+17+for+SQL+Server"'''

        elif database == "oracle":
            return '''# .streamlit/secrets.toml - Oracle Connection
[connections.sql]
dialect = "oracle"
host = "localhost"
port = 1521
database = "your_database"
username = "your_username"
password = "your_password"

# Alternative: Use connection URL
# url = "oracle://username:password@localhost:1521/database"'''

        else:
            return '''# .streamlit/secrets.toml - Generic SQL Connection
[connections.sql]
url = "dialect://username:password@host:port/database"

# Supported dialects: postgresql, mysql, sqlite, mssql, oracle
# Example: "postgresql://user:pass@localhost:5432/mydb"'''

    elif connection_type == "snowflake":
        return """# .streamlit/secrets.toml - Snowflake Connection
[connections.snowflake]
account = "your_account"
user = "your_username"
password = "your_password"
role = "your_role"
warehouse = "your_warehouse"
database = "your_database"
schema = "your_schema"

# Optional parameters:
# authenticator = "externalbrowser"  # For SSO
# private_key_file = "/path/to/key.p8"  # For key-pair auth"""

    elif connection_type == "custom":
        return """# .streamlit/secrets.toml - Custom Connection
[connections.my_connection]
# Add your custom connection parameters
api_key = "your_api_key"
endpoint = "https://api.example.com"
timeout = 30

# Parameters depend on your custom connection implementation
# See st.connections.BaseConnection for creating custom connections"""

    else:
        return '''# .streamlit/secrets.toml - Connection Configuration
[connections.your_connection]
# Add connection parameters based on your data source
# Examples: host, port, username, password, api_key, url, etc.

# For SQL databases:
# url = "dialect://username:password@host:port/database"

# For APIs:
# api_key = "your_api_key"
# endpoint = "https://api.example.com"'''


def generate_connection_pattern(pattern: str = "cached_query") -> str:
    """Generate code for common data connection patterns.

    Args:
        pattern: Pattern name - 'cached_query', 'parameterized_query', 'write_data', 'connection_pool'

    Returns:
        str: Generated Streamlit code with connection pattern
    """
    if pattern == "cached_query":
        return """# Cached query pattern for better performance
import streamlit as st

conn = st.connection("sql", type="sql")

@st.cache_data(ttl=600)
def load_data(query):
    return conn.query(query, ttl=600)

# Load data once, cache for 10 minutes
df = load_data("SELECT * FROM users WHERE active = true")
st.dataframe(df)

# Filter in Streamlit (not database)
filtered = df[df['role'] == st.selectbox('Role', df['role'].unique())]
st.dataframe(filtered)"""

    elif pattern == "parameterized_query":
        return """# Parameterized query pattern (safe from SQL injection)
import streamlit as st

conn = st.connection("sql", type="sql")

# User input
user_id = st.number_input("Enter User ID", min_value=1, value=1)

@st.cache_data(ttl=300)
def get_user_data(uid):
    # Use parameterized query for safety
    query = "SELECT * FROM users WHERE id = :user_id"
    return conn.query(query, params={"user_id": uid})

df = get_user_data(user_id)
st.dataframe(df)"""

    elif pattern == "write_data":
        return """# Write data pattern for Snowflake
import streamlit as st
import pandas as pd

conn = st.connection("snowflake", type="snowflake")

# User uploads data
uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    if st.button("Write to Snowflake"):
        with st.spinner("Writing to Snowflake..."):
            # Write data to Snowflake table
            conn.write_pandas(
                df,
                table_name="uploaded_data",
                database="my_database",
                schema="my_schema",
                auto_create_table=True
            )
        st.success("Data written successfully!")"""

    elif pattern == "connection_pool":
        return """# Connection pooling pattern for multiple queries
import streamlit as st

# Create connection (automatically pooled)
conn = st.connection("sql", type="sql")

# Multiple cached queries sharing the connection
@st.cache_data(ttl=600)
def get_users():
    return conn.query("SELECT * FROM users")

@st.cache_data(ttl=600)
def get_orders():
    return conn.query("SELECT * FROM orders")

@st.cache_data(ttl=600)
def get_products():
    return conn.query("SELECT * FROM products")

# Load all data using the same connection pool
users_df = get_users()
orders_df = get_orders()
products_df = get_products()

st.subheader("Users")
st.dataframe(users_df)

st.subheader("Orders")
st.dataframe(orders_df)

st.subheader("Products")
st.dataframe(products_df)"""

    else:
        return """# Custom connection pattern
import streamlit as st

conn = st.connection("your_connection")

# Your custom data access logic here
data = conn.query("your query")
st.write(data)"""


# MCP tool definitions
TOOLS = [
    {
        "name": "add_sql_connection",
        "description": "Add SQL database connection (st.connection with SQLConnection). Connect to PostgreSQL, MySQL, SQLite, SQL Server, Oracle. Use for querying relational databases with SQLAlchemy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "connection_name": {
                    "type": "string",
                    "description": "Connection name from secrets.toml",
                    "default": "sql",
                },
                "query": {
                    "type": "string",
                    "description": "SQL query to execute (e.g., 'SELECT * FROM users')",
                },
                "ttl": {
                    "type": "integer",
                    "description": "Cache TTL in seconds (default: 600)",
                    "default": 600,
                },
            },
        },
    },
    {
        "name": "add_snowflake_connection",
        "description": "Add Snowflake connection (st.connection with SnowflakeConnection). Connect to Snowflake data warehouse. Use for querying Snowflake, using Snowpark, writing data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "connection_name": {
                    "type": "string",
                    "description": "Connection name from secrets.toml",
                    "default": "snowflake",
                },
                "query": {"type": "string", "description": "SQL query to execute in Snowflake"},
                "use_snowpark": {
                    "type": "boolean",
                    "description": "Whether to use Snowpark session for DataFrame operations",
                    "default": False,
                },
            },
        },
    },
    {
        "name": "add_custom_connection",
        "description": "Add custom data connection (st.connection). Create connection to any data source with custom or built-in connection types. Use for APIs, custom databases, third-party services.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "connection_name": {
                    "type": "string",
                    "description": "Connection name from secrets.toml",
                },
                "connection_type": {
                    "type": "string",
                    "description": "Connection type (e.g., 'sql', 'snowflake', or custom class name)",
                },
            },
            "required": ["connection_name"],
        },
    },
    {
        "name": "generate_connection_config",
        "description": "Generate secrets.toml configuration for data connections. Creates configuration templates for SQL (PostgreSQL, MySQL, SQLite, SQL Server, Oracle), Snowflake, or custom connections.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "connection_type": {
                    "type": "string",
                    "description": "Type of connection configuration to generate",
                    "enum": ["sql", "snowflake", "custom"],
                    "default": "sql",
                },
                "database": {
                    "type": "string",
                    "description": "For SQL connections, specify database type",
                    "enum": ["postgresql", "mysql", "sqlite", "mssql", "oracle"],
                    "default": "postgresql",
                },
            },
        },
    },
    {
        "name": "generate_connection_pattern",
        "description": "Generate common data connection patterns. Pre-built implementations for cached queries, parameterized queries, writing data, connection pooling.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Connection pattern to generate",
                    "enum": [
                        "cached_query",
                        "parameterized_query",
                        "write_data",
                        "connection_pool",
                    ],
                    "default": "cached_query",
                }
            },
        },
    },
]
