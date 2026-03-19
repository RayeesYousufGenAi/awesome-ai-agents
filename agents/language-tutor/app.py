import streamlit as st
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Language Tutor", page_icon="🌎")

st.title("🌎 AI Language Tutor")
st.markdown("Practice speaking any language with an AI tutor that corrects your grammar in real-time.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    lang = st.selectbox("I want to practice:", ["Spanish", "French", "German", "Japanese", "Hindi", "English"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display Chat
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

if user_input := st.chat_input(f"Type your {lang} message here..."):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    else:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.spinner("Tutor is typing..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history])
            
            prompt = f"""
            You are a kind and expert {lang} tutor. 
            Behavior:
            1. Respond to the user in {lang}.
            2. If the user made a grammar or vocabulary mistake, provide a correction in English.
            3. Keep the conversation going with a question.
            
            Current Conversation:
            {history}
            
            Tutor:
            """
            
            response = llm.predict(prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
