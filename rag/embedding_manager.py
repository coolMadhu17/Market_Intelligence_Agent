"""
embedding_manager.py

Creates embeddings using Ollama's
nomic-embed-text model.

Author : Madhu
"""

from langchain_ollama import OllamaEmbeddings


###############################################################################


class EmbeddingManager:

    def __init__(self):

        print("Loading Embedding Model...")

        self.embedding_model = OllamaEmbeddings(
            model="nomic-embed-text:latest"
        )

        print("Embedding Model Ready")

    ###########################################################################

    def embed_text(self, text):

        """
        Generate embedding for a single text.
        """

        return self.embedding_model.embed_query(text)

    ###########################################################################

    def embed_chunk(self, chunk):

        """
        Generate embedding for one Chunk object.
        """

        return self.embedding_model.embed_query(
            chunk.text
        )

    ###########################################################################

    def embed_chunks(self, chunks):

        """
        Generate embeddings for all chunks.

        Returns:
            List[(Chunk, Embedding)]
        """

        results = []

        total = len(chunks)

        for index, chunk in enumerate(chunks, start=1):

            print(
                f"Embedding {index}/{total} : "
                f"{chunk.company} "
                f"Chunk {chunk.chunk_number}"
            )

            embedding = self.embed_chunk(chunk)

            results.append(

                (
                    chunk,
                    embedding
                )

            )

        return results