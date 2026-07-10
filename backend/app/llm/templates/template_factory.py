from app.llm.templates.qa_template import (
    QATemplate
)

from app.llm.templates.chat_template import (
    ChatTemplate
)

from app.llm.templates.summary_template import (
    SummaryTemplate
)


class TemplateFactory:

    QA = "qa"

    CHAT = "chat"

    SUMMARY = "summary"

    @classmethod
    def get_template(

        cls,

        template_type: str

    ) -> str:

        template_type = template_type.lower()

        if template_type == cls.QA:

            return QATemplate.build()

        if template_type == cls.CHAT:

            return ChatTemplate.build()

        if template_type == cls.SUMMARY:

            return SummaryTemplate.build()

        raise ValueError(

            f"Unsupported template: {template_type}"

        )