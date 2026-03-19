# 🗄️ AI SQL Query Generator

Convert natural language questions into valid SQL queries and execute them against your own database schema.

## 🚀 Features
- **Schema Upload**: Supports `.sql` dump files or direct pasting of `CREATE TABLE` statements.
- **Natural Language to SQL**: Uses GPT-4 to translate English questions into precision SQL.
- **In-Memory Sandbox**: Executes queries safely in a temporary SQLite environment.
- **Security First**: 
  - **Read-Only**: Strictly enforces `SELECT` statements only.
  - **SQL Injection Guard**: Uses `sqlparse` for AST-based validation.
  - **Prompt Injection Filter**: Detects and blocks malicious prompt engineering attempts.

## 🛠️ Tech Stack
- LangChain / OpenAI GPT-4
- SQLAlchemy (In-memory SQLite)
- sqlparse
- Streamlit

## 🚀 Quick Start
```bash
pip install -r requirements.txt
streamlit run app.py
```

---
Contributed by [@llrightll](https://github.com/llrightll)
