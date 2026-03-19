import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Plant Doctor", page_icon="🪴")

st.title("🪴 AI House Plant Doctor")
st.markdown("Diagnose what's wrong with your plants based on symptoms and get a recovery plan.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

plant_name = st.text_input("Plant Name (e.g. Monstera, Snake Plant):")
symptoms = st.text_area("What's happening? (e.g. Yellow leaves, spots, drooping):", height=200)

if st.button("Diagnose 🩺"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not symptoms:
        st.warning("Please describe the symptoms.")
    else:
        with st.spinner("Consulting the botanist..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["name", "symptoms"],
                template="""
                You are an expert Botanists. Diagnose the issue for the following plant.
                
                Plant: {name}
                Symptoms: {symptoms}
                
                Provide:
                1. Most Likely Cause: (Overwatering, light deficiency, pests, etc.)
                2. Immediate Action: What should I do right now?
                3. Recovery Plan: Next 2 weeks schedule.
                4. Pro-Tip: A specific care secret for this species.
                """
            )
            
            response = llm.predict(prompt.format(name=plant_name, symptoms=symptoms))
            
            st.success("Diagnosis Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
