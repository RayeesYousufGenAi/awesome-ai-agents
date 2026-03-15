# 📖 Building an AI Agent from Scratch — Step-by-Step Tutorial

Welcome! This tutorial will guide you through building your first AI agent and submitting it to this collection. By the end, you'll have a working agent with a beautiful UI and know how to contribute it back to the community.

---

## 📋 What You'll Build

A **Quote Generator Agent** — an AI that generates inspirational quotes based on topics the user provides. It's simple enough for beginners but demonstrates all the key concepts.

---

## 🎯 Prerequisites

- Python 3.8+ installed
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Basic Python knowledge
- Git installed

---

## Step 1: Setting Up the Project

### 1.1 Fork and Clone the Repository

First, fork this repository on GitHub, then clone your fork:

```bash
# Click "Fork" on GitHub first, then:
git clone https://github.com/YOUR-USERNAME/awesome-ai-agents.git
cd awesome-ai-agents
```

### 1.2 Create Your Agent Folder

Create a new folder for your agent:

```bash
mkdir -p agents/quote-generator
cd agents/quote-generator
```

### 1.3 Set Up a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

---

## Step 2: Creating the Agent Structure

Your agent folder needs 3 files:

```
agents/quote-generator/
├── app.py              # Main application code
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

Let's create them one by one.

### 2.1 Create requirements.txt

This lists all the packages your agent needs:

```bash
cat > requirements.txt << 'EOF'
openai>=1.12.0
streamlit>=1.30.0
python-dotenv>=1.0.0
EOF
```

**What each package does:**
- `openai` — Connects to OpenAI's API
- `streamlit` — Creates the web UI
- `python-dotenv` — Loads environment variables from a `.env` file

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3: Using OpenAI API

### 3.1 Set Up Your API Key

Create a `.env` file to store your API key securely:

```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

> ⚠️ **Never commit your `.env` file!** It's already in `.gitignore`.

### 3.2 Create the Basic Agent (app.py)

Let's start with a simple script that uses the OpenAI API:

```python
"""
Quote Generator — AI-powered inspirational quote generator.
Author: Your Name (@your-github)
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_quote(topic: str) -> str:
    """Generate an inspirational quote about the given topic."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an inspirational quote generator. "
                           "Create thoughtful, inspiring quotes."
            },
            {
                "role": "user",
                "content": f"Generate an inspirational quote about: {topic}"
            }
        ],
        temperature=0.8,
        max_tokens=100
    )
    return response.choices[0].message.content


def main():
    """Main entry point for the agent."""
    print("🌟 Quote Generator Agent")
    print("-" * 40)

    topic = input("Enter a topic (e.g., success, creativity): ")
    print("\nGenerating quote...\n")

    try:
        quote = generate_quote(topic)
        print(f'"{quote}"')
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
```

### 3.3 Test Your Agent

Run it from the terminal:

```bash
python app.py
```

Enter a topic like "success" and see your AI-generated quote! 🎉

---

## Step 4: Building the Streamlit UI

Now let's add a beautiful web interface using Streamlit.

### 4.1 Update app.py with Streamlit

Replace your `app.py` with this enhanced version:

```python
"""
Quote Generator — AI-powered inspirational quote generator with Streamlit UI.
Author: Your Name (@your-github)
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_quote(topic: str, style: str = "inspirational") -> str:
    """
    Generate a quote about the given topic.

    Args:
        topic: The subject of the quote
        style: The style of quote (inspirational, funny, philosophical)

    Returns:
        The generated quote text
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a {style} quote generator. "
                           "Create quotes that are memorable and impactful."
            },
            {
                "role": "user",
                "content": f"Generate a {style} quote about: {topic}"
            }
        ],
        temperature=0.8,
        max_tokens=100
    )
    return response.choices[0].message.content


# Streamlit UI Configuration
st.set_page_config(
    page_title="Quote Generator",
    page_icon="✨",
    layout="centered"
)

# App Header
st.title("✨ AI Quote Generator")
st.caption("Generate inspirational quotes on any topic")

# Sidebar for options
with st.sidebar:
    st.header("⚙️ Settings")
    quote_style = st.selectbox(
        "Quote Style:",
        ["inspirational", "funny", "philosophical", "motivational"]
    )
    st.markdown("---")
    st.markdown("Made with ❤️ by [Your Name](https://github.com/your-profile)")

# Main input
topic = st.text_input(
    "Enter a topic:",
    placeholder="e.g., success, creativity, perseverance..."
)

# Generate button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    generate_clicked = st.button("✨ Generate Quote", use_container_width=True)

# Display result
if generate_clicked and topic:
    with st.spinner("Creating your quote..."):
        try:
            quote = generate_quote(topic, quote_style)

            # Display in a nice card
            st.markdown("---")
            st.markdown(f"### 💭 {quote_style.title()} Quote on *{topic}*")
            st.markdown(f"> {quote}")
            st.markdown("---")

            # Add a copy button (shown as text)
            st.code(quote, language=None)

        except Exception as e:
            st.error(f"Error generating quote: {str(e)}")
            st.info("Make sure your OPENAI_API_KEY is set correctly!")

elif generate_clicked and not topic:
    st.warning("Please enter a topic first!")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Powered by OpenAI GPT-3.5 Turbo | Built with Streamlit"
    "</p>",
    unsafe_allow_html=True
)
```

