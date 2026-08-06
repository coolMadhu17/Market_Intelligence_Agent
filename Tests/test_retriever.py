import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from rag.retriever import MarketRetriever

retriever = MarketRetriever()

results = retriever.search(

    "factory expansion",

    k=5

)

print()

print("=" * 80)

for i, doc in enumerate(results, start=1):

    print(f"Result {i}")

    print("-" * 80)

    print(doc.metadata)

    print()

    print(doc.page_content[:500])

    print()