from openai import OpenAI

from .base_provider import BaseProvider


class OpenAIProvider(BaseProvider):

    def __init__(
        self,
        api_key: str
    ):

        self.client = OpenAI(
            api_key=api_key
        )

    def generate(
        self,
        prompt: str
    ):

        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        return response.choices[0].message.content