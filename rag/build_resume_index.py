import os
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from resume_reader import read_resume
from website import get_portfolio_data

os.makedirs("rag", exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

resume = read_resume()

# Split resume into paragraphs
chunks = [
    x.strip()
    for x in resume.split("\n\n")
    if x.strip()
]

documents = []

for i, chunk in enumerate(chunks):

    documents.append(
        {
            "title": f"Resume Chunk {i+1}",
            "text": chunk
        }
    )

texts = [x["text"] for x in documents]

embeddings = model.encode(
    texts,
    convert_to_numpy=True
).astype("float32")

index = faiss.IndexFlatL2(
    embeddings.shape[1]
)

index.add(embeddings)

faiss.write_index(
    index,
    "rag/resume.faiss"
)

with open(
    "rag/resume_chunks.json",
    "w",
    encoding="utf8"
) as f:

    json.dump(
        documents,
        f,
        indent=4
    )

print("✅ Resume Index Built")