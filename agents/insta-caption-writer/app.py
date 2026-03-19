import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Insta Caption Writer", page_icon="📸")

st.title("📸 AI Instagram Caption Writer")
st.markdown("Generate high-engagement Instagram captions with hooks and hashtags.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    tone = st.selectbox("Tone", ["Fun", "Inspirational", "Educational", "Savage"])

image_desc = st.text_area("Describe your photo/video:", placeholder="e.g. A sunrise hike at the Grand Canyon.")

if st.button("Write Captions ✨"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not image_desc:
        st.warning("Please provide a description.")
    else:
        with st.spinner("Writing viral captions..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["desc", "tone"],
                template="""
                You are a social media manager. Write 3 different Instagram captions for this image.
                Tone: {tone}
                
                Each caption should include:
                - A strong hook
                - The body text
                - A Call to Action (CTA)
                - 10-15 relevant hashtags
                
                Image Description: {desc}
                """
            )
            
            response = llm.predict(prompt.format(desc=image_desc, tone=tone))
            
            st.success("Captions Generated!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
