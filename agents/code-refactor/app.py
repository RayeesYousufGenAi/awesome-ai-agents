import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Code Refactorer", page_icon="🛠️")

st.title("🛠️ AI Code Refactorer")
st.markdown("Clean up messy code, improve variable naming, and implement best practices.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    priority = st.selectbox("Priority", ["Readability", "Performance", "Security", "DRY Principle"])

code_input = st.text_area("Paste code here:", height=300)

if st.button("Refactor Code 🚀"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not code_input:
        st.warning("Please paste some code.")
    else:
        with st.spinner(f"Applying {priority} rules..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["code", "priority"],
                template="""
                You are a Senior Software Engineer. Refactor the following code with a focus on {priority}.
                
                Provide:
                1. Refactored Code block.
                2. Change Log: What did you improve?
                3. Logic Check: Did any behavior change?
                
                Code:
                {code}
                """
            )
            
            response = llm.predict(prompt.format(code=code_input, priority=priority))
            
            st.success("Code Refactored!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
