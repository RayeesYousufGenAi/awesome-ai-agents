import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Expense Categorizer", page_icon="💸")

st.title("💸 AI Expense Categorizer")
st.markdown("Paste your transaction logs or bank statements to categorize spending automatically.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

data = st.text_area("Paste transactions here (Date, Shop, Amount):", height=250)

if st.button("Categorize 🧾"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not data:
        st.warning("Please paste some data.")
    else:
        with st.spinner("Analyzing ledger..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["data"],
                template="""
                You are a personal finance expert. Categorize the following transactions into 
                standard groups (Food, Rent, Entertainment, Subscriptions, Utilities, etc.).
                
                Provide:
                1. A breakdown by category (Total spent in each).
                2. A list of all transactions with their assigned category.
                3. 2 tips on where I can save money based on these patterns.

                Data:
                {data}
                """
            )
            
            response = llm.predict(prompt.format(data=data))
            
            st.success("Analysis Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
