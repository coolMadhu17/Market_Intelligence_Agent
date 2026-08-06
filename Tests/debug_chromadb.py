from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="nomic-embed-text:latest"
)

db = Chroma(
    collection_name="market_intelligence",
    persist_directory="vector_db",
    embedding_function=embeddings
)

print("=" * 80)
print("Collection Count")
print("=" * 80)

print(db._collection.count())

print()

data = db.get()

print("=" * 80)
print("Number of Documents")
print("=" * 80)

print(len(data["ids"]))

print()

print("=" * 80)
print("First 10 Metadata Records")
print("=" * 80)

for md in data["metadatas"][:10]:
    print(md)

    data = db.get(limit=5)

for md in data["metadatas"]:
    print(repr(md["company"]))

    data = db.get()

companies = sorted(
    set(md["company"] for md in data["metadatas"])
)

print(companies)
print("Total companies:", len(companies))