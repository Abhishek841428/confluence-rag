import os
import faiss
import numpy as np
import pickle

VECTOR_STORE_DIR = "vector_store"
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "index.faiss")
CHUNKS_PATH = os.path.join(VECTOR_STORE_DIR, "chunks.pkl")


def save_index(vectors, chunks):
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

    vectors = np.array(vectors, dtype="float32")
    dim = vectors.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)