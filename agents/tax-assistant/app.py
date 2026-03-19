import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Tax Assistant", page_icon="💸")

st.title("💸 AI Tax Prep Assistant")
st.markdown("Simplified guidance for standard deductions and tax filing for freelancers/small biz.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    country = st.selectbox("Region", ["USA", "India", "UK", "Canada"])

income_source = st.text_area("Describe your income sources and business expenses:", height=250)

if st.button("Get Tax Guidance 🛡️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not income_source:
        st.warning("Please provide info.")
    else:
        with st.spinner(f"Consulting {country} tax codes..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["info", "region"],
                template="""
                You are a Tax Consultant for {region}. Analyze the following income/expense info.
                
                Provide:
                1. Top 3 Deductions: What can they likely write off?
                2. Filing Deadlines: Significant dates for this region.
                3. Warning: 2 common mistakes to avoid in {region}.
                4. Disclaimer: Remind them you are an AI and they should check with a CPA.

                Info: {info}
                """
            )
            
            response = llm.predict(prompt.format(info=income_source, region=country))
            
            st.success("Guidance Prepared!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
