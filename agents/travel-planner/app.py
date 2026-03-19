import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Travel Itinerary Planner", page_icon="✈️")

st.title("✈️ AI Travel Itinerary Planner")
st.markdown("Get a custom, day-by-day travel plan based on your destination, budget, and style.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    budget = st.selectbox("Budget Level", ["Shoestring", "Moderate", "Luxury"])
    days = st.number_input("Duration (Days)", 1, 14, 3)

dest = st.text_input("Where are you going?", placeholder="e.g. Kyoto, Japan")
style = st.multiselect("Vibe", ["Adventure", "Foodie", "Culture", "Relaxation", "Nightlife"])

if st.button("Plan My Trip 🌍"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not dest:
        st.warning("Please provide a destination.")
    else:
        with st.spinner(f"Crafting your {dest} itinerary..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["dest", "budget", "days", "style"],
                template="""
                You are a world-class travel agent. Create a {days}-day itinerary for {dest}.
                Budget: {budget}
                Interest/Style: {style}
                
                For each day, provide:
                - Morning activity
                - Lunch suggestion
                - Afternoon activity
                - Dinner suggestion
                - A Pro-Tip for that city (specific to the budget).
                """
            )
            
            response = llm.predict(prompt.format(dest=dest, budget=budget, days=days, style=", ".join(style)))
            
            st.success("Itinerary Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
