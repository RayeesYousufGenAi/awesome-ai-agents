import streamlit as st
import arxiv
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="ArXiv Research Analyzer", page_icon="🧬")

st.title("🧬 ArXiv Research Paper Analyzer")
st.markdown("Search, download, and summarize scientific papers from ArXiv.org with AI.")

# Sidebar Configuration
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    model = st.selectbox("LLM Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo-16k"])
    chunk_size = st.slider("Chunk Size", 1000, 5000, 2000)

# Search UI
query = st.text_input("Search for papers (e.g., 'Large Language Models', 'Quantum Computing')", placeholder="Enter keywords or ArXiv ID")
max_results = st.number_input("Max Results", 1, 10, 3)

if st.button("Search Papers 🔍"):
    if not query:
        st.warning("Please enter a search query.")
    else:
        with st.spinner("Searching ArXiv..."):
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            papers = list(client.results(search))
            
            if not papers:
                st.info("No papers found for this query.")
            else:
                for paper in papers:
                    with st.container():
                        st.subheader(paper.title)
                        st.write(f"**Authors:** {', '.join(author.name for author in paper.authors)}")
                        st.write(f"**Published:** {paper.published.strftime('%Y-%m-%d')}")
                        st.write(f"**Summary (ArXiv):** {paper.summary[:300]}...")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.link_button("View on ArXiv", paper.entry_id)
                        with col2:
                            if st.button(f"Analyze PDF 🧠", key=paper.entry_id):
                                if not api_key:
                                    st.error("Please provide an OpenAI API Key in the sidebar.")
                                else:
                                    try:
                                        with st.spinner(f"Analyzing '{paper.title}'..."):
                                            # Download PDF to temp file
                                            with tempfile.TemporaryDirectory() as tmp_dir:
                                                path = paper.download_pdf(dirpath=tmp_dir)
                                                
                                                # Load and Split
                                                loader = PyPDFLoader(path)
                                                pages = loader.load_and_split()
                                                
                                                # Initialize LLM
                                                llm = ChatOpenAI(api_key=api_key, model=model, temperature=0.3)
                                                
                                                # Summary Chain
                                                chain = load_summarize_chain(llm, chain_type="map_reduce")
                                                summary = chain.run(pages)
                                                
                                                st.success("Analysis Complete!")
                                                st.markdown("### 📝 AI Research Summary")
                                                st.write(summary)
                                                
                                                st.markdown("### 💡 Key Takeaways")
                                                # Use a quick prompt for takeaways
                                                takeaway_prompt = f"Based on the following summary, list 3-5 key technical contributions of this paper:\n\n{summary}"
                                                takeaways = llm.predict(takeaway_prompt)
                                                st.write(takeaways)
                                                
                                    except Exception as e:
                                        st.error(f"Analysis failed: {str(e)}")

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
