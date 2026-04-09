import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_STORE_DIR = "vector_store"
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "index.faiss")
CHUNKS_PATH = os.path.join(VECTOR_STORE_DIR, "chunks.pkl")

model = SentenceTransformer("all-MiniLM-L6-v2")


def load():
    index = faiss.read_index(INDEX_PATH)

    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


def retrieve(query, k=3):
    index, chunks = load()
    q_vec = model.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(q_vec, k)

    results = []
    for idx in indices[0]:
        if idx < 0 or idx >= len(chunks):
            continue
        results.append(chunks[idx])

    return results