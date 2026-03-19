import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="📧 AI Email Writer", page_icon="📧")

st.title("📧 AI Email Writer")
st.caption("Generate professional, tone-aware emails in seconds powered by Google Gemini.")

with st.sidebar:
    st.header("Settings")
    # Priority: Sidebar > Environment Variable
    api_key = st.text_input("Gemini API Key", type="password", value=os.environ.get("GOOGLE_API_KEY", ""))
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("- Be specific about the recipient.\n- Mention any key dates or links.\n- Choose a tone that matches your relationship.")

if not api_key:
    st.warning("Please provide a Gemini API Key in the sidebar or set `GOOGLE_API_KEY` in your `.env` file.")
    st.stop()

# Configure the API
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")
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
        with st.spinner("Writing your email..."):
            prompt = f"""
            Task: Write a highly professional {tone.lower()} email.
            Context: {context}
            Ideal Length: {length}
            
            Format:
            - Clear Subject Line
            - Professional Greeting
            - Well-structured Body (logical flow)
            - Professional Closing
            
            Rules:
            - Don't use placeholders like [Your Name] if the context didn't provide it, instead use generic labels or [Name].
            - Ensure the tone is strictly {tone}.
            """
            
            try:
                response = model.generate_content(prompt)
                
                if response and response.text:
                    st.success("Email Generated!")
                    
                    st.markdown("### 📝 Draft")
                    st.code(response.text, language="markdown")
                    
                    st.info("💡 You can copy the text directly from the block above.")
                else:
                    st.error("The model returned an empty response. Please try reframing your context.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")