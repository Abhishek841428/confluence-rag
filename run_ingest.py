from dotenv import load_dotenv

load_dotenv()

from confluence_rag.confluence_loader import fetch_pages
from confluence_rag.chunker import chunk_pages
from confluence_rag.embedder import embed
from confluence_rag.store import save_index

if __name__ == "__main__":
    print("🚀 Starting Confluence ingest...")

    pages = fetch_pages()

    if not pages:
        print("⚠️ No pages found in Confluence. Check your space key and credentials.")
        exit(1)

    chunks = chunk_pages(pages)
    print(f"🧩 Created {len(chunks)} chunks from {len(pages)} pages.")

    vectors = embed(chunks)
    save_index(vectors, chunks)

    print("✅ Confluence data indexed successfully!")