from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connect SQLite doc
SQLALCHEMY_DATABASE_URL = "sqlite:///./documents.db"

# Engine: represents the connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session: Session for DB communication
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Main class that all model will inherit
Base = declarative_base()
