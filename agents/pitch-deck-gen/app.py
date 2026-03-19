import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Pitch Deck Gen", page_icon="🚀")

st.title("🚀 AI Startup Pitch Deck Gen")
st.markdown("Generate a winner's pitch deck outline for your startup to impress VCs.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

idea = st.text_area("Your Startup Idea/Mission:", height=200)
business_model = st.text_input("How will you make money?")

if st.button("Generate Deck Outline 📊"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not idea:
        st.warning("Please provide your idea.")
    else:
        with st.spinner("Architecting the pitch..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["idea", "model"],
                template="""
                You are a Venture Capitalist (VC). Create a 10-slide pitch deck outline for this startup.
                Idea: {idea}
                Business Model: {model}
                
                Slides required:
                1. The Vision
                2. The Problem
                3. The Solution
                4. Market Size (TAM/SAM/SOM)
                5. Product Showcase
                6. Business Model
                7. Traction/Roadmap
                8. Competition
                9. Team
                10. The Ask
                
                Provide a 2-3 sentence description of WHAT to say on each slide.
                """
            )
            
            response = llm.predict(prompt.format(idea=idea, model=business_model))
            
            st.success("Pitch Deck Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
