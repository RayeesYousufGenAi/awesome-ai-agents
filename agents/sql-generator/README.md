# 🗄️ AI SQL Query Generator

Convert natural language questions into SQL queries and execute them instantly. Upload your database schema, ask questions in plain English, and get accurate SQL queries with results.

## ✨ Features

- 📁 Upload database schema via SQL dump file
- 📝 Or paste schema directly as text input
- 💬 Natural language question input
- 🧠 GPT-4 powered SQL generation
- 🗄️ SQLAlchemy with SQLite in-memory execution
- 📊 Results displayed in table format with `st.dataframe()`
- ⚠️ Comprehensive error handling for invalid SQL

## 🛠️ Tech Stack

- **OpenAI GPT-4** — Natural language to SQL translation
- **SQLAlchemy** — Database engine and query execution
- **SQLite** — In-memory database for safe query testing
- **Streamlit** — Interactive web UI

## 🚀 Quick Start

### Install dependencies

```bash
cd agents/sql-generator
pip install -r requirements.txt
```

### Set up environment

```bash
export OPENAI_API_KEY="your-key-here"
```

Or create a `.env` file:

```
OPENAI_API_KEY=your-key-here
```

### Run the agent

```bash
streamlit run app.py
```

## 📝 How It Works

1. **Schema Upload**: Upload a SQL dump file or paste CREATE TABLE statements directly
2. **Schema Parsing**: The agent parses the SQL to understand table structures
3. **Query Generation**: Your natural language question is sent to GPT-4 with the schema context
4. **SQL Execution**: The generated SQL is executed safely in an in-memory SQLite database
5. **Results Display**: Query results are shown in a clean, formatted table

## 🎯 Example Usage

1. Upload a schema like:
   ```sql
   CREATE TABLE employees (
     id INTEGER PRIMARY KEY,
     name TEXT,
     department TEXT,
     salary INTEGER
   );
   ```

2. Ask: "Show me all employees in the Engineering department with salary above 50000"

3. Get the generated SQL and results instantly!

## 👤 Author

Rayees Yousuf — [@RayeesYousufGenAi](https://github.com/RayeesYousufGenAi)
