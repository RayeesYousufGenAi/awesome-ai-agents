import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Architecture Diagrammer", page_icon="🏗️")

st.title("🏗️ AI Code-to-Architecture Diagram")
st.markdown("Generate Mermaid.js diagrams automatically from your code or system descriptions.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

input_text = st.text_area("Paste code or system components here:", height=300)

if st.button("Generate Diagram 🖼️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not input_text:
        st.warning("Please paste some content.")
    else:
        with st.spinner("Mapping components..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["text"],
                template="""
                You are a Software Architect. Convert the following description or code into a 
                Mermaid.js Flowchart or Sequence Diagram.
                
                Rules:
                - Use clear node names.
                - Use subgraphs for grouping (e.g. Frontend, Backend, DB).
                - ONLY return the Mermaid code block.

                Input:
                {text}
                """
            )
            
            response = llm.predict(prompt.format(text=input_text))
            
            st.success("Diagram Generated!")
            st.code(response, language="mermaid")
            
            st.info("💡 Copy the code above and paste it into [Mermaid Live Editor](https://mermaid.live/) to export as SVG/PNG.")

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
