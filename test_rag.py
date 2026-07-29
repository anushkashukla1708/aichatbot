from rag.search import retrieve

query = "Tell me about your skills"

results = retrieve(query)

for doc in results:
    print("=" * 50)
    print(doc["title"])
    print(doc["text"])