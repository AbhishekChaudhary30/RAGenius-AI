from pathlib import Path
import chardet


class TextParser:

    @staticmethod
    def extract_text(file_path: str) -> str:

        try:

            path = Path(file_path)

            raw_data = path.read_bytes()

            encoding = chardet.detect(raw_data)["encoding"]

            if encoding is None:
                encoding = "utf-8"

            text = raw_data.decode(
                encoding,
                errors="ignore"
            )

            return text.strip()

        except Exception as e:

            raise Exception(
                f"Text Parsing Error: {str(e)}"
            )