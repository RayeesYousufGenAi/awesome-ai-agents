import streamlit as st
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="📧 AI Email Writer", page_icon="📧")

st.title("📧 AI Email Writer")
st.caption("Generate professional, tone-aware emails in any language — powered by GPT-4o.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.environ.get("OPENAI_API_KEY", ""))
    
    target_lang = st.selectbox("Output Language", 
                               ["English", "Hindi", "Spanish", "French", "German", "Japanese", "Chinese", "Arabic"])
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("- Be specific about the recipient.\n- Mention any key dates or links.\n- Choose a tone that matches your relationship.")

if not api_key:
    st.warning("Please provide an OpenAI API Key in the sidebar or set `OPENAI_API_KEY` in your `.env` file.")
    st.stop()

# Initialize OpenAI
try:
    llm = ChatOpenAI(model="gpt-4o", api_key=api_key)
except Exception as e:
    st.error(f"Error initializing OpenAI: {e}")
    st.stop()

# Input area
context = st.text_area("What is the email about?", 
                       placeholder="e.g. Asking my manager for a 1:1 to discuss a promotion, mentioning my recent successful project launch.", 
                       height=150)

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("Select tone:", ["Professional", "Formal", "Casual", "Friendly", "Direct", "Apologetic"])
with col2:
    length = st.select_slider("Ideal Length", options=["Short", "Medium", "Detailed"], value="Medium")

if st.button("Generate Email 🚀"):
    if not context:
        st.warning("Please enter some context first.")
    else:
        with st.spinner(f"Writing your email in {target_lang}..."):
            prompt = f"""
            You are a professional communication expert.
            Task: Write a highly professional {tone.lower()} email in the {target_lang} language.
            
            Context: {context}
            Ideal Length: {length}
            
            Format:
            - Clear Subject Line
            - Professional Greeting
            - Well-structured Body (logical flow)
            - Professional Closing
            
            Rules:
            - Content MUST be in {target_lang}.
            - Don't use placeholders like [Your Name] if the context didn't provide it, instead use generic labels or [Name].
            - Ensure the tone is strictly {tone}.
            """
            
            try:
                response = llm.predict(prompt)
                
                if response:
                    st.success(f"Email Generated in {target_lang}!")
                    
                    st.markdown("### 📝 Draft")
                    st.code(response, language="markdown")
                    
                    st.info("💡 You can copy the text directly from the block above.")
                else:
                    st.error("The model returned an empty response. Please try reframing your context.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")