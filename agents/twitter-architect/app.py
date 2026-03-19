import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Twitter Thread Architect", page_icon="🐦")

st.title("🐦 Twitter/X Thread Architect")
st.markdown("Convert any article, link, or long text into an engaging, viral Twitter thread.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    thread_length = st.slider("Thread Length (Tweets)", 3, 12, 6)
    style = st.selectbox("Style", ["Educational", "Controversial", "Storytelling", "Actionable"])

input_text = st.text_area("Paste your content here:", height=300)

if st.button("Architect Thread 🏗️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not input_text:
        st.warning("Please paste some content.")
    else:
        with st.spinner("Batching your tweets..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["text", "length", "style"],
                template="""
                You are a viral Twitter ghostwriter. Convert the following content into a thread of {length} tweets.
                
                Style: {style}
                
                Rules:
                - Tweet 1 must be a strong hook.
                - Use line breaks for readability.
                - Use relevant emojis but don't overdo it.
                - Each tweet should be under 280 characters.
                - Tweet {length} should have a CTA or a 'Follow for more' closure.
                - Keep the numbering (1/n, 2/n).

                Content:
                {text}
                """
            )
            
            response = llm.predict(prompt.format(text=input_text, length=thread_length, style=style))
            
            st.success("Thread Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
