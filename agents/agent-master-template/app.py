import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Agent Master Template", page_icon="🤖")

st.title("🤖 Agent Hub Master Template")
st.markdown("The official base for generating the next 950 agents in this repository.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

agent_name = st.text_input("Name of the next Agent:", placeholder="e.g. AI Lawyer")
core_function = st.text_area("What should this agent do?", height=150)

if st.button("Generate Full Agent Scaffolding 🛠️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not agent_name:
        st.warning("Please name your agent.")
    else:
        with st.spinner("Spawning files..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["name", "function"],
                template="""
                You are a Meta-Agent. Generate the full Python code for a Streamlit app called '{name}'.
                It must do: {function}
                
                The code should follow the 'Awesome AI Agents' standard:
                - Sidebar for API Key.
                - Professional UI with Streamlit.
                - Error handling.
                - Integration with LangChain/OpenAI.
                
                Return ONLY the Python code.
                """
            )
            
            response = llm.predict(prompt.format(name=agent_name, function=core_function))
            
            st.success(f"Scaffolding for {agent_name} generated!")
            st.markdown(f"### [NEW] `agents/{agent_name.lower().replace(' ', '-')}/app.py`")
            st.code(response, language="python")
            
            st.info("💡 Copy this code and create the folder in the repository to add your agent!")

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
