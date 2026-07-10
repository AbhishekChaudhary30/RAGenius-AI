from datetime import datetime
import uuid


class SessionManager:

    _sessions = {}

    @classmethod
    def create_session(cls):

        session_id = str(uuid.uuid4())

        now = datetime.utcnow().isoformat()

        cls._sessions[session_id] = {
            "created_at": now,
            "updated_at": now,
            "message_count": 0
        }

        return session_id

    @classmethod
    def get_or_create(
        cls,
        session_id: str | None
    ):

        if session_id is None:
            return cls.create_session()

        if session_id not in cls._sessions:

            now = datetime.utcnow().isoformat()

            cls._sessions[session_id] = {
                "created_at": now,
                "updated_at": now,
                "message_count": 0
            }

        return session_id

    @classmethod
    def touch(
        cls,
        session_id: str
    ):

        if session_id not in cls._sessions:
            cls.get_or_create(session_id)

        cls._sessions[session_id]["updated_at"] = datetime.utcnow().isoformat()

    @classmethod
    def increment_messages(
        cls,
        session_id: str
    ):

        cls.touch(session_id)

        cls._sessions[session_id]["message_count"] += 1

    @classmethod
    def get_session(
        cls,
        session_id: str
    ):

        return cls._sessions.get(session_id)

    @classmethod
    def list_sessions(cls):

        return cls._sessions

    @classmethod
    def delete_session(
        cls,
        session_id: str
    ):

        cls._sessions.pop(session_id, None)

    @classmethod
    def clear_all(cls):

        cls._sessions.clear()