### 4.2 Run Your Streamlit App

```bash
streamlit run app.py
```

Your browser should open automatically! You'll see:
- A beautiful centered layout
- A sidebar with style options
- An input field for topics
- A generate button
- Nicely formatted quote output

---

## Step 5: Writing Documentation

Create a `README.md` for your agent:

```markdown
# ✨ Quote Generator

An AI-powered quote generator that creates inspirational, funny, or philosophical quotes on any topic.

## ✨ Features

- 🎯 Generate quotes on any topic
- 🎨 Multiple quote styles (inspirational, funny, philosophical, motivational)
- 🖥️ Beautiful Streamlit web interface
- ⚡ Fast responses with GPT-3.5 Turbo

## 🛠️ Tech Stack

- **OpenAI GPT-3.5 Turbo** — Language model
- **Streamlit** — Web UI framework
- **Python** — Core language

## 🚀 Quick Start

### 1. Install dependencies

\`\`\`bash
cd agents/quote-generator
pip install -r requirements.txt
\`\`\`

### 2. Set up environment

\`\`\`bash
export OPENAI_API_KEY="your-key-here"
\`\`\`

Or create a `.env` file:
\`\`\`
OPENAI_API_KEY=your-key-here
\`\`\`

### 3. Run the app

\`\`\`bash
streamlit run app.py
\`\`\`

## 📝 How It Works

1. User enters a topic (e.g., "success", "creativity")
2. User selects a quote style from the sidebar
3. The app sends a request to OpenAI's GPT-3.5 Turbo
4. The AI generates a unique quote based on the topic and style
5. The quote is displayed in a beautiful card format

## 👤 Author

Your Name — [@your-profile](https://github.com/your-profile)
```

---

## Step 6: Testing Your Agent

Before submitting, make sure everything works:

### 6.1 Test Checklist

- [ ] `pip install -r requirements.txt` completes without errors
- [ ] `streamlit run app.py` opens the web UI
- [ ] Entering a topic generates a quote
- [ ] Different quote styles work
- [ ] Error handling works (try without API key)

### 6.2 Code Review

Check your code for:
- No hardcoded API keys
- Proper error handling
- Clear comments and docstrings
- Clean, readable formatting

---

## Step 7: Submitting a PR

Now let's contribute your agent back to the community!

### 7.1 Prepare Your Files

Make sure you have these 3 files:

```bash
ls -la agents/quote-generator/
# Should show: app.py, README.md, requirements.txt
```

### 7.2 Commit Your Changes

```bash
# From the repo root
cd /path/to/awesome-ai-agents

# Check what files changed
git status

# Add your new agent folder
git add agents/quote-generator/

# Commit with a descriptive message
git commit -m "✨ Add: Quote Generator Agent — AI-powered inspirational quotes"
```

### 7.3 Update the Main README

Add your agent to the **Agents Collection** table in the root `README.md`:

```markdown
| 6 | [✨ Quote Generator](agents/quote-generator/) | Generate inspirational quotes on any topic | OpenAI, Streamlit | [@your-profile](https://github.com/your-profile) |
```

Also update the agent count badge at the top:
```markdown
<img src="https://img.shields.io/badge/agents-6+-blueviolet?style=for-the-badge" />
```

Commit this change:
```bash
git add README.md
git commit -m "📚 Update README with Quote Generator agent"
```

### 7.4 Push and Create PR

```bash
# Push to your fork
git push origin add-agent/quote-generator

# Or if you used a different branch name:
git push origin your-branch-name
```

Then go to GitHub and:
1. Click **"Compare & pull request"**
2. Fill in the PR template
3. Submit your PR!

---

## 🎉 What Happens Next?

1. **Review** — Maintainers will review your PR within 48 hours
2. **Feedback** — You might get suggestions for improvements
3. **Merge** — Once approved, your agent gets merged!
4. **Credit** — Your name appears in the Contributors section

---

## 💡 Next Steps

Now that you know the basics, try building more advanced agents:

- **Add memory** — Use LangChain to remember user preferences
- **Add tools** — Let your agent search the web or calculate
- **Multi-modal** — Add image generation or voice
- **RAG** — Connect to documents for knowledge-based responses

Check the existing agents in this repo for inspiration!

---

## 📚 Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [CONTRIBUTING.md](CONTRIBUTING.md) — Full contribution guidelines

---

## ❓ Troubleshooting

### "Module not found" errors
Make sure you activated your virtual environment and ran `pip install -r requirements.txt`

### "API key not found" errors
Check that your `.env` file exists and has the correct format, or set the environment variable directly.

### Streamlit won't open
Try running with: `streamlit run app.py --server.port 8501`

---

<p align="center">
  <strong>Happy building! 🚀</strong><br>
  <em>Your first agent is just the beginning.</em>
</p>
