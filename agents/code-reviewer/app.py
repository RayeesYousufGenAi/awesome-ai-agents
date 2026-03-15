"""
AI Code Reviewer — Paste code and get AI-powered code review.
Provides bug detection, optimization tips, and best practices.
Author: Rayees Yousuf (@RayeesYousufGenAi)
"""

import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="🔍 AI Code Reviewer", page_icon="🔍", layout="wide")
st.title("🔍 AI Code Reviewer")
st.caption("Paste your code and get instant AI-powered review — bugs, optimizations, and best practices")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are an expert code reviewer. When given code, provide a thorough review that includes:

1. **🐛 Bugs & Issues**: Identify any bugs, errors, or potential runtime issues
2. **⚡ Performance**: Suggest performance optimizations
3. **🔒 Security**: Flag any security vulnerabilities
4. **📖 Readability**: Suggest improvements for code clarity
5. **✅ Best Practices**: Recommend industry best practices
6. **📊 Rating**: Give an overall code quality score (1-10)

Format your response with clear headers and use markdown. Be constructive and specific.
For each issue found, show the problematic code and the suggested fix."""

# Language selector
language = st.selectbox(
    "Select language:",
    ["Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust", "Other"],
    index=0,
)

# Code input
code = st.text_area(
    "📝 Paste your code here:",
    height=300,
    placeholder="# Paste your code here...\ndef example():\n    pass",
)

col1, col2 = st.columns([1, 5])
with col1:
    review_btn = st.button("🔍 Review Code", type="primary", use_container_width=True)

if review_btn and code:
    with st.spinner("🧠 Analyzing your code..."):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Review this {language} code:\n\n```{language.lower()}\n{code}\n```"},
            ],
            temperature=0.3,
        )

    st.markdown("---")
    st.markdown("## 📋 Code Review Results")
    st.markdown(response.choices[0].message.content)

elif review_btn:
    st.warning("Please paste some code to review!")
