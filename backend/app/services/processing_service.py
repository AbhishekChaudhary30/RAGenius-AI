from pathlib import Path

from app.parsers.exceptions import (
    EmptyDocumentError,
    CorruptedDocumentError
)

from app.parsers.parser_factory import ParserFactory
from app.services.chunking_service import ChunkingService

from app.services.embedding_service import EmbeddingService


class ProcessingService:

    @staticmethod
    def process_document(file_path: str):

        path = Path(file_path)

        if not path.exists():

            raise FileNotFoundError(
                "Document not found."
            )

        try:

            extracted_text = ParserFactory.extract_text(
                str(path)
            )

        except Exception as e:

            raise CorruptedDocumentError(
                str(e)
            )

        if not extracted_text.strip():

            raise EmptyDocumentError(
                "Document contains no readable text."
            )

        chunk_result = ChunkingService.create_chunks(

            text=extracted_text,

            strategy="recursive",

            chunk_size=1000,

            overlap=200

        )
        
        embedded_chunks = EmbeddingService.embed_chunks(
            chunk_result["chunks"]
        )

        return {

            "filename": path.name,

            "extension": path.suffix.lower(),

            "text": extracted_text,

            "characters": len(extracted_text),

            "words": len(extracted_text.split()),

            "total_chunks": chunk_result["total_chunks"],

            "chunk_strategy": chunk_result["strategy"],

            "chunks": embedded_chunks

        }
        
        