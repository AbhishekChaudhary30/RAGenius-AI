from app.chunking.chunk_models import TextChunk


class RecursiveChunker:

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 1000
    ):

        chunks = []

        chunk_id = 1

        separators = [

            "\n\n",

            "\n",

            ". ",

            " ",

            ""

        ]

        def split_recursively(content, separator_index):

            nonlocal chunk_id

            if len(content) <= chunk_size:

                chunks.append(

                    TextChunk(

                        chunk_id=chunk_id,

                        text=content,

                        start_index=0,

                        end_index=len(content),

                        character_count=len(content),

                        word_count=len(content.split()),

                        metadata={

                            "chunk_type": "recursive"

                        }

                    )

                )

                chunk_id += 1

                return

            if separator_index >= len(separators):

                for i in range(

                    0,

                    len(content),

                    chunk_size

                ):

                    piece = content[

                        i:i + chunk_size

                    ]

                    chunks.append(

                        TextChunk(

                            chunk_id=chunk_id,

                            text=piece,

                            start_index=i,

                            end_index=i + len(piece),

                            character_count=len(piece),

                            word_count=len(piece.split()),

                            metadata={

                                "chunk_type": "recursive"

                            }

                        )

                    )

                    chunk_id += 1

                return

            separator = separators[separator_index]

            parts = content.split(separator)

            current = ""

            for part in parts:

                candidate = (

                    part

                    if current == ""

                    else current + separator + part

                )

                if len(candidate) <= chunk_size:

                    current = candidate

                else:

                    if current:

                        split_recursively(

                            current,

                            separator_index + 1

                        )

                    current = part

            if current:

                split_recursively(

                    current,

                    separator_index + 1

                )

        split_recursively(text, 0)

        return chunks