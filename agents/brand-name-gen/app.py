import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Brand Name Generator", page_icon="🏷️")

st.title("🏷️ AI Brand Name Generator")
st.markdown("Generate catchy, meaningful names for your startup, product, or next big idea.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    industry = st.selectbox("Industry", ["Tech", "Fitness", "Food", "Fashion", "Finance", "Other"])
    vibe = st.select_slider("Brand Vibe", options=["Corporate", "Playful", "Minimalist", "Aggressive"])

description = st.text_area("What does your brand do?", placeholder="e.g. A high-end eco-friendly water bottle brand.")

if st.button("Generate Names 🚀"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not description:
        st.warning("Please provide a description.")
    else:
        with st.spinner("Brainstorming viral names..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["desc", "industry", "vibe"],
                template="""
                You are a world-class branding expert. Generate 10 unique brand names for a {industry} company.
                The vibe should be {vibe}. 
                
                For each name, provide:
                - Name
                - One-sentence tagline
                - Why it works (the psychology)
                
                Company Description:
                {desc}
                """
            )
            
            response = llm.predict(prompt.format(desc=description, industry=industry, vibe=vibe))
            
            st.success("Branding Ideas Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
