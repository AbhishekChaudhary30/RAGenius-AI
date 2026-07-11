from app.security.input_validator import InputValidator


def test_validate_question():

    question = InputValidator.validate_question(
        "     Hello AI      "
    )

    assert question == "Hello AI"