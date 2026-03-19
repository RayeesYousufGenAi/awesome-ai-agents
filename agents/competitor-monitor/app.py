import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Competitor Monitor", page_icon="📡")

st.title("📡 Competitive Intelligence Bot")
st.markdown("Analyze competitor strategies, pricing, and messaging to stay ahead.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

competitor_info = st.text_area("Paste Competitor Landing Page Text/News:", height=300)

if st.button("Analyze Strategy 🕵️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not competitor_info:
        st.warning("Please provide info.")
    else:
        with st.spinner("Decoding their moves..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["info"],
                template="""
                You are a Strategic Business Analyst. Analyze the following competitor information.
                
                Provide:
                1. Value Proposition: What is their core promise?
                2. Target Audience: Who are they chasing?
                3. Strategic Moat: What is their competitive advantage?
                4. Weakness/Gap: Where are they vulnerable?
                5. Counter-Move: How should we respond to their positioning?

                Competitor Info:
                {info}
                """
            )
            
            response = llm.predict(prompt.format(info=competitor_info))
            
            st.success("Strategy Report Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
