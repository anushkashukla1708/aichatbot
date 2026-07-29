import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("rag/index.faiss")

with open(
    "rag/chunks.json",
    "r",
    encoding="utf-8"
) as f:
    documents = json.load(f)
def retrieve(question):
    if not question or not str(question).strip():
        return []
    embedding = model.encode([question])


    embedding = np.array(
        embedding,
        dtype="float32"
    )

    distances, indices = index.search(
        embedding,
        top_k
    )

    results = []

    for idx in indices[0]:
        results.append(documents[idx])

    return results