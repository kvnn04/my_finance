from typing import Generator
from sqlalchemy.orm import Session
from core.session import SessionLocal  # aquí importas tu sessionmaker

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
