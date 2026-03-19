import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Content Calendar", page_icon="📅")

st.title("📅 AI Video Content Calendar")
st.markdown("Generate a 30-day content strategy for YouTube, TikTok, or Instagram.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    niche = st.text_input("Niche (e.g. Finance, Tech, Cooking):")
    platform = st.multiselect("Platforms", ["YouTube Shorts", "TikTok", "Instagram Reels", "Long-form YouTube"])

if st.button("Generate Strategy 🚀"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not niche:
        st.warning("Please specify your niche.")
    else:
        with st.spinner("Brainstorming viral topics..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["niche", "platforms"],
                template="""
                You are a Social Media Strategist. Generate a 30-day content calendar for the {niche} niche.
                Target Platforms: {platforms}
                
                Provide:
                1. Weekly Themes.
                2. Daily Hook Ideas for 30 days.
                3. Best Posting Times for this niche.
                4. One 'Viral Format' suggestion.
                """
            )
            
            response = llm.predict(prompt.format(niche=niche, platforms=", ".join(platform)))
            
            st.success("Calendar Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
