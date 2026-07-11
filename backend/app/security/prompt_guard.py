class PromptGuard:

    BLOCKED_PATTERNS = [

        "ignore previous instructions",
        "ignore all instructions",
        "ignore above instructions",
        "system prompt",
        "developer prompt",
        "reveal prompt",
        "show hidden prompt",
        "jailbreak",
        "bypass safety",
        "disable safety",
        "forget previous instructions",
        "act as system",
        "pretend to be system"

    ]

    @classmethod
    def is_safe(
        cls,
        text: str
    ) -> bool:

        lower = " ".join(
            text.lower().split()
        )

        for pattern in cls.BLOCKED_PATTERNS:

            if pattern in lower:

                return False

        return True