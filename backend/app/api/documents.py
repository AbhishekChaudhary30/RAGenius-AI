from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.core.security import get_current_active_user
from app.models.user import User

from sqlmodel import Session
from app.database.session import get_session
from app.services.document_service import create_document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path("app/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}

MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are allowed."
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=400,
            detail="Maximum file size is 10 MB."
        )

    save_path = UPLOAD_DIR / file.filename

    with open(save_path, "wb") as f:
        f.write(contents)

    document = create_document(
        session=session,
        filename=file.filename,
        original_filename=file.filename,
        uploaded_by=current_user.email,
        file_path=str(save_path),
        file_type=extension,
        size=len(contents)
    )

    return {
        "id": document.id,
        "filename": document.filename,
        "uploaded_by": document.uploaded_by,
        "status": document.status,
        "message": "Document uploaded successfully."
    }