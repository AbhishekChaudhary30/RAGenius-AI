from sentence_transformers import SentenceTransformer


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
    def embed_text(cls, text: str):

        model = cls.get_model()

        return model.encode(
            text,
            convert_to_tensor=False
        ).tolist()


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

            chunk.metadata["embedding_dimension"] = len(
                embedding
            )
            
            chunk.metadata["embedding_model"] = "all-MiniLM-L6-v2"