# 🐳 Dockerfile Performance Optimizer

A DevOps agent that audits your Docker containers for security, size, and build performance.

## 🚀 Features
- **Multi-Stage Refactoring**: Automatically suggests multi-stage build patterns.
- **Security Audit**: Detects root user usage and credentials in layers.
- **Layer Optimization**: Minimizes image size by combining redundant `RUN` commands.

## 🛠️ Tech Stack
- LangChain
- OpenAI GPT-4o
- Streamlit

## 🚀 Quick Start
```bash
pip install -r requirements.txt
streamlit run app.py
```
