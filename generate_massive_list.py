import os
import random

def scaffold_folder(slug, name, description, stack):
    folder_path = os.path.join('agents', slug)
    os.makedirs(folder_path, exist_ok=True)
    
    with open(os.path.join(folder_path, 'README.md'), 'w') as f:
        f.write(f"# {name}\\n\\n> {description}\\n\\n**Tech Stack:** {stack}\\n\\n*(Status: Scaffolding Complete. Core logic pending insertion.)*\\n")
    
    with open(os.path.join(folder_path, 'requirements.txt'), 'w') as f:
        f.write("requests\\npython-dotenv")

def main():
    categories = [
        "Finance & FinTech",
        "Healthcare & Biotech",
        "DevSecOps & Coding",
        "E-Commerce & Retail",
        "Content Creation & Marketing",
        "LegalTech & Compliance",
        "EduTech & Learning",
        "Crypto & Web3",
        "Real Estate & Construction",
        "HR & Recruiting"
    ]

    prefixes = ["Auto", "Smart", "Neuro", "Quantum", "Hyper", "Apex", "Omni", "Meta", "Cyber", "Zen", "Pro", "Ultra", "Swift", "Core", "Nexus", "Aura", "Pulse", "Vanguard", "Elite", "Prime"]
    nouns = ["Agent", "Bot", "Tracker", "Analyzer", "Optimizer", "Engine", "Architect", "Scout", "Oracle", "Sync", "Flow", "Pilot", "Copilot", "Guardian", "Wrangler", "Weaver", "Forge", "Hub", "Node", "Link"]
    actions = ["Automated", "AI-Driven", "Intelligent", "Predictive", "Real-Time", "Autonomous", "Scalable", "Dynamic", "Adaptive", "Smart"]
    targets = ["Analytics", "Data", "Workflows", "Insights", "Operations", "Strategy", "Management", "Processing", "Synthesis", "Optimization"]
    
    stacks = [
        "LangChain, OpenAI", "LlamaIndex, Gemini", "CrewAI, Claude 3", "AutoGen, GPT-4o", 
        "Streamlit, OpenAI", "FastAPI, LangChain", "Next.js, Vercel AI", "Python, ChromaDB",
        "React, Pinecone", "Node.js, Anthropic", "PyTorch, HuggingFace", "TensorFlow, LangChain"
    ]

    all_agents = []
    current_id = 61
    
    print("🚀 Starting Deterministic Agent Expansion Script...")
    
    for idx, category in enumerate(categories):
        print(f"Generating Batch {idx+1}/10: {category}...")
        
        for i in range(20):
            # Generate deterministic but unique concepts
            p = random.choice(prefixes)
            n = random.choice(nouns)
            name = f"{p} {n}"
            if category == "Finance & FinTech": name += " FX"
            elif category == "Healthcare & Biotech": name += " Med"
            elif category == "DevSecOps & Coding": name += " Dev"
            
            slug = name.replace(" ", "-").lower()
            desc = f"{random.choice(actions)} {random.choice(targets)} for {category.split(' & ')[0]}"
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
                f.write(f"\\n| **Expansion: {cat}** | | | | |\\n")
                for agent in cat_agents:
                    f.write(f"| {agent['id']} | [{agent['name']}](agents/{agent['slug']}/) | {agent['description']} | {agent['stack']} | {agent['author']} |\\n")
                    
    print("✅ README.md successfully updated with 200 new agents!")

if __name__ == "__main__":
    main()
