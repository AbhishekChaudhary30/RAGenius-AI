import google.generativeai as genai

from app.core.config import settings

from .base_provider import BaseProvider


class GeminiProvider(BaseProvider):

    def __init__(self):

        genai.configure(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = genai.GenerativeModel(
            settings.GEMINI_MODEL
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.model.generate_content(
            prompt
        )

        return response.text