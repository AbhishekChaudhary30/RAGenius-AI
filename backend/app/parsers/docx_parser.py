from docx import Document


class DOCXParser:

    @staticmethod
    def extract_text(file_path: str) -> str:

        try:

            document = Document(file_path)

            text = []

            for paragraph in document.paragraphs:

                if paragraph.text.strip():

                    text.append(paragraph.text)

            return "\n".join(text)

        except Exception as e:

            raise Exception(
                f"DOCX Parsing Error: {str(e)}"
            )