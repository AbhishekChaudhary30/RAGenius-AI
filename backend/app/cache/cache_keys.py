import hashlib


class CacheKeys:

    @staticmethod
    def query_key(
        question: str,
        top_k: int
    ) -> str:

        normalized = question.strip().lower()

        unique = f"{normalized}:{top_k}"

        digest = hashlib.md5(
            unique.encode()
        ).hexdigest()

        return f"rag:query:{digest}"
    
    @staticmethod
    def embedding_key(
        text: str
    ) -> str:

        return f"embedding:{hash(text)}"