# 📺 YouTube Video Summarizer

An AI-powered agent that generates summaries from YouTube video transcripts using GPT-4.

## ✨ Features
- 🔗 Accepts various YouTube URL formats (youtube.com, youtu.be, embed)
- 📝 Automatically extracts video transcripts
- 🧠 Generates AI summaries with key points and notable details
- ⚡ Handles long videos (1hr+) with intelligent chunking
- 🎨 Clean Streamlit interface with loading states
- 🛡️ Graceful error handling for missing transcripts, invalid URLs, and API errors

## 🛠️ Tech Stack
- **youtube-transcript-api** — Extract video transcripts
- **OpenAI GPT-4** — Generate summaries
- **Streamlit** — Web UI
- **python-dotenv** — Environment variable management

## 🚀 Quick Start

```bash
cd agents/youtube-summarizer
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
streamlit run app.py
```

## 👤 Author
Rayees Yousuf — [@RayeesYousufGenAi](https://github.com/RayeesYousufGenAi)
