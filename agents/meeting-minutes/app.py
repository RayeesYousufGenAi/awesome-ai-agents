import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Meeting Summarizer", page_icon="📝")

st.title("📝 Meeting Minutes Summarizer")
st.markdown("Paste your meeting transcript to get professional summaries and clear action items.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    detail_level = st.radio("Detail Level", ["Concise", "Detailed", "Executive"])

transcript = st.text_area("Paste Transcript here:", height=300)

if st.button("Summarize 🚀"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not transcript:
        st.warning("Please paste a transcript.")
    else:
        with st.spinner("Processing meeting data..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["transcript", "level"],
                template="""
                You are a professional executive assistant. Summarize the following meeting transcript.
                Level of detail: {level}

                Requirements:
                1. Executive Summary: 2-3 sentences max.
                2. Key Discussion Points: Bullet points of major topics.
                3. Action Items: Clear list of WHO needs to do WHAT.
                4. Decided Outcomes: What was finalized during the meeting.

                Transcript:
                {transcript}
                """
            )
            
            response = llm.predict(prompt.format(transcript=transcript, level=detail_level))
            
            st.success("Summary Generated!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
