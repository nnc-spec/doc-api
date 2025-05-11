from fastapi import FastAPI
from app import models
from app.database import engine
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import SessionLocal
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Doc API!"}

# Bağımlılık: Her istek için DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/documents/", response_model=schemas.Document)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    return crud.create_document(db=db, document=document)


@app.get("/documents/", response_model=list[schemas.Document])
def read_documents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_documents(db, skip=skip, limit=limit)


@app.get("/documents/{document_id}", response_model=schemas.Document)
def read_document(document_id: int, db: Session = Depends(get_db)):
    db_doc = crud.get_document(db, document_id=document_id)
    if db_doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_doc


@app.put("/documents/{document_id}", response_model=schemas.Document)
def update_document(document_id: int, document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    updated = crud.update_document(db, document_id, document)
    if updated is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return updated


@app.delete("/documents/{document_id}", response_model=schemas.Document)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_document(db, document_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return deleted
