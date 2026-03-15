"""
Smart Chatbot — AI-powered conversational assistant with memory.
Uses LangChain + OpenAI GPT-4 with conversation history.
Author: Rayees Yousuf (@RayeesYousufGenAi)
"""

import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="🤖 Smart Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Smart Chatbot")
st.caption("AI assistant with conversation memory — powered by GPT-4")

# Initialize the LLM and memory
@st.cache_resource
def init_chain():
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    memory = ConversationBufferWindowMemory(k=15)
    chain = ConversationChain(llm=llm, memory=memory, verbose=False)
    return chain

chain = init_chain()

# Chat history UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chain.predict(input=prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
