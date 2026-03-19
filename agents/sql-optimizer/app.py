import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="SQL Optimizer", page_icon="🗄️")

st.title("🗄️ AI SQL Query Optimizer")
st.markdown("Analyze your SQL queries for bottlenecks, missing indices, and performance issues.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    db_type = st.selectbox("Database", ["PostgreSQL", "MySQL", "SQLite", "MongoDB (NoSQL)"])

sql_query = st.text_area("Paste your SQL query here:", height=300)

if st.button("Optimize Query 🚀"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not sql_query:
        st.warning("Please paste a query.")
    else:
        with st.spinner("Analyzing execution plan..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["query", "db"],
                template="""
                You are a Senior Database Administrator (DBA). Analyze the following {db} query.
                
                Provide:
                1. Optimized Query: Rewrite the query for better performance.
                2. Indices Needed: Suggest which columns to index.
                3. Bottlenecks: Identify N+1 issues, full table scans, or bad joins.
                4. Explanation: Why is the new version better?

                Query: {query}
                """
            )
            
            response = llm.predict(prompt.format(query=sql_query, db=db_type))
            
            st.success("Performance Audit Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
