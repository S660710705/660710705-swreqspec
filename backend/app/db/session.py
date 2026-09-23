import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base

# รองรับ CON-TECH-01 และการทดสอบ SQLite ในหน่วยความจำ
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
