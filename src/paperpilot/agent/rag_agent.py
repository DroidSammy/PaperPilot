import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from paperpilot.core.logger import get_logger

logger = get_logger(__name__)

class RAGAgent:
    def __init__(self, retriever):
        
        groq_api_key = os.getenv("GROQ_API_KEY")

        if not groq_api_key:
             raise ValueError("GROQ_API_KEY not found in environment variables.")

        self.llm = ChatGroq(
            model="openai/gpt-oss-120b",
            api_key=groq_api_key,
            temperature=0.1
        )

        self.retriever = retriever
        
        system_prompt = (
            "You are an intelligent assistant. Use the following pieces of retrieved "
            "context to answer the user's question. If you don't know the answer, "
            "just say that you don't know. Keep the answer concise and accurate.\n\n"
            "Context:\n{context}"
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        self.qa_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, self.qa_chain)
        logger.info("RAG Agent initialized.")

    def ask(self, query: str):
        for chunk in self.rag_chain.stream({"input": query}):
            if "answer" in chunk:
                print(chunk["answer"], end="", flush=True)
        print()