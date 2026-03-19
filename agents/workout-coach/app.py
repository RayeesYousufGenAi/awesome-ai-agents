import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Workout Planner", page_icon="💪")

st.title("💪 AI Personal Workout Planner")
st.markdown("Get a customized training routine based on your goals, equipment, and level.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    level = st.selectbox("Experience", ["Beginner", "Intermediate", "Advanced"])
    days = st.slider("Days per week", 1, 7, 3)

goal = st.text_input("Goal (e.g. Weight loss, Muscle gain, Marathon training):")
equipment = st.multiselect("Available Equipment", ["None (Bodyweight)", "Dumbbells", "Full Gym", "Resistance Bands"])

if st.button("Generate Routine 🏋️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not goal:
        st.warning("Please provide a goal.")
    else:
        with st.spinner("Calculating split and volume..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["goal", "level", "days", "equip"],
                template="""
                You are a Certified Personal Trainer. Create a {days}-day workout split for a {level} trainee.
                Goal: {goal}
                Equipment: {equip}
                
                Provide:
                - The Split (e.g. Push/Pull/Legs).
                - Daily Routine: (Exercise, Sets, Reps).
                - 1 Recovery Tip.
                - Caution: A short safety disclaimer.
                """
            )
            
            response = llm.predict(prompt.format(goal=goal, level=level, days=days, equip=", ".join(equipment)))
            
            st.success("Plan Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
