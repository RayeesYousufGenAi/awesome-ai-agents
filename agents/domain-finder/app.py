import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Domain Finder", page_icon="🌎")

st.title("🌎 AI Domain & Startup Namer")
st.markdown("Brainstorm short, catchy domains and check their 'tech vibe' for your project.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    tld = st.selectbox("Preferred TLD", [".com", ".ai", ".io", ".xyz"])

idea = st.text_input("Project Description:", placeholder="e.g. AI that writes children's books.")

if st.button("Find Domains 🔍"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not idea:
        st.warning("Please provide an idea.")
    else:
        with st.spinner("Searching for available-ish gems..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["idea", "tld"],
                template="""
                You are a Domain Investing expert. Brainstorm 10 creative domain names for: {idea}.
                Primary extension: {tld}
                
                Rules:
                - Keep them under 10 characters if possible.
                - No hyphens.
                - Easy to pronounce.
                - Provide: [Domain] - [Brand Vibe]
                """
            )
            
            response = llm.predict(prompt.format(idea=idea, tld=tld))
            
            st.success("Domain Ideas Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
