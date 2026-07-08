from pathlib import Path

from app.parsers.exceptions import UnsupportedFileTypeError

from app.parsers.pdf_parser import PDFParser
from app.parsers.docx_parser import DOCXParser
from app.parsers.text_parser import TextParser


class ParserFactory:

    PDF_EXTENSIONS = {
        ".pdf"
    }

    DOCX_EXTENSIONS = {
        ".docx"
    }

    TEXT_EXTENSIONS = {
        ".txt",
        ".csv",
        ".json",
        ".xml",
        ".md",
        ".py",
        ".java",
        ".js",
        ".ts",
        ".html",
        ".css",
        ".sql",
        ".yaml",
        ".yml",
        ".log",
        ".ini",
        ".cfg",
        ".toml",
        ".env"
    }

    @classmethod
    def extract_text(
        cls,
        file_path: str
    ) -> str:

        extension = Path(file_path).suffix.lower()

        if extension in cls.PDF_EXTENSIONS:
            return PDFParser.extract_text(file_path)

        if extension in cls.DOCX_EXTENSIONS:
            return DOCXParser.extract_text(file_path)

        if extension in cls.TEXT_EXTENSIONS:
            return TextParser.extract_text(file_path)

        raise UnsupportedFileTypeError(
            f"Unsupported file type: {extension}"
        )