"""
chunker.py

Reads Markdown documents and converts them into
smaller chunks suitable for embedding.

Author : Madhu
"""

from pathlib import Path
from typing import List
import hashlib
from dataclasses import dataclass, field


###############################################################################


@dataclass
class Chunk:

    id: str
    company: str
    source_file: str
    chunk_number: int
    text: str
    keyword: str = ""
    article_title: str = ""
    published: str = ""
    source: str = ""
    url: str = ""
    embedding: list = field(default_factory=list)
###############################################################################


class MarkdownChunker:

    def __init__(
        self,
        chunk_size=1000,
        overlap=800
    ):

        self.chunk_size = chunk_size

        self.overlap = overlap

    ###########################################################################

    def chunk_file(
        self,
        markdown_file
    ) -> List[Chunk]:

        markdown_file = Path(markdown_file)

        company = markdown_file.stem

        with open(
            markdown_file,
            encoding="utf-8"
        ) as f:

            text = f.read()

        return self.chunk_text(
            text,
            company,
            markdown_file.name
        )

    ###########################################################################

    def chunk_text(
        self,
        text,
        company,
        source_file
    ) -> List[Chunk]:

        chunks = []

        start = 0

        index = 1

        length = len(text)

        while start < length:

            end = min(
                start + self.chunk_size,
                length
            )

            chunk = text[start:end]
            chunk_id = hashlib.sha256(
                (       
                    company +
                    source_file +
                    chunk).encode("utf-8")).hexdigest()

            chunks.append(

                Chunk(

                    id=chunk_id,

                    company=company,

                    source_file=source_file,

                    chunk_number=index,

                    text=chunk

                )

            )

            index += 1

            start += (
                self.chunk_size -
                self.overlap
            )

        return chunks