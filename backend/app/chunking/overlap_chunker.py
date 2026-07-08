from app.chunking.chunk_models import TextChunk


class OverlapChunker:

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200
    ):

        if overlap >= chunk_size:
            raise ValueError(
                "Overlap must be smaller than chunk size."
            )

        chunks = []

        chunk_id = 1

        start = 0

        while start < len(text):

            end = min(
                start + chunk_size,
                len(text)
            )

            chunk_text = text[start:end]

            chunks.append(

                TextChunk(

                    chunk_id=chunk_id,

                    text=chunk_text,

                    start_index=start,

                    end_index=end,

                    character_count=len(chunk_text),

                    word_count=len(chunk_text.split()),

                    metadata={
                        "chunk_type": "overlap",
                        "chunk_size": chunk_size,
                        "overlap": overlap
                    }

                )

            )

            if end == len(text):
                break

            start += chunk_size - overlap

            chunk_id += 1

        return chunks