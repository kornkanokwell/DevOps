from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # เช็คว่า connection ยังใช้ได้ก่อนใช้งาน
    echo=settings.environment == "development",  # log SQL queries เฉพาะ dev
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency สำหรับ FastAPI — สร้าง session ใหม่ทุก request
    และปิดเมื่อจบ
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()