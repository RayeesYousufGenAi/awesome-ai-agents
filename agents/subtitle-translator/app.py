import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Subtitle Translator", page_icon="🌍")

st.title("🌍 AI Subtitle Translator")
st.markdown("Translate SRT or plain text subtitles while maintaining timing and context.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    target_lang = st.selectbox("Target Language", ["Hindi", "Spanish", "French", "German", "Japanese", "Chinese"])

subtitles = st.text_area("Paste SRT content or text here:", height=300)

if st.button("Translate 🚀"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not subtitles:
        st.warning("Please paste some content.")
    else:
        with st.spinner(f"Translating to {target_lang}..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["subs", "lang"],
                template="""
                You are a Professional Translator. Translate the following subtitles into {lang}.
                
                Rules:
                - Maintain the SRT format (timestamps and sequence numbers).
                - Ensure the translation fits the timing (don't make lines too long).
                - Preserve tone and context.
                
                Subtitles:
                {subs}
                """
            )
            
            response = llm.predict(prompt.format(subs=subtitles, lang=target_lang))
            
            st.success("Translation Complete!")
            st.text_area("Result:", response, height=300)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
