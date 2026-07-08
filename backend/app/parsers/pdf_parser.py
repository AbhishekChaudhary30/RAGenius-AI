import fitz


class PDFParser:

    @staticmethod
    def extract_text(file_path: str) -> str:

        text = ""

        try:

            document = fitz.open(file_path)

            for page in document:

                text += page.get_text()

            document.close()

            return text.strip()

        except Exception as e:

            raise Exception(
                f"PDF Parsing Error: {str(e)}"
            )