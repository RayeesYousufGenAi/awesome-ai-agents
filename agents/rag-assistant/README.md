# 📄 RAG Document Assistant

Upload any PDF and ask questions — the agent retrieves relevant chunks and generates accurate answers using RAG (Retrieval-Augmented Generation).

## ✨ Features
- 📄 Upload and process any PDF document
- 🔍 Semantic search using ChromaDB
- 🧠 GPT-4 powered answer generation
- 📋 Shows source chunks for transparency

## 🛠️ Tech Stack
- **LangChain** — RAG pipeline
- **ChromaDB** — Vector storage
- **OpenAI** — Embeddings + GPT-4
- **Streamlit** — Web UI

## 🚀 Quick Start

```bash
cd agents/rag-assistant
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
streamlit run app.py
```

## 👤 Author
Rayees Yousuf — [@RayeesYousufGenAi](https://github.com/RayeesYousufGenAi)
