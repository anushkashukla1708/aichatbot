import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "rag/resume.faiss"
)

with open(
    "rag/resume_chunks.json",
    encoding="utf8"
) as f:

    docs = json.load(f)


def retrieve_resume(query, top_k=2):

    emb = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    _, ids = index.search(
        emb,
        top_k
    )

    return [
        docs[i]
        for i in ids[0]
    ]