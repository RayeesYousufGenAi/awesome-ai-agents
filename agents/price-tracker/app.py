import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Price Monitor", page_icon="🏷️")

st.title("🏷️ Smart Price Alert Analyst")
st.markdown("Analyze product details and price history to determine if it's the right time to buy.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

product_url = st.text_input("Product URL or Name:", placeholder="e.g. Sony WH-1000XM5")
current_price = st.number_input("Current Price ($)", min_value=0.0, value=350.0)

if st.button("Evaluate Deal 📊"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not product_url:
        st.warning("Please provide product info.")
    else:
        with st.spinner("Analyzing market trends..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["product", "price"],
                template="""
                You are a shopping expert. Analyze if {price} is a good deal for {product}.
                
                Provide:
                1. Expected Price Range: (Highs and Lows for this category).
                2. Seasonal Timing: Is a sale coming up (Black Friday, Prime Day)?
                3. Verdict: Buy Now / Wait / Look for Alternatives.
                4. Why: Justification based on product lifecycle.

                Product: {product}
                Price: ${price}
                """
            )
            
            response = llm.predict(prompt.format(product=product_url, price=current_price))
            
            st.success("Analysis Complete!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
