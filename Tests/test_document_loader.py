import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from rag.document_loader import DocumentLoader

loader = DocumentLoader()

chunks = loader.load_folder()

print()

print("Total Chunks")

print(len(chunks))

print()

print(chunks[0])