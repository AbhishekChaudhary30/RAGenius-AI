import re


class InputValidator:

    MAX_QUESTION_LENGTH = 4000

    @classmethod
    def validate_question(
        cls,
        question: str
    ):
        question = question.strip()

        if not question:

            raise ValueError(
                "Question cannot be empty."
            )

        if len(question) > cls.MAX_QUESTION_LENGTH:

            raise ValueError(
                "Question is too long."
            )

        question = re.sub(
            r"\s+",
            " ",
            question
        )

        question = question.replace(
            "\x00",
            ""
        )

        return question