import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Release Notes Gen", page_icon="🆕")

st.title("🆕 AI Release Notes Generator")
st.markdown("Turn your Jira tickets or Git logs into beautiful, user-facing Release Notes.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

raw_logs = st.text_area("Paste Jira tickets, Git commits, or raw changelog info:", height=300)

if st.button("Generate Release Notes 📝"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not raw_logs:
        st.warning("Please provide logs.")
    else:
        with st.spinner("Refining for users..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["logs"],
                template="""
                You are a Product Marketer. Convert these raw technical logs into professional, 
                engaging Release Notes.
                
                Structure:
                1. Headlines: Catchy title for the update.
                2. 🚀 What's New: High-impact features described for users.
                3. 🐞 Bug Fixes: List of significant squashed bugs.
                4. ⚡ Performance: Technical improvements.
                5. Closing: Motivational end note.

                Logs: {logs}
                """
            )
            
            response = llm.predict(prompt.format(logs=raw_logs))
            
            st.success("Release Notes Produced!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
