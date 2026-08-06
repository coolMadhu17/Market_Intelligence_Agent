"""
vector_store.py

Stores and retrieves Market Intelligence chunks
using ChromaDB.

Author : Madhu
"""

from pathlib import Path
from tracemalloc import start
from typing import List

from langchain_chroma import Chroma
from langchain_core import documents
from langchain_core import documents
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

from rag.chunker import Chunk

###############################################################################


class MarketVectorStore:

    def __init__(
        self,
        persist_directory="vector_db",
        collection_name="market_intelligence",
        embedding_model="nomic-embed-text:latest"
    ):

        self.persist_directory = persist_directory
        self.collection_name = collection_name

        Path(self.persist_directory).mkdir(
            parents=True,
            exist_ok=True
        )

        self.embeddings = OllamaEmbeddings(
            model=embedding_model
        )

        self.db = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    ###########################################################################

    def chunk_to_document(
        self,
        chunk: Chunk
    ) -> Document:
        if chunk is None:
            raise ValueError("chunk cannot be None")

        return Document(

            page_content=chunk.text,
        metadata={

                "chunk_id": chunk.id,

                "company": chunk.company,

                "source_file": chunk.source_file,

                "chunk_number": chunk.chunk_number

            }

        )

    ###########################################################################

    def get_existing_ids(self):

        data = self.db.get(include=[])

        metadatas = data.get("metadatas") or []

        ids = set()

        for md in metadatas:

            if md is None:
                continue

            if "chunk_id" in md:
                ids.add(md["chunk_id"])

        return ids

    ###########################################################################

    def add_chunks(
        self,
        chunks: List[Chunk]
    ):

        existing_ids = self.get_existing_ids()

        documents = []
        ids = []

        skipped = 0

        for chunk in chunks:

            if chunk.id in existing_ids:

                skipped += 1

                continue

            documents.append(
                self.chunk_to_document(chunk)
            )

            ids.append(chunk.id)

        print()

        print(f"Existing Chunks : {len(existing_ids)}")
        print(f"New Chunks      : {len(documents)}")
        print(f"Skipped         : {skipped}")

        if len(documents) == 0:

            print("Nothing to index.")

            return
        BATCH_SIZE = 25

        for start in range(0, len(documents), BATCH_SIZE):

            end = min(start + BATCH_SIZE, len(documents))

            batch_docs = documents[start:end]
            batch_ids = ids[start:end]

            print(
                f"Indexing {start + 1} - {end} "
                f"of {len(documents)}"
            )

            self.db.add_documents(
                documents=batch_docs,
                ids=batch_ids
        )

        print()

        print("Index Updated Successfully")

    ###########################################################################

    def similarity_search(
        self,
        query,
        k=5
    ):

        return self.db.similarity_search(

            query,

            k=k

        )

    ###########################################################################

    def similarity_search_with_score(
        self,
        query,
        k=5
    ):

        return self.db.similarity_search_with_score(

            query,

            k=k

        )

    ###########################################################################

    def count(self):

        return self.db._collection.count()

    ###########################################################################

    def clear(self):

        self.db.delete_collection()

        print("Collection Deleted")