import os


class ProviderFactory:

    @staticmethod
    def get_provider():

        provider = os.getenv(
            "LLM_PROVIDER",
            "ollama"
        ).lower()

        if provider == "ollama":
            from app.llm.providers.ollama_provider import OllamaProvider
            return OllamaProvider()

        if provider == "openai":
            from app.llm.providers.openai_provider import OpenAIProvider
            return OpenAIProvider(
                api_key=os.getenv("OPENAI_API_KEY")
            )

        raise ValueError(
            f"Unsupported provider: {provider}"
        )