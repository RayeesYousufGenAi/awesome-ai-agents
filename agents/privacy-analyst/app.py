import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Privacy Policy Analyst", page_icon="🔐")

st.title("🔐 AI Privacy Policy Analyst")
st.markdown("Check what data is being tracked and how it's used. Get a 'Privacy Grade' instantly.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

policy_text = st.text_area("Paste Privacy Policy here:", height=300)

if st.button("Audit Policy 🔍"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not policy_text:
        st.warning("Please paste some text.")
    else:
        with st.spinner("Analyzing data tracking clauses..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["text"],
                template="""
                You are a Data Privacy Expert. Analyze the following privacy policy.
                
                Provide:
                1. Data Tracked: List specific personal info they collect.
                2. Third-Party Sharing: Do they sell data? To whom?
                3. Privacy Grade: (A to F based on user-friendliness).
                4. One Major Warning: The most intrusive part of this policy.

                Policy: {text}
                """
            )
            
            response = llm.predict(prompt.format(text=policy_text))
            
            st.success("Audit Complete!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
