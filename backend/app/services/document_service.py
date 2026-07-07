from sqlmodel import Session

from app.models.document import Document


def create_document(
    session: Session,
    filename: str,
    original_filename: str,
    uploaded_by: str,
    file_path: str,
    file_type: str,
    size: int
):

    document = Document(
        filename=filename,
        original_filename=original_filename,
        uploaded_by=uploaded_by,
        file_path=file_path,
        file_type=file_type,
        size=size
    )

    session.add(document)
    session.commit()
    session.refresh(document)

    return document