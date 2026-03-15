"""
AI SQL Query Generator — Convert natural language to SQL queries and execute them.
Upload database schema via SQL dump file or text input, ask questions in plain English,
and get SQL queries generated and executed with results displayed.
Author: Rayees Yousuf (@RayeesYousufGenAi)
"""

import os
import re
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
import sqlparse

load_dotenv()

# Validate OPENAI_API_KEY before creating client
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is required")

st.set_page_config(page_title="🗄️ AI SQL Query Generator", page_icon="🗄️", layout="wide")
st.title("🗄️ AI SQL Query Generator")
st.caption("Upload your database schema and ask questions in plain English to generate SQL queries")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Initialize SQLite in-memory database
@st.cache_resource
def get_database_engine():
    """Create and return an in-memory SQLite engine."""
    return create_engine("sqlite:///:memory:", echo=False)


def extract_schema_from_sql(sql_content: str) -> str:
    """Extract CREATE TABLE statements from SQL dump."""
    # Remove comments
    sql_content = re.sub(r'--.*?\n', '\n', sql_content)
    sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)

    # Find CREATE TABLE statements
    create_pattern = r'CREATE\s+TABLE\s+[^;]+;'
    matches = re.findall(create_pattern, sql_content, re.IGNORECASE | re.DOTALL)

    if matches:
        return '\n\n'.join(matches)
    return sql_content.strip()


def execute_schema_sql(engine, sql_content: str) -> tuple[bool, str]:
    """Execute SQL schema statements to set up the database."""
    try:
        # Split SQL into individual statements using sqlparse for better parsing
        parsed_statements = sqlparse.parse(sql_content)
        statements = [stmt for stmt in parsed_statements if stmt.strip()]

        # Limit number of statements to prevent DoS from large uploads
        MAX_STATEMENTS = 500
        if len(statements) > MAX_STATEMENTS:
            return False, f"Too many SQL statements. Maximum allowed: {MAX_STATEMENTS}"

        # Allowed statement types for schema initialization
        ALLOWED_TYPES = {'CREATE', 'INSERT', 'ALTER', 'DROP'}
        # Keywords that are dangerous (e.g., DROP DATABASE, DROP TABLE hints)
        DANGEROUS_KEYWORDS = {'DATABASE', 'USER', 'ROLE'}

        with engine.connect() as conn:
            for statement in statements:
                stmt_str = str(statement).strip()
                if not stmt_str:
                    continue

                # Parse the statement to get token types
                parsed = sqlparse.parse(stmt_str)[0]
                first_token = parsed.token_first()

                if not first_token:
                    continue

                # Get the statement type from the first token
                token_value = first_token.value.upper()

                # Strict validation: only allow CREATE/INSERT/ALTER statements
                if token_value in ALLOWED_TYPES:
                    # Additional safety check for dangerous keywords
                    stmt_upper = stmt_str.upper()
                    if any(kw in stmt_upper for kw in DANGEROUS_KEYWORDS):
                        return False, f"SQL Error: Dangerous keyword detected in: {stmt_str[:50]}..."

                    conn.execute(text(stmt_str))

            conn.commit()
        return True, "Schema loaded successfully"
    except SQLAlchemyError as e:
        return False, f"SQL Error: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def get_schema_info(engine) -> dict:
    """Extract schema information from the database."""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        schema_info = {}

        for table in tables:
            columns = inspector.get_columns(table)
            schema_info[table] = [
                {
                    "name": col["name"],
                    "type": str(col["type"]),
                }
                for col in columns
            ]

        return schema_info
    except Exception:
        return {}


def schema_to_text(schema_info: dict) -> str:
    """Convert schema info to a text representation for the LLM."""
    lines = []
    lines.append("Database Schema:")
    lines.append("-" * 40)

    for table_name, columns in schema_info.items():
        lines.append(f"\nTable: {table_name}")
        lines.append("Columns:")
        for col in columns:
            lines.append(f"  - {col['name']} ({col['type']})")

    return "\n".join(lines)


def detect_prompt_injection(question: str) -> tuple[bool, str]:
    """Detect potential prompt injection attempts in user input."""
    # Suspicious patterns that indicate prompt injection
    suspicious_patterns = [
        r'ignore\s+(previous|above|all)\s+(instructions?|context|text)',
        r'forget\s+(everything|all|previous)',
        r'you\s+are\s+now',
        r'act\s+as\s+(if|though)',
        r'pretend\s+to\s+be',
        r'system\s*:',  # Attempting to set system role
        r'user\s*:',  # Attempting to inject user messages
        r'assistant\s*:',  # Attempting to inject assistant responses
        r'do\s+(not|not\s+any)\s+(explain|return|provide)',
        r'{.*}.*\n*{.*}',  # Multiple braces/brackets that might be trying to format
    ]

    question_lower = question.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, question_lower):
            return True, f"Potential prompt injection detected: pattern '{pattern}'"

    # Check for unusual characters that might be injection attempts
    if question.count('"') > 10 or question.count("'") > 10:
        return True, "Excessive quote characters detected"

    return False, ""


