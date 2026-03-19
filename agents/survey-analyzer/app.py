import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Survey Analyzer", page_icon="📊")

st.title("📊 AI Survey & Feedback Analyzer")
st.markdown("Extract themes, sentiment, and actionable insights from raw survey feedback.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

raw_feedback = st.text_area("Paste survey results (CSV or Text) here:", height=300)

if st.button("Extract Insights 💡"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not raw_feedback:
        st.warning("Please paste some feedback.")
    else:
        with st.spinner("Analyzing sentiment and themes..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["feedback"],
                template="""
                You are a Data Analyst. Analyze the following survey feedback.
                
                Provide:
                1. Sentiment Heatmap: Overall % Positive/Negative/Neutral.
                2. Top 3 Recurring Themes: What are people saying most?
                3. Core Complaints: What needs to be fixed immediately?
                4. Actionable Recommendation: One big thing the company should do.

                Feedback:
                {feedback}
                """
            )
            
            response = llm.predict(prompt.format(feedback=raw_feedback))
            
            st.success("Analysis Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
