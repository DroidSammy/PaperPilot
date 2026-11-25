
import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from paperpilot.ingestion.pipeline import IngestionPipeline
from paperpilot.retrieval.hybrid_search import build_advanced_retriever
from paperpilot.retrieval.vector_store import ChromaRetriever
from paperpilot.agent.rag_agent import RAGAgent

load_dotenv()

PROJECT_ROOT = Path(__file__).parent
DB_PATH = PROJECT_ROOT / "data" / "chroma_db"

st.set_page_config(
    page_title="PaperPilot",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PaperPilot")
st.caption("Your Intelligent Document Assistant")

with st.sidebar:
    st.header("Document Library")
    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process Documents", use_container_width=True):
        if not uploaded_files:
            st.warning("Please upload at least one PDF.")
        else:
            with st.spinner("Processing documents..."):
                try:
                    raw_dir = PROJECT_ROOT / "data" / "raw"
                    raw_dir.mkdir(parents=True, exist_ok=True)

                    for uploaded_file in uploaded_files:
                        file_path = raw_dir / Path(uploaded_file.name).name
                        file_path.write_bytes(uploaded_file.getvalue())

                    pipeline = IngestionPipeline(
                        data_dir=str(raw_dir),
                        db_dir=str(DB_PATH)
                    )
                    count = pipeline.run()

                    st.success(f"Processing complete: {count} chunks stored.")
                    st.session_state.pop("agent", None)

                except Exception as e:
                    st.error(f"Processing failed: {e}")

    st.divider()
    st.caption("PaperPilot | Gemini Embeddings + Groq")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.subheader("💬 Chat with your documents")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask something about your documents..."):
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching your documents..."):
                db_client = ChromaRetriever(db_dir=str(DB_PATH))
                chroma_retriever = db_client.get_retriever(k=10)
                documents = db_client.get_all_document_chunks()

                if not documents:
                    st.warning("No documents found. Upload and process PDFs first.")
                else:
                    retriever = build_advanced_retriever(
                        chroma_retriever=chroma_retriever,
                        documents=documents,
                        top_k=3
                    )

                    agent = RAGAgent(retriever=retriever)

                    response = agent.rag_chain.invoke({"input": question})
                    answer = response.get("answer", "I couldn't generate an answer.")

                    st.markdown(answer)

                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )

        except Exception as e:
            st.error(f"Something went wrong: {e}")
