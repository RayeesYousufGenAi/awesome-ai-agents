import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Contract Compare", page_icon="📜")

st.title("📜 AI Contract Comparison Bot")
st.markdown("Compare two versions of a contract and instantly highlight changes in rights or obligations.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

col1, col2 = st.columns(2)
with col1:
    v1 = st.text_area("Original Contract (v1):", height=300)
with col2:
    v2 = st.text_area("New Version (v2):", height=300)

if st.button("Analyze Changes 🔍"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not v1 or not v2:
        st.warning("Please paste both versions.")
    else:
        with st.spinner("Diffing legal clauses..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["v1", "v2"],
                template="""
                You are a Paralegal. Compare the following two versions of a contract.
                
                Provide:
                1. Significant Changes: List any clauses modified.
                2. Risk Shifts: Does 'v2' shift more risk to us?
                3. Better/Worse: Is this a better deal than the original?
                
                v1: {v1}
                v2: {v2}
                """
            )
            
            response = llm.predict(prompt.format(v1=v1, v2=v2))
            
            st.success("Comparison Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
