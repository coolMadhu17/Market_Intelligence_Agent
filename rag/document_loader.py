"""
document_loader.py

Loads every markdown document from the knowledge base
and converts them into chunks.

Author : Madhu
"""

from pathlib import Path

from rag.chunker import MarkdownChunker


##############################################################################


class DocumentLoader:

    def __init__(self):

        self.chunker = MarkdownChunker()

    ##########################################################################

    def load_folder(
        self,
        folder="output/markdown"
    ):

        folder = Path(folder)

        markdown_files = sorted(
            folder.glob("*.md")
        )

        print()

        print(
            f"Found {len(markdown_files)} markdown files."
        )

        all_chunks = []

        for md_file in markdown_files:

            print(
                f"Loading {md_file.name}"
            )

            chunks = self.chunker.chunk_file(
                md_file
            )

            print(
                f"   {len(chunks)} chunks"
            )

            all_chunks.extend(chunks)

        print()

        print(
            f"Total Chunks : {len(all_chunks)}"
        )

        return all_chunks