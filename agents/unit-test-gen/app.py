import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Unit Test Generator", page_icon="🧪")

st.title("🧪 AI Unit Test Generator")
st.markdown("Instantly generate `pytest` or `unittest` suites for your Python code.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    framework = st.selectbox("Testing Framework", ["Pytest", "Unittest"])
    coverage = st.slider("Target Coverage (%)", 80, 100, 95)

code_input = st.text_area("Paste your Python code/function here:", height=300)

if st.button("Generate Tests 🛠️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not code_input:
        st.warning("Please paste some code.")
    else:
        with st.spinner("Generating test suite..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["code", "framework", "coverage"],
                template="""
                You are a Senior QA Engineer. Write a comprehensive test suite using {framework} for the following code.
                Ensure:
                - High edge-case coverage.
                - Mocking of external dependencies if any.
                - Clear test names and comments.
                - Target {coverage}% coverage.

                Code:
                {code}
                """
            )
            
            response = llm.predict(prompt.format(code=code_input, framework=framework, coverage=coverage))
            
            st.success("Test Suite Generated!")
            st.code(response, language="python")

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) hub.")
