import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Interview Coach", page_icon="👨‍🏫")

st.title("👨‍🏫 AI Coding Interview Coach")
st.markdown("Practice your technical interviews with an AI that gives real-time feedback and hints.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    role = st.selectbox("Target Role", ["Frontend Developer", "Backend Developer", "Fullstack", "Data Engineer"])
    difficulty = st.select_slider("Difficulty", options=["Junior", "Mid-level", "Senior"])

# Session state for conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Chat
if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": f"Hello! I'm your {role} interviewer today. Are you ready to start with a technical question?"})

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if user_input := st.chat_input("Your answer or 'Start Interview'"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.spinner("Interviewer is thinking..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            # Create a history-aware prompt
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            
            prompt = f"""
            You are a technical interviewer for a {difficulty} {role} position.
            
            Context:
            - Ask challenging coding or architectural questions.
            - If the user provides an answer, evaluate it and provide constructive feedback.
            - If they are stuck, give a subtle hint.
            - Keep the conversation professional and encouraging.

            Current Conversation:
            {history}

            Interviewer:
            """
            
            response = llm.predict(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

if st.button("Reset Interview"):
    st.session_state.messages = []
    st.rerun()

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
