# 🧬 ArXiv Research Paper Analyzer

A sophisticated AI agent that helps researchers find, download, and summarize academic papers from ArXiv. It uses GPT-4 to analyze full PDF contents and extract key contributions.

## ✨ Features
- **Integrated Search**: Search papers directly via keyword or ArXiv ID.
- **Deep PDF Analysis**: Downloads and parses full paper PDFs (not just abstracts).
- **AI Summarization**: Generates structured summaries using LangChain's Map-Reduce chain.
- **Key Takeaways**: Automatically identifies technical contributions and novelty.

## 🛠️ Tech Stack
- **Source**: `arxiv` Python library
- **PDF Parsing**: `pypdf`
- **Framework**: Streamlit
- **Logic**: LangChain + OpenAI GPT-4

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Usage:**
   - Enter your OpenAI API Key in the sidebar.
   - Search for a topic (e.g., "AI Ethics").
   - Click **Analyze PDF** on any result to get deep insights.
