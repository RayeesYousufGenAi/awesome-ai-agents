import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Patent Searcher", page_icon="📜")

st.title("📜 AI Patent Searcher")
st.markdown("Search for existing patents and check the novelty of your invention idea.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

idea = st.text_area("Describe your invention/idea in detail:", height=250)

if st.button("Search & Analyze Novelty 🔍"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not idea:
        st.warning("Please provide your idea.")
    else:
        with st.spinner("Searching repositories and analyzing novelty..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["idea"],
                template="""
                You are a Patent Attorney. Analyze the following invention idea.
                
                Provide:
                1. Concept Analysis: Breakdown of the core unique elements.
                2. Potential Prior Art: What already exists that might conflict?
                3. Novelty Score (1-10): How unique is this?
                4. Patentability Recommendation: Should they file a patent? What should they change to make it more unique?

                Idea:
                {idea}
                """
            )
            
            response = llm.predict(prompt.format(idea=idea))
            
            st.success("Analysis Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
