from sqlmodel import Session, select

from app.models.document import Document

from pathlib import Path

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

def get_user_documents(
    session: Session,
    email: str,
    page: int = 1,
    limit: int = 10
):

    offset = (page - 1) * limit

    statement = (
        select(Document)
        .where(Document.uploaded_by == email)
        .order_by(Document.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    return session.exec(statement).all()


def get_document_by_id(
    session: Session,
    document_id: int
):

    return session.get(
        Document,
        document_id
    )
    
def get_document_by_id(
    session: Session,
    document_id: int,
    email: str
):

    statement = (
        select(Document)
        .where(Document.id == document_id)
        .where(Document.uploaded_by == email)
    )

    return session.exec(statement).first()

def delete_document(
    session: Session,
    document: Document
):

    file_path = Path(document.file_path)

    if file_path.exists():
        file_path.unlink()

    session.delete(document)

    session.commit()
    
def rename_document(
    session: Session,
    document: Document,
    new_name: str
):

    document.original_filename = new_name

    session.add(document)

    session.commit()

    session.refresh(document)

    return document

def search_documents(
    session: Session,
    email: str,
    keyword: str
):

    statement = (
        select(Document)
        .where(Document.uploaded_by == email)
        .where(Document.original_filename.contains(keyword))
        .order_by(Document.created_at.desc())
    )

    return session.exec(statement).all()

def get_document_statistics(
    session: Session,
    email: str
):

    documents = session.exec(
        select(Document).where(
            Document.uploaded_by == email
        )
    ).all()

    total_documents = len(documents)

    total_size = sum(doc.size for doc in documents)

    pdf_files = sum(
        1 for doc in documents
        if doc.file_type == ".pdf"
    )

    docx_files = sum(
        1 for doc in documents
        if doc.file_type == ".docx"
    )

    txt_files = sum(
        1 for doc in documents
        if doc.file_type == ".txt"
    )

    return {
        "total_documents": total_documents,
        "total_size": total_size,
        "pdf_files": pdf_files,
        "docx_files": docx_files,
        "txt_files": txt_files
    }
    
def get_document_count(
    session: Session,
    email: str,
):

    statement = (
        select(Document)
        .where(Document.uploaded_by == email)
    )
    documents = session.exec(statement).all()

    return {
        "total_documents": len(documents)
    }