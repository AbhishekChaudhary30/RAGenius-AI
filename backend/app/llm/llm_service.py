import os

from openai import OpenAI


class LLMService:

    _client = None

    @classmethod
    def get_client(cls):

        if cls._client is None:

            cls._client = OpenAI(

                api_key=os.getenv(
                    "OPENAI_API_KEY"
                )

            )

        return cls._client