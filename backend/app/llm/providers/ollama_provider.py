import os
import json
import requests

from .base_provider import BaseProvider


class OllamaProvider(BaseProvider):

    def generate(
        self,
        prompt: str
    ):

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": os.getenv(
                    "OLLAMA_MODEL",
                    "llama3.2"
                ),

                "prompt": prompt,

                "stream": False

            },

            timeout=120

        )

        response.raise_for_status()

        return response.json()["response"]

    def generate_stream(
        self,
        prompt: str
    ):

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": os.getenv(
                    "OLLAMA_MODEL",
                    "llama3.2"
                ),

                "prompt": prompt,

                "stream": True

            },

            stream=True,

            timeout=120

        )

        response.raise_for_status()

        for line in response.iter_lines():

            if not line:
                continue

            data = json.loads(
                line.decode("utf-8")
            )

            if "response" in data:

                yield data["response"]