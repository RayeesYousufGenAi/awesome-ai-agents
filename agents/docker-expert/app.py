import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Docker Optimizer", page_icon="🐳")

st.title("🐳 Dockerfile Performance Optimizer")
st.markdown("Analyze your Dockerfiles for security risks, layer optimization, and build size.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

docker_content = st.text_area("Paste Dockerfile content here:", height=300)

if st.button("Optimize Dockerfile 🚀"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not docker_content:
        st.warning("Please paste a Dockerfile.")
    else:
        with st.spinner("Analyzing layers and security..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["dockerfile"],
                template="""
                You are a DevOps and Cloud Architect. Analyze the following Dockerfile.
                
                Provide:
                1. Optimized Version: Rewrite it using multi-stage builds or better layer management.
                2. Security Warnings: Identify root user usage, secrets exposure, or outdated base images.
                3. Size Savings: Estimate potential image size reduction.
                4. Best Practices: List 3 industry-standard tips for this specific stack.

                Dockerfile:
                {dockerfile}
                """
            )
            
            response = llm.predict(prompt.format(dockerfile=docker_content))
            
            st.success("Optimization Report Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
