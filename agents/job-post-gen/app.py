import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Job Post Gen", page_icon="💼")

st.title("💼 AI Job Post Generator")
st.markdown("Generate engaging, inclusive, and professional job descriptions in seconds.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

title = st.text_input("Job Title:", placeholder="e.g. Senior Full Stack Engineer")
company_vibe = st.text_input("Company Culture:", placeholder="e.g. Fast-paced startup, work-life balance focus")
key_reqs = st.text_area("Key Requirements (bullet points):", height=150)

if st.button("Draft Job Post ✍️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not title:
        st.warning("Please provide a title.")
    else:
        with st.spinner("Writing job post..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["title", "vibe", "reqs"],
                template="""
                You are an HR Specialist. Write a compelling job post for {title}.
                Culture: {vibe}
                
                Include:
                1. Role Summary (The Hook).
                2. Key Responsibilities.
                3. Required Skills: {reqs}
                4. Why Join Us (Perks/Culture).
                5. Call to Action.
                """
            )
            
            response = llm.predict(prompt.format(title=title, vibe=company_vibe, reqs=key_reqs))
            
            st.success("Job Post Drafted!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
