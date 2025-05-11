from pydantic import BaseModel


class DocumentBase(BaseModel):
    title: str
    content: str


class DocumentCreate(DocumentBase):
    pass


class Document(DocumentBase):
    id: int
    approved: bool

    class Config:
        orm_mode = True
