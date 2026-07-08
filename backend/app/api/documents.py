from pathlib import Path

from app.services.processing_service import ProcessingService

from pydantic import BaseModel

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from app.core.security import get_current_active_user
from app.models.user import User

from sqlmodel import Session
from app.database.session import get_session

from fastapi.responses import FileResponse

from app.services.document_service import (
    create_document,
    get_user_documents,
    get_document_by_id,
    delete_document as delete_document_service,
    rename_document,
    search_documents,
    get_document_statistics,
    get_document_count
)


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

class RenameDocumentRequest(BaseModel):
    new_name: str

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
    
    processing_result = ProcessingService.process_document(
    str(save_path)
    )

    return {

    "id": document.id,

    "filename": document.filename,

    "uploaded_by": document.uploaded_by,

    "status": document.status,

    "processing": {

        "characters": processing_result["characters"],

        "words": processing_result["words"]

    },

    "message": "Document uploaded and processed successfully."
    }
    
@router.get("/")
def get_my_documents(

    page: int = 1,

    limit: int = 10,

    current_user: User = Depends(get_current_active_user),

    session: Session = Depends(get_session)

):

    return get_user_documents(

        session=session,

        email=current_user.email,

        page=page,

        limit=limit

    )
    
@router.get("/search")
def search_user_documents(
    keyword: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    return search_documents(
        session = session,
        email = current_user.email,
        keyword = keyword
    )

@router.get("/stats/summary")
def document_statistics(

    current_user: User = Depends(get_current_active_user),

    session: Session = Depends(get_session)

):

    return get_document_statistics(

        session=session,

        email=current_user.email

    )
    
@router.get("/count")
def document_count(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    return get_document_count(
        session = session,
        email = current_user.email
    )

@router.get("/{document_id}")
def get_document(

    document_id: int,

    current_user: User = Depends(
        get_current_active_user
    ),

    session: Session = Depends(get_session)

):

    document = get_document_by_id(

        session=session,

        document_id=document_id,

        email=current_user.email

    )

    if document is None:

        raise HTTPException(

            status_code=404,

            detail="Document not found."

        )

    return document
    
@router.put("/{document_id}/rename")
def rename_document_api(

    document_id: int,

    request: RenameDocumentRequest,

    current_user: User = Depends(get_current_active_user),

    session: Session = Depends(get_session)

):

    document = get_document_by_id(

        session=session,

        document_id=document_id,

        email=current_user.email

    )

    if document is None:

        raise HTTPException(

            status_code=404,

            detail="Document not found."

        )

    updated_document = rename_document(

        session=session,

        document=document,

        new_name=request.new_name

    )

    return {

        "message": "Document renamed successfully.",

        "document": updated_document

    }
    
@router.get("/{document_id}/download")
def download_document(

    document_id: int,

    current_user: User = Depends(
        get_current_active_user
    ),

    session: Session = Depends(get_session)

):

    document = get_document_by_id(

        session=session,

        document_id=document_id,

        email=current_user.email

    )

    if document is None:

        raise HTTPException(

            status_code=404,

            detail="Document not found."

        )

    file_path = Path(document.file_path)

    if not file_path.exists():

        raise HTTPException(

            status_code=404,

            detail="File not found on disk."

        )

    return FileResponse(

        path=file_path,

        filename=document.original_filename,

        media_type="application/octet-stream"

    )
    
@router.delete("/{document_id}")
def delete_document_api(

    document_id: int,

    current_user: User = Depends(
        get_current_active_user
    ),

    session: Session = Depends(get_session)

):

    document = get_document_by_id(

        session=session,

        document_id=document_id,

        email=current_user.email

    )

    if document is None:

        raise HTTPException(

            status_code=404,

            detail="Document not found."

        )

    delete_document_service(
        session=session,
        document=document
    )

    return {

        "message": "Document deleted successfully."

    }
    
@router.post("/{document_id}/process")
def process_document(

    document_id: int,

    current_user: User = Depends(get_current_active_user),

    session: Session = Depends(get_session)

):

    document = get_document_by_id(

        session=session,

        document_id=document_id,

        email=current_user.email

    )

    if document is None:

        raise HTTPException(

            status_code=404,

            detail="Document not found."

        )

    result = ProcessingService.process_document(

        document.file_path

    )

    return {

        "message": "Document processed successfully.",

        "processing": result

    }