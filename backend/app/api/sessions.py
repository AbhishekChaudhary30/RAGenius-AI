from fastapi import APIRouter

from app.memory.session_manager import SessionManager

from fastapi import HTTPException

from app.memory.memory_service import MemoryService


router = APIRouter(

    prefix="/sessions",

    tags=["Sessions"]

)


@router.get("/")
def list_sessions():

    sessions = SessionManager.list_sessions()

    response = []

    for session_id, session in sessions.items():

        response.append({

            "session_id": session_id,

            "created_at": session["created_at"],

            "updated_at": session["updated_at"],

            "message_count": session["message_count"]

        })

    response.sort(

        key=lambda x: x["updated_at"],

        reverse=True

    )

    return {

        "total_sessions": len(response),

        "sessions": response

    }
    
@router.get(
    "/{session_id}"
)
def get_session_history(

    session_id: str

):

    session = SessionManager.get_session(
        session_id
    )

    if session is None:

        raise HTTPException(

            status_code=404,

            detail="Session not found."

        )

    memory = MemoryService.get_session_data(
        session_id
    )

    return {

        "session_id": session_id,

        "created_at": session["created_at"],

        "updated_at": session["updated_at"],

        "message_count": session["message_count"],

        "summary": memory["summary"],

        "history": memory["messages"]

    }
    
@router.delete(
    "/{session_id}"
)
def delete_session(

    session_id: str

):

    session = SessionManager.get_session(
        session_id
    )

    if session is None:

        raise HTTPException(

            status_code=404,

            detail="Session not found."

        )

    MemoryService.clear_session(
        session_id
    )

    SessionManager.delete_session(
        session_id
    )

    return {

        "message": "Session deleted successfully.",

        "session_id": session_id

    }
    
@router.delete(
    "/"
)
def clear_all_sessions():

    total_sessions = len(
        SessionManager.list_sessions()
    )

    MemoryService.clear_all()

    SessionManager.clear_all()

    return {

        "message": "All sessions cleared successfully.",

        "deleted_sessions": total_sessions

    }