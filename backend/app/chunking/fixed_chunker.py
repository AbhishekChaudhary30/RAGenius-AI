from app.chunking.chunk_models import TextChunk


class FixedChunker:

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 1000
    ):

        chunks = []

        chunk_id = 1

        for start in range(0, len(text), chunk_size):

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

                    word_count=len(
                        chunk_text.split()
                    ),

                    metadata={

                        "chunk_type": "fixed",

                        "chunk_size": chunk_size

                    }

                )

            )

            chunk_id += 1

        return chunks