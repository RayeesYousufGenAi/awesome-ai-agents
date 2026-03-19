import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Cold Call Script", page_icon="📞")

st.title("📞 AI Cold Call Script Writer")
st.markdown("Write non-cringe sales scripts that actually work. Optimized for high conversion.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

product = st.text_input("What are you selling?", placeholder="e.g. AI automation for real estate")
prospect = st.text_input("Who is the prospect?", placeholder="e.g. Busy real estate broker")

if st.button("Generate Script ☎️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not product:
        st.warning("Please provide product info.")
    else:
        with st.spinner("Designing the conversation..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["prod", "who"],
                template="""
                You are a Sales Coach. Write a cold call script for {prod} targeting {who}.
                
                Structure:
                1. Permission-based Open (The 15-second hook).
                2. The "Wait, what?" moment (Interrupt their pattern).
                3. Discovery: 2 power questions.
                4. The Close: Low friction meeting request.
                5. Objection Handling: What to say for "I'm too busy" and "Send me an email".
                """
            )
            
            response = llm.predict(prompt.format(prod=product, who=prospect))
            
            st.success("Script Finished!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
