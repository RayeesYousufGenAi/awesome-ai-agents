import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Lyrics Writer", page_icon="🎵")

st.title("🎵 AI Lyrics & Songwriter")
st.markdown("Generate full song lyrics based on genre, mood, and story.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    genre = st.selectbox("Genre", ["Pop", "Rap", "Rock", "Country", "Jazz", "Metal"])
    mood = st.selectbox("Mood", ["Happy", "Heartbroken", "Angry", "Pensive", "Hype"])

topic = st.text_input("What is the song about?", placeholder="e.g. Life in a busy city.")

if st.button("Write Song 🎸"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not topic:
        st.warning("Please provide a topic.")
    else:
        with st.spinner(f"Writing your {genre} hit..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["topic", "genre", "mood"],
                template="""
                You are a professional songwriter. Write a {genre} song about {topic}.
                The mood should be {mood}.
                
                Structure:
                - Intro
                - Verse 1
                - Chorus
                - Verse 2
                - Chorus
                - Bridge
                - Outro
                
                Include stage directions (e.g. [Beat drops], [Slow piano melody]).
                """
            )
            
            response = llm.predict(prompt.format(topic=topic, genre=genre, mood=mood))
            
            st.success("Song Finished!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
