from sqlalchemy.orm import Session
from . import models, schemas


def create_document(db: Session, document: schemas.DocumentCreate):
    db_document = models.Document(
        title=document.title,
        content=document.content
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

# Get docs


def get_documents(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Document).offset(skip).limit(limit).all()

# Get specific doc


def get_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()

# Update doc


def update_document(db: Session, document_id: int, updated_doc: schemas.DocumentCreate):
    db_doc = get_document(db, document_id)
    if db_doc is None:
        return None
    db_doc.title = updated_doc.title
    db_doc.content = updated_doc.content
    db.commit()
    db.refresh(db_doc)
    return db_doc

# Delete doc


def delete_document(db: Session, document_id: int):
    db_doc = get_document(db, document_id)
    if db_doc is None:
        return None
    db.delete(db_doc)
    db.commit()
    return db_doc
