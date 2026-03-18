import streamlit as st
import google.generativeai as genai

# Set your API key here
genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-pro")

st.title("📧 AI Email Writer")

context = st.text_area("Enter email context:")
tone = st.selectbox("Select tone:", ["Formal", "Casual", "Friendly"])

if st.button("Generate Email"):
    prompt = f"""
    Write a {tone.lower()} professional email based on this context:

    {context}

    Include:
    - Subject line
    - Greeting
    - Well-structured body
    - Closing
    """

    response = model.generate_content(prompt)
    st.write(response.text)