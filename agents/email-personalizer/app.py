import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Cold Email Personalizer", page_icon="📧")

st.title("📧 Cold Email Personalizer")
st.markdown("Generate hyper-personalized outreach emails by analyzing a prospect's bio or company description.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    tone = st.selectbox("Tone", ["Professional", "Witty", "Direct", "Friendly"])

prospect_info = st.text_area("Prospect Info (Paste Bio/LinkedIn About/Company Page):", height=200)
your_offer = st.text_input("Your Product/Service/Goal:", placeholder="e.g. Free SEO Audit")

if st.button("Generate Personalized Email ✉️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not prospect_info:
        st.warning("Please provide prospect info.")
    else:
        with st.spinner("Personalizing..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["bio", "offer", "tone"],
                template="""
                You are a world-class sales copywriter. Write a cold email that feels personal and non-spammy.
                Analyze the prospect's info and find a unique 'hook' to start the email.

                Prospect Info: {bio}
                My Offer: {offer}
                Tone: {tone}

                Structure:
                - Subject Line
                - Personalized Hook (based on their info)
                - Bridge (link the hook to my offer)
                - The Value/Offer
                - Low-friction CTA
                """
            )
            
            response = llm.predict(prompt.format(bio=prospect_info, offer=your_offer, tone=tone))
            
            st.success("Email Generated!")
            st.code(response, language="markdown")

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) hub.")
