import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from website import get_portfolio_data
from resume_reader import read_resume

os.makedirs("rag", exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

portfolio = get_portfolio_data()
resume = read_resume()

documents = []

# About
if "about" in portfolio:
    documents.append({
        "title": "About",
        "text": str(portfolio["about"])
    })

# Skills
if "skills" in portfolio:
    documents.append({
        "title": "Skills",
        "text": json.dumps(portfolio["skills"])
    })

# Education
if "education" in portfolio:
    documents.append({
        "title": "Education",
        "text": json.dumps(portfolio["education"])
    })

# Experience
if "experiences" in portfolio:
    documents.append({
        "title": "Experience",
        "text": json.dumps(portfolio["experiences"])
    })

# Contact
if "contact" in portfolio:
    documents.append({
        "title": "Contact",
        "text": json.dumps(portfolio["contact"])
    })

# Projects
for project in portfolio.get("projects", []):
    documents.append({
        "title": project["title"],
        "text": json.dumps(project)
    })

# Resume
documents.append({
    "title": "Resume",
    "text": resume
})

texts = [doc["text"] for doc in documents]

embeddings = model.encode(texts)

embeddings = np.array(
    embeddings,
    dtype="float32"
)

index = faiss.IndexFlatL2(
    embeddings.shape[1]
)

index.add(embeddings)

faiss.write_index(
    index,
    "rag/index.faiss"
)

with open(
    "rag/chunks.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        documents,
        f,
        indent=4
    )

print("✅ Index Built Successfully")