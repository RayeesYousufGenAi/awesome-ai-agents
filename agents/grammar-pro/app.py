import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Grammar Pro", page_icon="✍️")

st.title("✍️ AI Grammar & Tone Optimizer")
st.markdown("Beyond basic spellcheck. Adjust the vibe of your writing for any audience.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    vibe = st.selectbox("Desired Vibe", ["Professional", "Witty", "Direct", "Friendly", "Academic"])

text_input = st.text_area("Paste your text here:", height=300)

if st.button("Fix & Polish ✨"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not text_input:
        st.warning("Please paste some text.")
    else:
        with st.spinner(f"Polishing as {vibe}..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["text", "vibe"],
                template="""
                You are a Professional Editor. Polish the following text while keeping the meaning.
                Target Tone: {vibe}
                
                Provide:
                1. Corrected Version (Grammar + Flow).
                2. Key Changes: What did you fix?
                3. Tone Score: How well does it match '{vibe}' now?
                
                Text: {text}
                """
            )
            
            response = llm.predict(prompt.format(text=text_input, vibe=vibe))
            
            st.success("Polish Complete!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
