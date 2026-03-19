import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
import os
from dotenv import load_dotenv
import tempfile

load_dotenv()

st.set_page_config(page_title="PDF Flashcard Creator", page_icon="📇")

st.title("📇 PDF Flashcard Creator")
st.markdown("Turn your lecture slides or textbooks into Anki-style flashcards instantly.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    num_cards = st.slider("Max Flashcards", 5, 20, 10)

uploaded_file = st.file_uploader("Upload a Study PDF", type="pdf")

if uploaded_file and st.button("Generate Flashcards ✨"):
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    else:
        try:
            with st.spinner("Reading PDF and extracting concepts..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                loader = PyPDFLoader(tmp_path)
                pages = loader.load_and_split()
                
                # Use only the first few identifying pages to save tokens if it's a huge book
                context = "\n".join([p.page_content for p in pages[:10]])
                
                llm = ChatOpenAI(api_key=api_key, model="gpt-4o")
                
                prompt = f"""
                You are a learning expert. Create {num_cards} flashcards from the following study material.
                Each flashcard must have a 'Question' and an 'Answer'.
                Focus on key definitions, formulas, and core concepts.

                Material:
                {context}
                """
                
                response = llm.predict(prompt)
                
                st.success("Flashcards Generated!")
                st.markdown(response)
                
                os.unlink(tmp_path)
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("Built for the [Awesome AI Agents](https://github.com/RayeesYousufGenAi/awesome-ai-agents) collection.")
