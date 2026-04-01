import os
import random

def scaffold_folder(slug, name, description, stack):
    folder_path = os.path.join('agents', slug)
    os.makedirs(folder_path, exist_ok=True)
    
    badge_stack = stack.replace(' ', '%20').replace(',', '')
    readme_content = f"""# {name}

<p align="center">
  <img src="https://img.shields.io/badge/Status-Scaffolded-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Stack-{badge_stack}-blue?style=for-the-badge" />
</p>

> {description}

## 🚀 Quick Start
```bash
cd {slug}
pip install -r requirements.txt
python app.py
```

*(Note: This is an automatically generated scaffolding folder. Core application logic is pending PR insertion.)*
"""
    
    with open(os.path.join(folder_path, 'README.md'), 'w') as f:
        f.write(readme_content)
    
    with open(os.path.join(folder_path, 'requirements.txt'), 'w') as f:
        f.write("requests\npython-dotenv\nlangchain\nopenai\nnumpy\npandas")

def main():
    # 25 Categories * 20 Agents = 500 Agents
    categories = [
        "AI Agent Orchestration", "Robotics & IoT", "Supply Chain & Logistics", 
        "Customer Support AI", "Game Development & NPCs", "No-Code Automations",
        "Personal Assistants", "Data Engineering AI", "Cybersecurity & DefSec",
        "Video Production AI", "Music & Audio Synthesis", "AgriTech & Farming",
        "Language Translation", "Academic Research & ArXiv", "Astrophysics AI",
        "Climate Tech & ESG", "Fitness & Nutrition", "Psychology & Therapy",
        "Event Management", "Non-Profit & ONG AI", "Politics & OSINT",
        "Fashion & Design", "Interior Architecture", "Salesforce & CRM",
        "Quantitative Trading"
    ]

    prefixes = ["Omni", "Core", "Vanguard", "Apex", "Neuro", "Cyber", "Quantum", "Hyper", "Zen", "Pro", "Ultra", "Swift", "Nexus", "Astral", "Echo", "Flux", "Nova", "Titan", "Vertex", "Zephyr"]
    nouns = ["Engine", "Forge", "Hub", "Node", "Link", "Sync", "Weaver", "Scout", "Oracle", "Pilot", "Wrangler", "Copilot", "Guardian", "Analyzer", "Optimizer", "Architect", "Tracker", "Bot", "Agent", "Synth"]
    actions = ["Automated", "Adaptive", "Dynamic", "Scalable", "Intelligent", "Predictive", "Autonomous", "Real-Time", "Smart", "Algorithmic"]
    targets = ["Synthesis", "Optimization", "Management", "Strategy", "Operations", "Workflows", "Insights", "Processing", "Analytics", "Routing"]
    
    stacks = [
        "LangChain, OpenAI", "LlamaIndex, Gemini", "CrewAI, Claude 3", "AutoGen, GPT-4o", 
        "Streamlit, OpenAI", "FastAPI, LangChain", "Next.js, Vercel AI", "Python, ChromaDB",
        "React, Pinecone", "Node.js, Anthropic", "PyTorch, HuggingFace", "TensorFlow, LangChain",
        "Supabase, OpenAI", "Golang, Claude 3", "Rust, HuggingFace", "Docker, AutoGen"
    ]

    all_agents = []
    current_id = 261 # Since we already have 260
    
    print("🚀 Starting 500-Agent Massive Expansion Script...")
    
    for idx, category in enumerate(categories):
        print(f"Generating Batch {idx+1}/25: {category}...")
        
        for i in range(20):
            p = random.choice(prefixes)
            n = random.choice(nouns)
            name = f"{p} {n}"
            
            # Add niche flair
            if "Gaming" in category: name += " NPC"
            elif "Audio" in category: name += " DJ"
            elif "Crypto" in category: name += " Web3"
            elif "Cyber" in category: name += " Sec"
            
            slug = name.replace(" ", "-").lower() + f"-{random.randint(100,999)}" # ensure unique slug
            desc = f"{random.choice(actions)} {random.choice(targets)} for {category}"
            stack = random.choice(stacks)
            author = "[@RayeesYousufGenAi](https://github.com/RayeesYousufGenAi)"
            
            agent = {
                'id': current_id, 'name': name, 'slug': slug, 
                'description': desc, 'stack': stack, 'author': author, 'category': category
            }
            
            scaffold_folder(slug, name, desc, stack)
            all_agents.append(agent)
            current_id += 1
            
        print(f"✅ Generated 20 agents for {category}.")
        
    print(f"\\n✅ Total Agents Generated: {len(all_agents)}")
    
    with open('README.md', 'a') as f:
        for cat in categories:
            cat_agents = [a for a in all_agents if a.get('category') == cat]
            if cat_agents:
                f.write(f"\\n### 🌐 {cat}\\n")
                f.write("| ID | Agent | Description | Tech Stack | Author |\\n")
                f.write("|---|-------|-------------|------------|--------|\\n")
                for agent in cat_agents:
                    f.write(f"| {agent['id']} | [{agent['name']}](agents/{agent['slug']}/) | {agent['description']} | {agent['stack']} | {agent['author']} |\\n")
                    
    print("✅ README.md successfully updated with 500 new agents!")

if __name__ == "__main__":
    main()
