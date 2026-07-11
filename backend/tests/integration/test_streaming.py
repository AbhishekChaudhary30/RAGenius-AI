from app.services.rag_service import RAGService


def test_stream_method_exists():

    assert hasattr(
        RAGService,
        "stream"
    )

    assert hasattr(
        RAGService,
        "stream_events"
    )