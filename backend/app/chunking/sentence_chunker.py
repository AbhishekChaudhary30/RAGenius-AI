import re

from app.chunking.chunk_models import TextChunk


class SentenceChunker:

    @staticmethod
    def chunk_text(
        text: str,
        max_chunk_size: int = 1000
    ):

        sentences = re.split(
            r'(?<=[.!?])\s+',
            text.strip()
        )

        chunks = []

        current_chunk = ""

        chunk_id = 1

        start_index = 0

        for sentence in sentences:

            if len(current_chunk) + len(sentence) <= max_chunk_size:

                if current_chunk:

                    current_chunk += " "

                current_chunk += sentence

            else:

                end_index = start_index + len(current_chunk)

                chunks.append(

                    TextChunk(

                        chunk_id=chunk_id,

                        text=current_chunk,

                        start_index=start_index,

                        end_index=end_index,

                        character_count=len(current_chunk),

                        word_count=len(current_chunk.split()),

                        metadata={

                            "chunk_type": "sentence",

                            "max_chunk_size": max_chunk_size

                        }

                    )

                )

                chunk_id += 1

                start_index = end_index

                current_chunk = sentence

        if current_chunk:

            end_index = start_index + len(current_chunk)

            chunks.append(

                TextChunk(

                    chunk_id=chunk_id,

                    text=current_chunk,

                    start_index=start_index,

                    end_index=end_index,

                    character_count=len(current_chunk),

                    word_count=len(current_chunk.split()),

                    metadata={

                        "chunk_type": "sentence",

                        "max_chunk_size": max_chunk_size

                    }

                )

            )

        return chunks