import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Cover Letter Writer", page_icon="💌")

st.title("💌 AI High-Conversion Cover Letter")
st.markdown("Write a cover letter that actually resonates with hiring managers by matching your bio to a job description.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")

job_desc = st.text_area("Job Description:", height=200)
user_bio = st.text_area("Your Bio/Resume/Achievements:", height=200)

if st.button("Write Letter 🖋️"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not job_desc or not user_bio:
        st.warning("Please provide both info.")
    else:
        with st.spinner("Matching skills to requirements..."):
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
            
            prompt = PromptTemplate(
                input_variables=["job", "bio"],
                template="""
                You are a Career Coach. Write a punchy, professional, and personalized cover letter.
                
                Rules:
                - Hook them in the first paragraph.
                - Don't just list skills; explain how the skill solves the company's problem in the job description.
                - Keep it under 300 words.
                
                Job: {job}
                Candidate: {bio}
                """
            )
            
            response = llm.predict(prompt.format(job=job_desc, bio=user_bio))
            
            st.success("Cover Letter Generated!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
