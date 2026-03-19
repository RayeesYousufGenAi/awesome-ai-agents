import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Invoice Generator", page_icon="🧾")

st.title("🧾 AI Self-Employed Invoice Generator")
st.markdown("Turn your work logs or unstructured text into a professional PDF-ready invoice structure.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

work_log = st.text_area("Paste your work logs/hours (e.g. 5 hours coding, 2 hours meetings):", height=250)
rate = st.number_input("Hourly Rate ($)", value=50.0)

if st.button("Generate Invoice Structure 🛠️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not work_log:
        st.warning("Please provide work logs.")
    else:
        with st.spinner("Calculating and formatting..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["log", "rate"],
                template="""
                You are a professional accountant. Convert the following work log into a clear 
                invoice-style table.
                
                Work Log: {log}
                Hourly Rate: ${rate}
                
                Provide:
                1. Itemized Table (Task, Duration, Cost).
                2. Subtotal, Tax (10% estimate), and Grand Total.
                3. Footer Notes: (e.g. Payment terms Net 30).
                """
            )
            
            response = llm.predict(prompt.format(log=work_log, rate=rate))
            
            st.success("Invoice Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
