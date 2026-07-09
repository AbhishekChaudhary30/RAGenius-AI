from app.core.config import settings


class ProviderFactory:

    @staticmethod
    def get_provider():

        provider = settings.LLM_PROVIDER.lower()

        if provider == "ollama":

            from app.llm.providers.ollama_provider import (
                OllamaProvider
            )

            return OllamaProvider()

        elif provider == "openai":

            from app.llm.providers.openai_provider import (
                OpenAIProvider
            )

            return OpenAIProvider()

        elif provider == "groq":

            from app.llm.providers.groq_provider import (
                GroqProvider
            )

            return GroqProvider()

        elif provider == "gemini":

            from app.llm.providers.gemini_provider import (
                GeminiProvider
            )

            return GeminiProvider()

        raise ValueError(
            f"Unsupported provider: {provider}"
        )