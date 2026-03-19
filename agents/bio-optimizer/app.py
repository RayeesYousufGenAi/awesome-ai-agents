import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Social Bio Optimizer", page_icon="👤")

st.title("👤 Social Media Bio Optimizer")
st.markdown("Turn your boring bio into a professional, high-conversion 'landing page' for your profile.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    platform = st.selectbox("Platform", ["Twitter/X", "LinkedIn", "Instagram", "GitHub"])

current_bio = st.text_area("Your current bio or achievements:", height=150)

if st.button("Optimize Bio ✨"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not current_bio:
        st.warning("Please provide info.")
    else:
        with st.spinner(f"Polishing your {platform} profile..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["bio", "platform"],
                template="""
                You are a Personal Branding expert. Rewrite the following bio for {platform}.
                
                Rules:
                - Use the appropriate character limit.
                - Include a 'Who', 'What', and 'Proof' (Achievements).
                - Use professional/relevant emojis.
                - Include 1 clear Call to Action.
                
                Original Info: {bio}
                """
            )
            
            response = llm.predict(prompt.format(bio=current_bio, platform=platform))
            
            st.success("Bio Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
