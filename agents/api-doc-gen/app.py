import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="API Documentation Bot", page_icon="📖")

st.title("📖 AI API Documentation Bot")
st.markdown("Turn your raw code into beautiful, clean Markdown documentation (Swagger/OpenAPI style).")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

raw_code = st.text_area("Paste your API code (FastAPI, Flask, Node, etc.) here:", height=300)

if st.button("Generate Documentation 📝"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not raw_code:
        st.warning("Please paste some code.")
    else:
        with st.spinner("Analyzing endpoints and models..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["code"],
                template="""
                You are a Technical Writer. Convert the following API code into structured Markdown documentation.
                Include:
                - Endpoint Path & Method
                - Description
                - Request Parameters (Body/Query)
                - Response Format (JSON)
                - Example Request/Response

                Code:
                {code}
                """
            )
            
            response = llm.predict(prompt.format(code=raw_code))
            
            st.success("Documentation Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
