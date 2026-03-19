import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Recipe Generator", page_icon="🍳")

st.title("🍳 AI Recipe Generator")
st.markdown("No more 'what to eat?' moments. Generate recipes based on ingredients you already have.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"])
    diet = st.multiselect("Dietary Restrictions", ["Vegan", "Gluten-Free", "Keto", "Paleo", "None"])

ingredients = st.text_area("What's in your fridge? (comma separated):", placeholder="e.g. Eggs, Tomato, Spinach, Bread.")

if st.button("Generate Recipe 👩‍🍳"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not ingredients:
        st.warning("Please provide ingredients.")
    else:
        with st.spinner("Chef AI is cooking up something..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["ingredients", "meal", "diet"],
                template="""
                You are a world-class chef. Create a {meal} recipe using primarily these ingredients: {ingredients}.
                Compliance: {diet}
                
                Format:
                - Name of dish
                - Prep time / Cook time
                - Ingredients list
                - Step-by-step instructions
                - Nutrition info (estimate)
                - Why this works (Chef's secret tip)
                """
            )
            
            response = llm.predict(prompt.format(ingredients=ingredients, meal=meal_type, diet=", ".join(diet)))
            
            st.success("Recipe Ready!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
