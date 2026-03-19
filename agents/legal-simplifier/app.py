import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Legal jargon Simplifier", page_icon="⚖️")

st.title("⚖️ Legal jargon Simplifier")
st.markdown("Paste complex Terms of Service or Legal Contracts to get a plain-English summary.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

legal_text = st.text_area("Paste Legal Text/Section here:", height=300)

if st.button("Simplify 🪄"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not legal_text:
        st.warning("Please paste some text.")
    else:
        with st.spinner("Decoding legalese..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["text"],
                template="""
                You are a consumer advocate and lawyer. Explain the following legal text in plain English 
                so a 10-year-old can understand it. 

                Text:
                {text}

                Highlight:
                - What am I giving up?
                - What am I getting?
                - Any 'Hidden' red flags or risks.
                """
            )
            
            response = llm.predict(prompt.format(text=legal_text))
            
            st.success("Simplified!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) hub.")
