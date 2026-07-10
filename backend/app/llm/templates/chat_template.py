class ChatTemplate:

    @staticmethod
    def build() -> str:

        return """
==============================
CHAT MODE
==============================

Continue the conversation naturally.

Use previous conversation history.

Use retrieved context whenever available.

If context is missing,

say that clearly.
""".strip()