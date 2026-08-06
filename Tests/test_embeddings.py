import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from rag.document_loader import DocumentLoader
from rag.embedding_manager import EmbeddingManager

loader = DocumentLoader()

chunks = loader.load_folder()

manager = EmbeddingManager()

chunk, vector = manager.embed_chunks(chunks[:1])[0]

print()

print(chunk.company)

print()

print(len(vector))

print()

print(vector[:10])