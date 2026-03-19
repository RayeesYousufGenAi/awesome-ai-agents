import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Standup Gen", page_icon="🌤️")

st.title("🌤️ AI Daily Standup Generator")
st.markdown("Convert your disorganized daily notes into a professional Standup update.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

notes = st.text_area("What did you do today? (Raw notes, bullet points):", height=250)

if st.button("Generate Standup 📢"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not notes:
        st.warning("Please provide notes.")
    else:
        with st.spinner("Structuring update..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["notes"],
                template="""
                You are a Team Lead. Format the following notes into a 'Daily Standup' update.
                
                Structure:
                1. Yesterday: What I accomplished.
                2. Today: What I'm working on.
                3. Blockers: Any risks or issues.
                
                Make it look professional for Slack/Teams.
                Notes: {notes}
                """
            )
            
            response = llm.predict(prompt.format(notes=notes))
            
            st.success("Standup Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
