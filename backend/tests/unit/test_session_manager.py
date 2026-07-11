from app.memory.session_manager import SessionManager


def test_create_session():

    session = SessionManager.create_session()

    assert session is not None

    assert isinstance(session, str)