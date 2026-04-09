# Confluence RAG

This repository builds a Confluence knowledge-base RAG system using:
- FAISS for vector search and similarity retrieval
- Groq API for LLM generation
- Confluence REST API for page ingestion

## Setup

1. Create and activate a Python environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your Confluence and Groq credentials

## Configuration

Add the following variables to `.env`:

```env
CONFLUENCE_BASE_URL=https://your-domain.atlassian.net/wiki
CONFLUENCE_EMAIL=your-email@example.com
CONFLUENCE_API_TOKEN=your-confluence-api-token
CONFLUENCE_SPACE_KEY=YOUR_SPACE_KEY
GROQ_API_KEY=your-groq-api-key
```

## Ingest Confluence content

Run the ingest pipeline to fetch pages, chunk text, embed it, and store a FAISS index:

```bash
python run_ingest.py
```

## Query the knowledge base

Use the query script to ask questions against the indexed Confluence data:

```bash
python run_query.py
```

Or use the Streamlit chat app:

```bash
streamlit run ui.py
```

## How it works

- `run_ingest.py` pulls page content from Confluence
- `confluence_rag/chunker.py` splits text into manageable chunks
- `confluence_rag/embedder.py` encodes chunks into vectors
- `confluence_rag/store.py` writes a FAISS index and chunk metadata
- `confluence_rag/pipeline.py` retrieves the best matching chunks and sends them to Groq for answer generation
