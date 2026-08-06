import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from rag.document_loader import DocumentLoader
from rag.vector_store import MarketVectorStore

loader = DocumentLoader()

chunks = loader.load_folder()

store = MarketVectorStore()

store.add_chunks(chunks)

print()

print("Total Indexed Chunks")

print(store.count())