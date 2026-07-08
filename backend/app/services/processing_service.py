from pathlib import Path

from app.parsers.exceptions import (
    EmptyDocumentError,
    CorruptedDocumentError
)

from app.parsers.parser_factory import ParserFactory


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

        return {

            "filename": path.name,

            "extension": path.suffix.lower(),

            "text": extracted_text,

            "characters": len(extracted_text),

            "words": len(extracted_text.split())

        }