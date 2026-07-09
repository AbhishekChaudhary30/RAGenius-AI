from groq import Groq

from app.core.config import settings

from .base_provider import BaseProvider


class GroqProvider(BaseProvider):

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.client.chat.completions.create(

            model=settings.GROQ_MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0

        )

        return response.choices[0].message.content