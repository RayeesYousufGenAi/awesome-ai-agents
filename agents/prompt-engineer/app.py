import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Prompt Engineer", page_icon="🎨")

st.title("🎨 AI Art Prompt Engineer")
st.markdown("Transform your basic ideas into high-detail prompts for Midjourney, DALL-E, or Stable Diffusion.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    engine = st.selectbox("Target Engine", ["Midjourney", "DALL-E 3", "Stable Diffusion"])

basic_idea = st.text_input("What do you want to see?", placeholder="e.g. A cat in space.")

if st.button("Engineer Prompt ✨"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not basic_idea:
        st.warning("Please provide an idea.")
    else:
        with st.spinner(f"Polishing your {engine} prompt..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["idea", "engine"],
                template="""
                You are a Prompt Engineering expert for Generative AI Art.
                Expand the following basic idea into a highly descriptive prompt for {engine}.
                
                Include:
                - Lighting (e.g. volumetric, cinematic)
                - Style (e.g. cyberpunk, oil painting, photorealistic)
                - Camera settings (e.g. 85mm lens, f/1.8)
                - Aspect Ratio suggestions
                - Negative prompts (if applicable)
                
                Idea: {idea}
                """
            )
            
            response = llm.predict(prompt.format(idea=basic_idea, engine=engine))
            
            st.success("Prompt Engineered!")
            st.code(response, language="markdown")

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
