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

    def generate_stream(
        self,
        prompt: str
    ):

        stream = self.client.chat.completions.create(

            model=settings.GROQ_MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0,

            stream=True

        )

        for chunk in stream:

            if (
                chunk.choices
                and chunk.choices[0].delta.content
            ):
                yield chunk.choices[0].delta.content