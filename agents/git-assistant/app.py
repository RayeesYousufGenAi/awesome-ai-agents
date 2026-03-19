import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Git Commit Assistant", page_icon="🎋")

st.title("🎋 AI Git Commit Assistant")
st.markdown("Paste your `git diff` to get meaningful, industry-standard commit messages.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    conv_commits = st.checkbox("Standard Conventional Commits", value=True)

diff_text = st.text_area("Paste Git Diff output here:", height=300)

if st.button("Generate Commit Message 📝"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not diff_text:
        st.warning("Please paste a diff.")
    else:
        with st.spinner("Analyzing changes..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            conv_instruct = "Use Conventional Commits format (feat, fix, docs, etc.)" if conv_commits else ""
            
            prompt = PromptTemplate(
                input_variables=["diff", "format"],
                template="""
                You are a Senior Developer. Based on the following git diff, write 3 possible commit messages.
                {format}
                
                Diff:
                {diff}
                """
            )
            
            response = llm.predict(prompt.format(diff=diff_text, format=conv_instruct))
            
            st.success("Commit Messages Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
