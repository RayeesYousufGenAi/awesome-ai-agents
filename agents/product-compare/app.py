import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Product Compare", page_icon="⚖️")

st.title("⚖️ AI Product Comparison Helper")
st.markdown("Compare two products side-by-side to find the winner for your specific needs.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

col1, col2 = st.columns(2)
with col1:
    p1 = st.text_input("Product A:", placeholder="e.g. iPhone 15 Pro")
with col2:
    p2 = st.text_input("Product B:", placeholder="e.g. Samsung S24 Ultra")

use_case = st.text_input("My Primary Use Case (e.g. Photography, Gaming):")

if st.button("Battle of Specs ⚔️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not p1 or not p2:
        st.warning("Please provide both product names.")
    else:
        with st.spinner("Comparing features and benchmarks..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["p1", "p2", "use"],
                template="""
                You are a Tech Reviewer. Compare {p1} and {p2}.
                User's Priority: {use}
                
                Provide:
                1. Feature Showdown Table (Display, Battery, Camera, etc.).
                2. Pros/Cons for both.
                3. The Verdict: Which one should the user buy for '{use}'?
                """
            )
            
            response = llm.predict(prompt.format(p1=p1, p2=p2, use=use_case))
            
            st.success("Comparison Complete!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