def generate_sql_query(client: OpenAI, schema: str, question: str) -> tuple[str, str]:
    """Use OpenAI GPT-4 to generate SQL from natural language."""
    # Check for prompt injection before processing
    is_suspicious, injection_msg = detect_prompt_injection(question)
    if is_suspicious:
        return "", f"Security Error: {injection_msg}"

    try:
        prompt = f"""Given the following database schema:

{schema}

Convert this natural language question to a valid SQL query:
"{question}"

Provide ONLY the SQL query without any explanation, markdown formatting, or code blocks.
The query should be compatible with SQLite syntax."""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert SQL query generator. "
                        "Convert natural language questions to accurate SQL queries. "
                        "Return only the SQL query, no explanations or markdown. "
                        "IMPORTANT: Only generate SELECT queries. Do NOT generate DELETE, UPDATE, INSERT, DROP, or other modifying statements."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            timeout=30.0,  # 30 second timeout to prevent indefinite hangs
        )

        sql = response.choices[0].message.content.strip()
        # Remove markdown code blocks if present
        sql = re.sub(r'```sql\s*', '', sql)
        sql = re.sub(r'```\s*$', '', sql)
        sql = sql.strip()

        return sql, ""
    except Exception as e:
        return "", f"Error generating SQL: {str(e)}"


def is_safe_sql_query(query: str) -> tuple[bool, str]:
    """Validate that a SQL query is safe to execute."""
    # Parse the query using sqlparse
    parsed = sqlparse.parse(query)

    if not parsed:
        return False, "Could not parse SQL query"

    # Only allow SELECT statements
    for statement in parsed:
        if not statement.strip():
            continue

        first_token = statement.token_first()
        if not first_token:
            return False, "Empty SQL statement"

        token_type = first_token.ttype
        token_value = first_token.value.upper()

        # Only allow SELECT statements (not INSERT, UPDATE, DELETE, DROP, etc.)
        if token_value != 'SELECT':
            return False, f"Only SELECT queries are allowed. Found: {token_value}"

        # Check for dangerous keywords in the query
        dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'EXEC', 'EXECUTE', 'CALL']
        query_upper = query.upper()
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False, f"Query contains dangerous keyword: {keyword}"

    return True, ""


def execute_query(engine, query: str) -> tuple[list, list, str]:
    """Execute SQL query and return results."""
    # Validate query before execution
    is_safe, error_msg = is_safe_sql_query(query)
    if not is_safe:
        return [], [], f"SQL Security Error: {error_msg}"

    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            columns = list(result.keys())
            rows = result.fetchall()
            return rows, columns, ""
    except SQLAlchemyError as e:
        return [], [], f"SQL Execution Error: {str(e)}"
    except Exception as e:
        return [], [], f"Error: {str(e)}"


# Sidebar for schema input
tab1, tab2 = st.tabs(["📁 Upload SQL Dump", "📝 Paste Schema"])

with tab1:
    st.subheader("Upload SQL Dump File")
    uploaded_file = st.file_uploader("Upload your SQL schema file (.sql)", type=["sql"])

with tab2:
    st.subheader("Paste Schema Directly")
    schema_text = st.text_area(
        "Paste your CREATE TABLE statements here:",
        height=200,
        placeholder="CREATE TABLE users (\n  id INTEGER PRIMARY KEY,\n  name TEXT\n);",
    )

# Main content area
st.markdown("---")

# Get database engine
engine = get_database_engine()

# Process schema input
schema_loaded = False
schema_info = {}

if uploaded_file is not None:
    sql_content = uploaded_file.getvalue().decode("utf-8")
    success, message = execute_schema_sql(engine, sql_content)

    if success:
        schema_info = get_schema_info(engine)
        schema_loaded = True
        st.success(f"✅ {message}")
    else:
        st.error(f"❌ {message}")

elif schema_text.strip():
    success, message = execute_schema_sql(engine, schema_text)

    if success:
        schema_info = get_schema_info(engine)
        schema_loaded = True
        st.success(f"✅ {message}")
    else:
        st.error(f"❌ {message}")

# Display schema preview
if schema_loaded and schema_info:
    st.subheader("📋 Database Schema")
    for table_name, columns in schema_info.items():
        with st.expander(f"Table: {table_name}"):
            col_data = [{"Column": col["name"], "Type": col["type"]} for col in columns]
            st.dataframe(col_data, use_container_width=True, hide_index=True)

    # Natural language query input
    st.markdown("---")
    st.subheader("💬 Ask a Question in Natural Language")

    question = st.text_input(
        "What would you like to query?",
        placeholder="e.g., Show me all users who joined in 2024",
    )

    if st.button("🧠 Generate SQL", type="primary") and question:
        with st.spinner("Generating SQL query..."):
            schema_text_for_llm = schema_to_text(schema_info)
            sql_query, error = generate_sql_query(client, schema_text_for_llm, question)

        if error:
            st.error(error)
        else:
            st.markdown("### 📝 Generated SQL Query")
            st.code(sql_query, language="sql")

            # Execute the query
            with st.spinner("Executing query..."):
                rows, columns, exec_error = execute_query(engine, sql_query)

            if exec_error:
                st.error(f"❌ {exec_error}")
            else:
                st.markdown("### 📊 Query Results")

                if len(rows) == 0:
                    st.info("Query executed successfully. No rows returned.")
                else:
                    # Convert to dictionary format for dataframe
                    result_data = [dict(zip(columns, row)) for row in rows]
                    st.dataframe(result_data, use_container_width=True)

                    st.caption(f"Showing {len(rows)} row(s)")

else:
    st.info("👈 Upload a SQL file or paste your schema above to get started!")
