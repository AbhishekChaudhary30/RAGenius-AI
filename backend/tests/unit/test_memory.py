from app.memory.memory_service import MemoryService


def test_memory_add_message():

    session = "test-session"

    MemoryService.clear_session(session)

    MemoryService.add_message(
        session,
        "User",
        "Hello"
    )

    messages = MemoryService.get_messages(
        session
    )

    assert len(messages) == 1

    assert messages[0]["content"] == "Hello"