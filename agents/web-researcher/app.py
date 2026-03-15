"""
AI Web Researcher — Enter a topic and get AI-curated research.
Scrapes the web and summarizes findings using GPT-4.
Author: Rayees Yousuf (@RayeesYousufGenAi)
"""

import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="🌐 AI Web Researcher", page_icon="🌐", layout="wide")
st.title("🌐 AI Web Researcher")
st.caption("Enter a topic or URL — get AI-powered research summary with key findings")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def scrape_url(url: str) -> str:
    """Scrape text content from a URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; AIResearcher/1.0)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts, styles, and navigation
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        return text[:8000]  # Limit to avoid token overflow
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"


def research_topic(topic: str) -> str:
    """Use GPT-4 to research a topic."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert researcher. Given a topic, provide a comprehensive "
                    "research summary with:\n"
                    "1. **Overview** — What is this topic about?\n"
                    "2. **Key Facts** — Important facts and statistics\n"
                    "3. **Current Trends** — What's happening now?\n"
                    "4. **Pros & Cons** — Different perspectives\n"
                    "5. **Key Resources** — Where to learn more\n"
                    "Use markdown formatting with headers and bullet points."
                ),
            },
            {"role": "user", "content": f"Research this topic thoroughly: {topic}"},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content


def analyze_url(url: str, question: str = "") -> str:
    """Scrape a URL and analyze its content."""
    content = scrape_url(url)

    prompt = f"Analyze this web page content:\n\n{content}"
    if question:
        prompt += f"\n\nSpecifically answer: {question}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert content analyst. Analyze the given web page content "
                    "and provide a clear, structured summary with key takeaways. "
                    "Use markdown formatting."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


# UI
tab1, tab2 = st.tabs(["🔍 Research a Topic", "🌐 Analyze a URL"])

with tab1:
    topic = st.text_input("📝 Enter a topic to research:", placeholder="e.g., AI Agents in 2025")
    if st.button("🔍 Research", type="primary", key="research"):
        if topic:
            with st.spinner("🧠 Researching..."):
                result = research_topic(topic)
            st.markdown("---")
            st.markdown(result)
        else:
            st.warning("Please enter a topic!")

with tab2:
    url = st.text_input("🔗 Enter a URL to analyze:", placeholder="https://example.com/article")
    question = st.text_input("❓ Specific question (optional):", placeholder="What are the key points?")
    if st.button("🌐 Analyze", type="primary", key="analyze"):
        if url:
            with st.spinner("🕷️ Scraping and analyzing..."):
                result = analyze_url(url, question)
            st.markdown("---")
            st.markdown(result)
        else:
            st.warning("Please enter a URL!")
