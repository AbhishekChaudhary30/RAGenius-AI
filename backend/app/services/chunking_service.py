from app.chunking.chunk_factory import ChunkFactory


class ChunkingService:

    @staticmethod
    def create_chunks(
        text: str,
        strategy: str = "recursive",
        chunk_size: int = 1000,
        overlap: int = 200
    ):

        chunks = ChunkFactory.chunk_text(

            text=text,

            strategy=strategy,

            chunk_size=chunk_size,

            overlap=overlap

        )

        return {

            "total_chunks": len(chunks),

            "strategy": strategy,

            "chunk_size": chunk_size,

            "overlap": overlap,

            "chunks": chunks

        }