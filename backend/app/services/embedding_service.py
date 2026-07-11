from sentence_transformers import SentenceTransformer

from app.cache.redis_client import RedisClient
from app.cache.cache_keys import CacheKeys

class EmbeddingService:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            cls._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        return cls._model
      
    @classmethod
    def embed_text(
        cls,
        text: str
    ):

        cache_key = CacheKeys.embedding_key(
            text
        )

        cached_embedding = RedisClient.get_json(
            cache_key
        )

        if cached_embedding is not None:
            
            print("✅ Embedding Cache Hit")

            return cached_embedding
        
        print("❌ Embedding Cache Miss")

        model = cls.get_model()

        embedding = model.encode(
            text,
            convert_to_tensor=False
        ).tolist()

        RedisClient.set_json(

            key=cache_key,

            value=embedding,

            ttl=3600

        )

        return embedding


    @classmethod
    def embed_batch(cls, texts: list[str]):

        model = cls.get_model()

        embeddings = model.encode(

            texts,

            convert_to_numpy=True,

            normalize_embeddings=True,

            show_progress_bar=False

    )

        return embeddings.tolist()
        
    @classmethod
    def embed_chunks(cls, chunks):

        texts = []

        for chunk in chunks:

            texts.append(chunk.text)

        embeddings = cls.embed_batch(texts)

        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding
            chunk.metadata["embedding_dimension"] = len(embedding)
            chunk.metadata["embedding_model"] = "all-MiniLM-L6-v2"
        
        return chunks