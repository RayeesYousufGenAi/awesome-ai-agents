import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Vibe Recommender", page_icon="📚")

st.title("🎬 Niche Movie & Book Recommender")
st.markdown("Get hyper-specific recommendations based on your current 'vibe' or mood, not just genres.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    media_type = st.radio("I'm looking for:", ["Movies", "Books", "Both"])

vibe = st.text_input("What's your vibe today?", placeholder="e.g. Rainy day in London, feeling melancholic but hopeful.")

if st.button("Find My Match 🔍"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not vibe:
        st.warning("Please describe your vibe.")
    else:
        with st.spinner("Scanning the library..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["vibe", "type"],
                template="""
                You are a cultural curator. Recommend 3 {type} that perfectly match the following 'vibe'.
                Avoid extremely popular/obvious choices unless they are perfect. 
                
                Vibe: {vibe}
                
                For each recommendation, provide:
                - Title
                - Why it matches the vibe
                - One 'Fun Fact' or piece of trivia.
                """
            )
            
            response = llm.predict(prompt.format(vibe=vibe, type=media_type))
            
            st.success("Curation Complete!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
