"""Business logic สำหรับ Cinema"""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Cinema
from app.schemas.cinema import CinemaCreate, CinemaUpdate


def list_cinemas(db: Session) -> list[Cinema]:
    stmt = select(Cinema).order_by(Cinema.id)
    return list(db.scalars(stmt).all())


def get_cinema(db: Session, cinema_id: int) -> Cinema:
    cinema = db.get(Cinema, cinema_id)
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cinema {cinema_id} not found",
        )
    return cinema


def create_cinema(db: Session, data: CinemaCreate) -> Cinema:
    cinema = Cinema(**data.model_dump())
    db.add(cinema)
    db.commit()
    db.refresh(cinema)
    return cinema


def update_cinema(db: Session, cinema_id: int, data: CinemaUpdate) -> Cinema:
    cinema = get_cinema(db, cinema_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(cinema, key, value)
    db.commit()
    db.refresh(cinema)
    return cinema
