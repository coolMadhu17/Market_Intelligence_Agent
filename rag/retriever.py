"""
retriever.py

Semantic Retriever for Market Intelligence

Author : Madhu
"""

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


###############################################################################


class MarketRetriever:

    def __init__(
        self,
        persist_directory="vector_db",
        collection_name="market_intelligence",
        embedding_model="nomic-embed-text:latest"
    ):

        self.embeddings = OllamaEmbeddings(
            model=embedding_model
        )

        self.db = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )

    ###########################################################################

    def search(
        self,
        query,
        k=5
    ):

        return self.db.similarity_search(
            query,
            k=k
        )

    ###########################################################################

    def search_with_score(
        self,
        query,
        k=5
    ):

        return self.db.similarity_search_with_score(
            query,
            k=k
        )

    ###########################################################################

    def company_search(
        self,
        company,
        query,
        k=5
    ):

        return self.db.similarity_search(

            query,

            k=k,

            filter={

                "company": company

            }

        )