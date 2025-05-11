from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    approved = Column(Boolean, default=False)
