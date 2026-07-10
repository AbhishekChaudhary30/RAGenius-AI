from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate complete response.
        """
        pass

    @abstractmethod
    def generate_stream(
        self,
        prompt: str
    ):
        """
        Stream response token-by-token.
        """
        pass