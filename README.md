# PaperPilot

### Intelligent Document Q&A Powered by Retrieval-Augmented Generation (RAG)

PaperPilot is a document intelligence platform powered by Retrieval-Augmented Generation (RAG). It enables users to interact with their document collections using natural language and receive context-aware answers grounded in source documents.

Rather than relying entirely on an LLM's pretrained knowledge, PaperPilot retrieves relevant information from documents and supplies that context to a language model to generate grounded responses.

## ✨ Key Features

- **Automated Document Ingestion:** Processes source documents through a modular ingestion pipeline.
- **Retrieval-Augmented Generation:** Combines document retrieval with LLM-powered response generation.
- **Hybrid Search:** Combines semantic vector search and BM25 keyword-based retrieval to find relevant document chunks.
- **Context-Aware Responses:** Supplies retrieved document context to the language model.
- **PII Redaction:** Integrates Microsoft Presidio for personally identifiable information detection and anonymization.
- **Prompt Injection Scanning:** Scans document content for potentially malicious instructions.
- **Persistent Vector Storage:** Uses ChromaDB to store document embeddings for subsequent retrieval.
- **Streaming Responses:** Supports streaming generated answers.
- **Modern Python Tooling:** Uses `uv` for dependency and environment management.

## 🏗️ Architecture Overview

PaperPilot follows a modular RAG architecture with two primary workflows.

### 1. Document Ingestion Pipeline

```text
Raw Documents
      ↓
Document Loading
      ↓
PII Redaction
      ↓
Prompt Injection Scanning
      ↓
Text Chunking
      ↓
Embedding Generation (Gemini)
      ↓
ChromaDB
```

### 2. Query and Retrieval Pipeline

```text
User Query
     ↓
Query Embedding (Gemini)
     ↓
Hybrid Retrieval
(BM25 + ChromaDB)
     ↓
Relevant Document Context
     ↓
LLM (Groq API)
     ↓
Generated Answer
```

## 📁 Project Structure

```text
PaperPilot/
│
├── data/
│   ├── raw/                         # Source documents
│   └── chroma_db/                   # Persistent vector database
│
├── scripts/
│   ├── run_ingestion.py             # Document ingestion entry point
│   ├── run_query.py                 # Interactive query entry point
│   └── check_models.py              # Model utility
│
├── src/
│   └── paperpilot/
│       ├── agent/
│       │   └── rag_agent.py         # RAG pipeline implementation
│       │
│       ├── core/
│       │   ├── config.py            # Application configuration
│       │   └── logger.py            # Logging utilities
│       │
│       ├── ingestion/
│       │   ├── pipeline.py          # Ingestion pipeline
│       │   ├── loaders.py           # Document loading
│       │   ├── chunking/
│       │   └── guardrails/
│       │
│       └── retrieval/
│           ├── embedders.py         # Embedding integration
│           ├── vector_store.py      # ChromaDB integration
│           └── hybrid_search.py     # Hybrid retrieval
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| LangChain | RAG orchestration and LLM integration |
| Groq API | LLM-powered response generation |
| Gemini Embeddings | Document and query vectorization |
| ChromaDB | Vector storage and semantic search |
| BM25 | Keyword-based retrieval |
| Microsoft Presidio | PII detection and anonymization |
| PyMuPDF | PDF document processing |
| uv | Python dependency management |
| python-dotenv | Environment variable management |

## 🚀 Getting Started

### Prerequisites

- Python 3.14 or later
- [uv](https://docs.astral.sh/uv/)
- Groq API key
- Google Gemini API key for embeddings

### 1. Clone the Repository

```bash
git clone https://github.com/DroidSammy/PaperPilot.git

cd PaperPilot
```

### 2. Set Up the Environment

Install the dependencies using the project configuration:

```bash
uv sync
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

- `GOOGLE_API_KEY`: Used for document and query embedding generation.
- `GROQ_API_KEY`: Used for LLM response generation.

Generate your keys through [Google AI Studio](https://aistudio.google.com/) and [Groq Console](https://console.groq.com/).

**Important:** Never commit API keys or sensitive credentials to GitHub. Keep `.env` excluded through `.gitignore`.

### 4. Add Your Documents

Place source documents inside the raw data directory:

```text
data/
└── raw/
    ├── company_report.pdf
    ├── technical_documentation.pdf
    └── project_notes.md
```

## ⚙️ Core Components

### Document Ingestion

The ingestion pipeline prepares source documents for retrieval through the following stages:

1. Document loading and text extraction.
2. PII detection and redaction.
3. Prompt injection scanning.
4. Document chunking.
5. Embedding generation.
6. Persistent storage in ChromaDB.

### Vector Retrieval

The retrieval component combines ChromaDB semantic similarity search with BM25 keyword-based retrieval using LangChain's `EnsembleRetriever` to identify relevant document chunks.

### RAG Pipeline

The RAG pipeline uses LangChain to combine retrieved document context with the user's query.

The retrieved chunks are passed to the Groq API using the `openai/gpt-oss-120b` model, which generates responses grounded in the provided document context.

The pipeline also supports streaming generated responses.

## 🔄 How It Works

| Component | Responsibility |
|---|---|
| Document Loader | Extracts content from source documents |
| PII Redactor | Identifies and redacts sensitive information |
| Injection Scanner | Scans document content for potential prompt injection |
| Chunker | Splits documents into smaller segments |
| Embedding Model | Converts text into numerical vector representations |
| ChromaDB | Stores and indexes document embeddings |
| Hybrid Retriever | Finds relevant chunks using semantic and keyword search |
| RAG Pipeline | Combines retrieved context with the user query |
| LLM (Groq) | Generates natural-language responses using retrieved context |

## 🗺️ Future Enhancements

- [ ] Improve and evaluate hybrid retrieval.
- [ ] Add source citations and document references to generated answers.
- [ ] Implement conversation history and multi-turn conversations.
- [ ] Add metadata filtering for document retrieval.
- [ ] Build a React-based chat interface.
- [ ] Add authentication and multi-user document isolation.
- [ ] Containerize the application using Docker.
- [ ] Implement retrieval and answer evaluation metrics.
- [ ] Add document upload and management APIs.
- [ ] Expand support for additional document formats.

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

## 👨‍💻 Project Credits

**Author:** Sameer Singh

- GitHub: [DroidSammy](https://github.com/DroidSammy)
- LinkedIn: [Sameer Singh](https://www.linkedin.com/in/sameersingh07/)

PaperPilot is a rebranded and modified version of the original project, developed with permission from the original author.

---

**PaperPilot — Turn your documents into knowledge.**