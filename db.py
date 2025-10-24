
from sqlalchemy import create_engine, Column, String, Text, Enum, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import enum
import datetime

Base = declarative_base()

class Status(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Ingestion(Base):
    __tablename__ = "ingestions"
    id = Column(String, primary_key=True)
    url = Column(Text)
    status = Column(Enum(Status))
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error = Column(Text, nullable=True)

# --- Database setup ---
DATABASE_URL = "sqlite:///rag_metadata.db"
engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
