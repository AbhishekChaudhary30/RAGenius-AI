from app.memory.memory_service import MemoryService


class MemorySummaryService:

    SUMMARY_TRIGGER = 8

    KEEP_LAST_MESSAGES = 4

    @classmethod
    def should_summarize(
        cls,
        session_id: str
    ) -> bool:

        return MemoryService.should_create_summary(
            session_id
        )

    @classmethod
    def build_summary_prompt(
        cls,
        session_id: str
    ) -> str:

        history = MemoryService.build_history(
            session_id
        )

        return f"""
Summarize the following conversation.

Rules:

- Keep only important information.
- Preserve technical facts.
- Preserve user preferences.
- Remove duplicate information.
- Maximum 150 words.

Conversation

{history}

Summary
"""

    @classmethod
    def finalize_summary(
        cls,
        session_id: str,
        summary: str
    ):

        MemoryService.set_summary(
            session_id,
            summary
        )

        MemoryService.trim_messages(
            session_id,
            keep_last=cls.KEEP_LAST_MESSAGES
        )