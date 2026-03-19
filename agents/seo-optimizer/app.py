import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="SEO Content Optimizer", page_icon="📈")

st.title("📈 SEO Meta-Content Optimizer")
st.markdown("Generate high-ranking titles, meta descriptions, and keywords for your content.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    model = st.selectbox("Model", ["gpt-4o", "gpt-3.5-turbo"])
    target_audience = st.text_input("Target Audience", "General Readers")

content = st.text_area("Paste your article/content here:", height=300)
primary_keyword = st.text_input("Primary Keyword (Optional)")

if st.button("Optimize for SEO 🚀"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    elif not content:
        st.warning("Please paste some content.")
    else:
        with st.spinner("Analyzing and optimizing..."):
            llm = ChatOpenAI(api_key=api_key, model=model)
            
            prompt = PromptTemplate(
                input_variables=["content", "keyword", "audience"],
                template="""
                You are an SEO expert. Analyze the following content and provide:
                1. 3 SEO-optimized Titles (catchy and high CTR).
                2. 2 Meta Descriptions (under 160 characters).
                3. A list of 10 relevant LSI Keywords.
                4. Readability score and 2 tips to improve ranking.

                Content: {content}
                Target Keyword: {keyword}
                Audience: {audience}
                """
            )
            
            response = llm.predict(prompt.format(content=content, keyword=primary_keyword, audience=target_audience))
            
            st.success("Optimization Complete!")
            st.markdown(response)

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) hub.")
