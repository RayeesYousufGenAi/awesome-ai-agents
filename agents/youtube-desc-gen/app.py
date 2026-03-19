import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="YouTube Description Gen", page_icon="🎬")

st.title("🎬 AI YouTube Description Generator")
st.markdown("Generate SEO-optimized descriptions, timestamps, and tags for your videos.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

video_topic = st.text_input("Video Title/Topic:", placeholder="e.g. How to grow your AI startup in 2026")
key_points = st.text_area("Bullet points of what happens in the video:", height=150)

if st.button("Generate Description 🚀"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not video_topic:
        st.warning("Please provide a topic.")
    else:
        with st.spinner("Writing metadata..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["topic", "points"],
                template="""
                You are a YouTube SEO expert. Write an engaging description for a video about {topic}.
                
                Include:
                - Hook (First 2 lines).
                - Summary of the video.
                - Chapters/Timestamps (Guess based on points).
                - 10 High-Volume Tags.
                - Call to Action (Like/Subscribe).
                
                Video Info: {points}
                """
            )
            
            response = llm.predict(prompt.format(topic=video_topic, points=key_points))
            
            st.success("Metadata Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
