# 🤝 Contributing to Awesome AI Agents

First off, **thank you** for considering contributing! This project is community-driven, and every contribution makes it better. 🙌

Whether you're adding a new AI agent, fixing a bug, improving documentation, or suggesting ideas — **you're welcome here**.

---

## 📋 Table of Contents

- [How to Contribute](#-how-to-contribute)
- [Adding a New Agent (Step-by-Step)](#-adding-a-new-agent-step-by-step)
- [Agent Requirements](#-agent-requirements)
- [Code Style](#-code-style)
- [Pull Request Process](#-pull-request-process)
- [Need Help?](#-need-help)

---

## 🚀 How to Contribute

### Option 1: Add a New AI Agent (Most popular!)
This is the **best way** to contribute. Build an AI agent and add it to the collection! See the [step-by-step guide](#-adding-a-new-agent-step-by-step) below.

### Option 2: Improve an Existing Agent
- Fix bugs
- Add new features
- Improve error handling
- Add tests

### Option 3: Improve Documentation
- Fix typos
- Add usage examples
- Improve README files
- Add architecture diagrams

### Option 4: Suggest Ideas
- [Open a "New Agent" issue](../../issues/new?template=new_agent.md) to propose an agent idea
- [Open a "Feature Request"](../../issues/new?template=feature_request.md) for improvements

---

## 🤖 Adding a New Agent (Step-by-Step)

### Step 1: Fork & Clone

```bash
# Fork this repo on GitHub (click the "Fork" button at the top!)

# Then clone YOUR fork:
git clone https://github.com/YOUR-USERNAME/awesome-ai-agents.git
cd awesome-ai-agents
```

### Step 2: Create a Branch

```bash
git checkout -b add-agent/your-agent-name
```

### Step 3: Create Your Agent Folder

```bash
mkdir -p agents/your-agent-name
```

Your folder MUST contain:

```
agents/your-agent-name/
├── app.py              # Main application file
├── README.md           # Documentation for your agent
└── requirements.txt    # Python dependencies
```

### Step 4: Build Your Agent

Write your AI agent code in `app.py`. Here's a minimal template:

```python
"""
Your Agent Name — Brief description of what it does.
Author: Your Name (@your-github)
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Your agent implementation here

def main():
    """Main entry point for the agent."""
    # Your code here
    pass

if __name__ == "__main__":
    main()
```

### Step 5: Write Documentation

Create a `README.md` in your agent folder with:

```markdown
# 🤖 Your Agent Name

Brief description of what this agent does.

## ✨ Features
- Feature 1
- Feature 2

## 🛠️ Tech Stack
- Framework (e.g., LangChain, CrewAI)
- API (e.g., OpenAI, Anthropic)

## 🚀 Quick Start

### Install dependencies
\`\`\`bash
cd agents/your-agent-name
pip install -r requirements.txt
\`\`\`

### Set up environment
\`\`\`bash
export OPENAI_API_KEY="your-key-here"
\`\`\`

### Run the agent
\`\`\`bash
python app.py
\`\`\`

## 📝 How It Works
Explain the architecture and logic.

## 👤 Author
Your Name — [GitHub](https://github.com/your-profile)
```

### Step 6: Update the Main README

Add your agent to the **Agents Collection** table in the root `README.md`:

```markdown
| 🤖 Your Agent Name | Brief description | LangChain, OpenAI | [@you](https://github.com/you) |
```

### Step 7: Commit & Push

```bash
git add .
git commit -m "✨ Add: Your Agent Name — brief description"
git push origin add-agent/your-agent-name
```

### Step 8: Open a Pull Request 🎉

Go to the original repo and click **"Compare & pull request"**. Fill in the PR template and submit!

---

## ✅ Agent Requirements

Your agent **must** have:

| Requirement | Description |
|------------|-------------|
| ✅ Working code | It should run without errors |
| ✅ README.md | Clear documentation with setup instructions |
| ✅ requirements.txt | All Python dependencies listed |
| ✅ Environment variables | API keys via `os.environ` or `.env`, never hardcoded |
| ✅ Error handling | Graceful error handling for API failures |

Your agent **should NOT**:

| ❌ Don't | Why |
|----------|-----|
| Hardcode API keys | Security risk |
| Include `__pycache__/` or `.env` | Already in `.gitignore` |
| Modify other agents | One agent per PR |
| Include large binary files | Keep the repo lightweight |

---

## 🎨 Code Style

- Follow **PEP 8** Python coding style
- Add **docstrings** to all functions
- Use **type hints** where possible
- Keep code **readable** and well-commented
- Use **descriptive** variable names

---

## 📤 Pull Request Process

1. **Fill in the PR template completely**
2. **Ensure your agent runs without errors**
3. **Wait for review** — maintainers will review within 48 hours
4. **Address feedback** — make requested changes
5. **Get merged!** 🎉

### What happens after your PR is merged?

- Your agent appears in the main README with your name
- You become a **contributor** to the project
- Your GitHub profile shows the contribution
- You get credited in the Contributors section

---

## ❓ Need Help?

- 💬 [Open a Discussion](../../discussions) to ask questions
- 🐛 [Report a Bug](../../issues/new?template=bug_report.md) if something's broken
- 💡 [Suggest an Agent](../../issues/new?template=new_agent.md) if you have an idea

---

<p align="center">
  <strong>Every contribution counts. Let's build the best AI agents collection together! 🚀</strong>
</p>
