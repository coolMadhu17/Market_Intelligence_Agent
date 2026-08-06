import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from rag.chunker import MarkdownChunker

chunker = MarkdownChunker()

chunks = chunker.chunk_file(
    "output/markdown/Flex.md"
)

print()

print("Chunks:", len(chunks))

print()

print(chunks[0].company)

print()

print(chunks[0].chunk_number)

print()

print(chunks[0].text[:500])