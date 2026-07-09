from .base_provider import BaseProvider


class OllamaProvider(BaseProvider):

    def generate(
        self,
        prompt: str
    ):

        raise NotImplementedError(
            "Will implement in Step 36."
        )