import os
import re
from fastapi import UploadFile


class FileValidator:

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt"
    }

    ALLOWED_CONTENT_TYPES = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain"
    }

    @classmethod
    def validate(
        cls,
        file: UploadFile
    ):

        filename = file.filename or ""

        extension = os.path.splitext(
            filename
        )[1].lower()

        if extension not in cls.ALLOWED_EXTENSIONS:

            raise ValueError(
                "File extension is not allowed."
            )

        if file.content_type not in cls.ALLOWED_CONTENT_TYPES:

            raise ValueError(
                "Invalid content type."
            )

        if ".." in filename:

            raise ValueError(
                "Invalid filename."
            )

        if "/" in filename or "\\" in filename:

            raise ValueError(
                "Invalid filename."
            )

        safe_name = re.sub(
            r"[^a-zA-Z0-9._-]",
            "_",
            filename
        )

        if safe_name.startswith("."):
            raise ValueError(
                "Invalid filename."
            )

        return safe_name.strip()