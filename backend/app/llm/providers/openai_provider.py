from openai import OpenAI

from app.core.config import settings

from .base_provider import BaseProvider


class OpenAIProvider(BaseProvider):

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.client.chat.completions.create(

            model=settings.OPENAI_MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0

        )
        
        def generate_stream(
            self,
            prompt: str
        ):

            stream = self.client.chat.completions.create(

                model="gpt-4.1-mini",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                stream=True

            )

            for chunk in stream:

                delta = chunk.choices[0].delta.content

                if delta:

                    yield delta

        return response.choices[0].message.content