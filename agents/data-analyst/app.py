"""
AI Data Analyst — Upload CSV and get AI-powered data analysis.
Generates summaries, visualizations, and insights using GPT-4.
Author: Rayees Yousuf (@RayeesYousufGenAi)
"""

import os
import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="📊 AI Data Analyst", page_icon="📊", layout="wide")
st.title("📊 AI Data Analyst")
st.caption("Upload a CSV and get instant AI-powered insights, summaries, and analysis")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# File upload
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Show data preview
    st.subheader("📋 Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", f"{len(df):,}")
    col2.metric("Columns", len(df.columns))
    col3.metric("Missing Values", df.isnull().sum().sum())

    # Generate data context
    data_context = f"""
Dataset Info:
- Shape: {df.shape}
- Columns: {list(df.columns)}
- Data Types: {df.dtypes.to_dict()}
- Sample Data (first 5 rows): {df.head().to_string()}
- Basic Stats: {df.describe().to_string()}
- Missing Values: {df.isnull().sum().to_dict()}
"""

    # Analysis options
    st.subheader("🔍 Ask Questions About Your Data")

    analysis_type = st.selectbox(
        "Quick Analysis:",
        [
            "Custom question...",
            "Give me a comprehensive summary of this dataset",
            "What are the key trends and patterns?",
            "Identify outliers and anomalies",
            "What insights can help business decisions?",
            "Suggest further analysis or visualizations",
        ],
    )

    if analysis_type == "Custom question...":
        question = st.text_input("💬 Your question:")
    else:
        question = analysis_type

    if st.button("🧠 Analyze", type="primary") and question:
        with st.spinner("Analyzing your data..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert data analyst. Analyze the given dataset and provide "
                            "clear, actionable insights. Use markdown formatting with headers, "
                            "bullet points, and tables where appropriate. Be specific with numbers."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Dataset:\n{data_context}\n\nQuestion: {question}",
                    },
                ],
                temperature=0.3,
            )

        st.markdown("---")
        st.markdown("### 📊 Analysis Results")
        st.markdown(response.choices[0].message.content)

    # Basic visualizations
    st.subheader("📈 Quick Visualizations")

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if numeric_cols:
        selected_col = st.selectbox("Select a numeric column to visualize:", numeric_cols)
        chart_type = st.radio("Chart type:", ["Bar", "Line", "Area"], horizontal=True)

        if chart_type == "Bar":
            st.bar_chart(df[selected_col])
        elif chart_type == "Line":
            st.line_chart(df[selected_col])
        else:
            st.area_chart(df[selected_col])
else:
    st.info("👈 Upload a CSV file to get started!")
