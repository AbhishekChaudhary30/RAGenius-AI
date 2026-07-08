from app.chunking.fixed_chunker import FixedChunker
from app.chunking.overlap_chunker import OverlapChunker
from app.chunking.sentence_chunker import SentenceChunker
from app.chunking.recursive_chunker import RecursiveChunker


class ChunkFactory:

    @staticmethod
    def chunk_text(
        text: str,
        strategy: str = "recursive",
        chunk_size: int = 1000,
        overlap: int = 200
    ):

        strategy = strategy.lower()

        if strategy == "fixed":

            return FixedChunker.chunk_text(
                text=text,
                chunk_size=chunk_size
            )

        elif strategy == "overlap":

            return OverlapChunker.chunk_text(
                text=text,
                chunk_size=chunk_size,
                overlap=overlap
            )

        elif strategy == "sentence":

            return SentenceChunker.chunk_text(
                text=text,
                max_chunk_size=chunk_size
            )

        elif strategy == "recursive":

            return RecursiveChunker.chunk_text(
                text=text,
                chunk_size=chunk_size
            )

        raise ValueError(
            f"Unknown chunking strategy: {strategy}"
        )