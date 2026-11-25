# PaperPilot

### Intelligent Document Q&A Powered by Retrieval-Augmented Generation (RAG)

PaperPilot is a document intelligence platform powered by Retrieval-Augmented Generation (RAG). It enables users to interact with their document collections using natural language and receive context-aware answers grounded in the source documents.

Rather than relying entirely on an LLM's pretrained knowledge, PaperPilot retrieves relevant information from a vector database and supplies that context to a language model to generate relevant and grounded responses.

## ✨ Key Features

- **Automated Document Ingestion:** Processes source documents through a modular ingestion pipeline.
- **Retrieval-Augmented Generation:** Combines document retrieval with LLM-powered response generation.
- **Semantic Search:** Uses vector embeddings and similarity search to retrieve relevant document chunks.
- **Context-Aware Responses:** Supplies retrieved document context to the language model.
- **PII Redaction:** Integrates Microsoft Presidio for personally identifiable information processing.
- **Prompt Injection Scanning:** Includes a scanning stage to identify potentially malicious instructions in document content.
- **Persistent Vector Storage:** Uses ChromaDB to store document embeddings for subsequent retrieval.
- **Streaming Responses:** Supports streaming generated answers through the RAG agent.
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
Embedding Generation
      ↓
ChromaDB
```

### 2. Query and Retrieval Pipeline

```text
User Query
     ↓
Query Embedding
     ↓
Semantic Retrieval
     ↓
Relevant Document Context
     ↓
LLM (Google Gemini)
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
│   └── check_models.py              # Gemini model utility
│
├── src/
│   └── paperpilot/
│       ├── agent/
│       │   └── rag_agent.py         # RAG agent implementation
│       │
│       ├── core/
│       │   ├── config.py            # Application configuration
│       │   └── logger.py            # Logging utilities
│       │
│       ├── ingestion/
│       │   ├── pipeline.py          # Ingestion pipeline
│       │   ├── loaders.py           # Document loading
│       │   ├── chunkers.py          # Chunking components
│       │   ├── chunking/
│       │   └── guardrails/
│       │
│       └── retrieval/
│           ├── embedders.py         # Embedding integration
│           ├── vector_store.py      # ChromaDB integration
│           └── hybrid_search.py     # Advanced retrieval components
│
├── tests/                           # Tests, if present
├── .env.example
├── .gitignore
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| LangChain | LLM orchestration and RAG chains |
| Google Gemini | LLM-powered response generation |
| Gemini Embeddings | Document and query vectorization |
| ChromaDB | Vector storage and similarity search |
| Microsoft Presidio | PII detection and anonymization |
| PyMuPDF | PDF document processing |
| BM25 | Keyword-based retrieval components |
| uv | Python dependency management |
| python-dotenv | Environment variable management |

## 🚀 Getting Started

### Prerequisites

- Python 3.14 or later
- [uv](https://docs.astral.sh/uv/)
- Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/DroidSammy/PaperPilot.git

cd PaperPilot
```

### 2. Set Up the Environment

Install the dependencies using the existing project configuration:

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
```

Generate an API key through [Google AI Studio](https://aistudio.google.com/).

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

The retrieval component connects to ChromaDB and retrieves relevant document chunks using semantic similarity search.

### RAG Agent

The RAG agent integrates the retriever with Google Gemini using LangChain.

It constructs a structured prompt containing the retrieved context and the user's question. The language model uses this context to generate a response.

The agent also supports streaming generated responses.

## 🔄 How It Works

| Component | Responsibility |
|---|---|
| Document Loader | Extracts content from source documents |
| PII Redactor | Identifies and redacts sensitive information |
| Injection Scanner | Scans document content for potential prompt injection |
| Chunker | Splits documents into smaller segments |
| Embedding Model | Converts text into numerical vector representations |
| ChromaDB | Stores and indexes document embeddings |
| Retriever | Finds relevant document chunks |
| RAG Agent | Combines retrieved context with the user query |
| Gemini LLM | Generates natural-language responses |

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

**Original Project Author:** Ravi Kumar

**Current Maintainer and Rebranding:** Sameer Singh

- GitHub: [DroidSammy](https://github.com/DroidSammy)
- LinkedIn: [Sameer Singh](https://www.linkedin.com/in/sameersingh07/)

PaperPilot is a rebranded and modified version of the original project, developed with permission from the original author.

---

**PaperPilot — Turn your documents into knowledge.**