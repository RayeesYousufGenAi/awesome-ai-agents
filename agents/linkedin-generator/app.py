import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="LinkedIn Post Generator", page_icon="🔗")

st.title("🔗 LinkedIn Post Generator")
st.markdown("Generate high-engagement LinkedIn posts from any topic or link using AI.")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    model = st.selectbox("Select Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"])
    temperature = st.slider("Creativity Level", 0.0, 1.0, 0.7)

# Main UI
topic = st.text_area("What is your post about? (or paste a link/article)", placeholder="e.g., The future of AI Agents in 2025...")
style = st.selectbox("Post Style", ["Viral/Hook-based", "Professional/Insightful", "Personal Story", "Casual/Relatable"])
target_audience = st.text_input("Target Audience (Optional)", placeholder="e.g., Software Engineers, Founders, Recruiters")

if st.button("Generate Post 🚀"):
    if not api_key:
        st.error("Please enter your OpenAI API Key in the sidebar.")
    elif not topic:
        st.error("Please enter a topic or link.")
    else:
        try:
            with st.spinner("Generating your LinkedIn post..."):
                llm = ChatOpenAI(api_key=api_key, model=model, temperature=temperature)
                
                system_prompt = """
                You are an expert LinkedIn Content Creator and Ghostwriter. Your goal is to write high-engagement posts that drive comments and shares.
                Guidelines:
                - Use a strong "hook" in the first 2 lines.
                - Use white space for readability.
                - Use bullet points if listing items.
                - End with a clear Call to Action (CTA) or a thought-provoking question.
                - Add 3-5 relevant hashtags.
                - Style: {style}
                - Target Audience: {audience}
                """
                
                user_prompt = "Generate a LinkedIn post about the following topic: {topic}"
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("user", user_prompt)
                ])
                
                chain = prompt | llm | StrOutputParser()
                response = chain.invoke({
                    "style": style,
                    "audience": target_audience if target_audience else "General Professional",
                    "topic": topic
                })
                
                st.success("Generated Post:")
                st.code(response, language="markdown")
                st.button("Copy to Clipboard", on_click=st.write, args=(response,)) # Simple mockup
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
