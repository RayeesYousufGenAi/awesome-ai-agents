import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Stack Recommender", page_icon="💻")

st.title("💻 AI Tech Stack Recommender")
st.markdown("Describe your project, and get a modern, scalable tech stack recommendation.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

idea = st.text_area("Describe your project (e.g. Real-time chat app for gamers):", height=200)

if st.button("Build My Stack 🛠️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not idea:
        st.warning("Please provide an idea.")
    else:
        with st.spinner("Analyzing requirements..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["idea"],
                template="""
                You are a CTO. Recommend a modern tech stack for: {idea}.
                
                Provide:
                1. Frontend (Framework + Styling).
                2. Backend (Language + Framework).
                3. Database (Choose based on data structure).
                4. Infrastructure (Hosting + CI/CD).
                5. Why: Justification for these choices.
                """
            )
            
            response = llm.predict(prompt.format(idea=idea))
            
            st.success("Stack Recommendation Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
