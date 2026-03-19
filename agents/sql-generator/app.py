"""
AI SQL Query Generator — Convert natural language to SQL queries and execute them.
Upload database schema via SQL dump file or text input, ask questions in plain English,
and get SQL queries generated and executed with results displayed.
Author: llrightll (@llrightll)
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

st.set_page_config(page_title="🗄️ AI SQL Query Generator", page_icon="🗄️", layout="wide")
st.title("🗄️ AI SQL Query Generator")
st.caption("Upload your database schema and ask questions in plain English to generate SQL queries")

# Authentication
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.warning("Please provide an OpenAI API Key in the sidebar to continue.")
    st.stop()

client = OpenAI(api_key=api_key)

# Initialize SQLite in-memory database
if "db_engine" not in st.session_state:
    st.session_state.db_engine = create_engine("sqlite:///:memory:", echo=False)

engine = st.session_state.db_engine

def extract_schema_from_sql(sql_content: str) -> str:
    """Extract CREATE TABLE statements from SQL dump."""
    sql_content = re.sub(r'--.*?\n', '\n', sql_content)
    sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
    create_pattern = r'CREATE\s+TABLE\s+[^;]+;'
    matches = re.findall(create_pattern, sql_content, re.IGNORECASE | re.DOTALL)
    if matches:
        return '\n\n'.join(matches)
    return sql_content.strip()

def execute_schema_sql(engine, sql_content: str) -> tuple[bool, str]:
    """Execute SQL schema statements to set up the database."""
    try:
        parsed_statements = sqlparse.parse(sql_content)
        statements = [stmt for stmt in parsed_statements if str(stmt).strip()]
        MAX_STATEMENTS = 500
        if len(statements) > MAX_STATEMENTS:
            return False, f"Too many SQL statements. Maximum allowed: {MAX_STATEMENTS}"
        ALLOWED_TYPES = {'CREATE', 'INSERT', 'ALTER', 'DROP'}
        DANGEROUS_KEYWORDS = {'DATABASE', 'USER', 'ROLE'}
        with engine.connect() as conn:
            for statement in statements:
                stmt_str = str(statement).strip()
                if not stmt_str: continue
                parsed = sqlparse.parse(stmt_str)[0]
                first_token = parsed.token_first()
                if not first_token: continue
                token_value = first_token.value.upper()
                if token_value in ALLOWED_TYPES:
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
            schema_info[table] = [{"name": col["name"], "type": str(col["type"])} for col in columns]
        return schema_info
    except Exception:
        return {}

def schema_to_text(schema_info: dict) -> str:
    """Convert schema info to a text representation for the LLM."""
    lines = ["Database Schema:", "-" * 40]
    for table_name, columns in schema_info.items():
        lines.append(f"\nTable: {table_name}")
        lines.append("Columns:")
        for col in columns:
            lines.append(f"  - {col['name']} ({col['type']})")
    return "\n".join(lines)

def detect_prompt_injection(question: str) -> tuple[bool, str]:
    """Detect potential prompt injection attempts in user input."""
    suspicious_patterns = [
        r'ignore\s+(previous|above|all)\s+(instructions?|context|text)',
        r'forget\s+(everything|all|previous)',
        r'you\s+are\s+now',
        r'act\s+as\s+(if|though)',
        r'pretend\s+to\s+be',
        r'system\s*:', r'user\s*:', r'assistant\s*:',
        r'do\s+(not|not\s+any)\s+(explain|return|provide)',
    ]
    question_lower = question.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, question_lower):
            return True, f"Potential prompt injection detected: pattern '{pattern}'"
    if question.count('"') > 10 or question.count("'") > 10:
        return True, "Excessive quote characters detected"
    return False, ""

def generate_sql_query(client, schema: str, question: str) -> tuple[str, str]:
    """Use OpenAI GPT-4 to generate SQL from natural language."""
    is_suspicious, injection_msg = detect_prompt_injection(question)
    if is_suspicious: return "", f"Security Error: {injection_msg}"
    try:
        prompt = f"Given the following database schema:\n\n{schema}\n\nConvert this natural language question to a valid SQL query:\n\"{question}\"\n\nProvide ONLY the SQL query without any explanation, markdown formatting, or code blocks. The query should be compatible with SQLite syntax."
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert SQL query generator. Only generate SELECT queries. Do NOT generate DELETE, UPDATE, INSERT, DROP, or other modifying statements."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            timeout=30.0,
        )
        sql = response.choices[0].message.content.strip()
        sql = re.sub(r'```sql\s*', '', sql)
        sql = re.sub(r'```\s*$', '', sql)
        return sql.strip(), ""
    except Exception as e:
        return "", f"Error generating SQL: {str(e)}"

def is_safe_sql_query(query: str) -> tuple[bool, str]:
    """Validate that a SQL query is safe to execute."""
    parsed = sqlparse.parse(query)
    if not parsed: return False, "Could not parse SQL query"
    for statement in parsed:
        if not statement.strip(): continue
        first_token = statement.token_first()
        if not first_token: return False, "Empty SQL statement"
        token_value = first_token.value.upper()
        if token_value != 'SELECT':
            return False, f"Only SELECT queries are allowed. Found: {token_value}"
        dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'EXEC', 'EXECUTE', 'CALL']
        query_upper = query.upper()
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False, f"Query contains dangerous keyword: {keyword}"
    return True, ""

def execute_query(engine, query: str) -> tuple[list, list, str]:
    """Execute SQL query and return results."""
    is_safe, error_msg = is_safe_sql_query(query)
    if not is_safe: return [], [], f"SQL Security Error: {error_msg}"
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

# UI
tab1, tab2 = st.tabs(["📁 Upload SQL Dump", "📝 Paste Schema"])
with tab1:
    uploaded_file = st.file_uploader("Upload your SQL schema file (.sql)", type=["sql"])
with tab2:
    schema_text = st.text_area("Paste your CREATE TABLE statements here:", height=200)

if uploaded_file is not None or schema_text.strip():
    sql_input = uploaded_file.getvalue().decode("utf-8") if uploaded_file else schema_text
    success, message = execute_schema_sql(engine, sql_input)
    if success:
        schema_info = get_schema_info(engine)
        st.success(f"✅ {message}")
        
        st.subheader("📋 Database Schema")
        for table_name, cols in schema_info.items():
            with st.expander(f"Table: {table_name}"):
                st.dataframe([{"Column": c["name"], "Type": c["type"]} for c in cols], hide_index=True)

        st.markdown("---")
        st.subheader("💬 Ask a Question")
        question = st.text_input("What would you like to query?", placeholder="e.g., Get all users")
        
        if st.button("🧠 Generate SQL", type="primary") and question:
            with st.spinner("Processing..."):
                schema_llm = schema_to_text(schema_info)
                sql_query, error = generate_sql_query(client, schema_llm, question)
                if error: st.error(error)
                else:
                    st.code(sql_query, language="sql")
                    rows, cols, ex_err = execute_query(engine, sql_query)
                    if ex_err: st.error(ex_err)
                    else:
                        if not rows: st.info("No results.")
                        else: st.dataframe([dict(zip(cols, r)) for r in rows])
else:
    st.info("👈 Upload a SQL file or paste your schema to get started!")

st.markdown("---")
st.markdown("Built by [@llrightll](https://github.com/llrightll) for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
