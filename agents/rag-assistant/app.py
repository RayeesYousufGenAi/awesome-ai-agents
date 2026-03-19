"""
RAG Assistant — Ask questions about your PDF documents.
Uses ChromaDB for vector storage + OpenAI embeddings.
Author: Rayees Yousuf (@RayeesYousufGenAi)
"""

import os
import tempfile
import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="📄 RAG Assistant", page_icon="📄", layout="centered")
st.title("📄 RAG Document Assistant")
st.caption("Upload a PDF and ask questions — powered by RAG + GPT-4o")

# Sidebar for file upload
with st.sidebar:
    st.header("📁 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
    st.info("Your document is processed locally and never stored permanently.")

if uploaded_file:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    # Load and split the PDF
    with st.spinner("📖 Processing document..."):
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(pages)

        # Create vector store
        embeddings = OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY"))
        vectorstore = Chroma.from_documents(chunks, embeddings)

        # Build QA chain
        llm = ChatOpenAI(model="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY"))
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True,
        )

    st.success(f"✅ Loaded {len(pages)} pages, {len(chunks)} chunks")

    # Question input
    question = st.text_input("❓ Ask a question about your document:")

    if question:
        with st.spinner("🔍 Searching..."):
            result = qa_chain.invoke({"query": question})

            st.markdown("### 💬 Answer")
            st.write(result["result"])

            with st.expander("📄 Source chunks"):
                for i, doc in enumerate(result["source_documents"]):
                    st.markdown(f"**Chunk {i+1}** (Page {doc.metadata.get('page', '?')})")
                    st.text(doc.page_content[:300] + "...")

    # Cleanup
    os.unlink(tmp_path)
else:
    st.info("👈 Upload a PDF document to get started!")
