import os
import requests

from .base_provider import BaseProvider


class OllamaProvider(BaseProvider):

    def generate(
        self,
        prompt: str
    ):

        url = "http://127.0.0.1:11434/api/generate"

        payload = {
            "model": os.getenv(
                "OLLAMA_MODEL",
                "llama3.2"
            ),
            "prompt": prompt,
            "stream": False
        }

        print("=" * 80)
        print("OLLAMA REQUEST")
        print("URL:", url)
        print("MODEL:", payload["model"])
        print("PROMPT LENGTH:", len(prompt))
        print("=" * 80)

        response = requests.post(
            url,
            json=payload,
            timeout=(10, 300)
        )

        print("STATUS:", response.status_code)

        response.raise_for_status()

        data = response.json()

        print("RESPONSE RECEIVED")

        return data["response"]