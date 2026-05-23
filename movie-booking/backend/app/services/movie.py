"""Business logic สำหรับ Movie"""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Movie
from app.schemas.movie import MovieCreate, MovieUpdate


def list_movies(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    genre: str | None = None,
    only_active: bool = True,
) -> list[Movie]:
    """ดึงรายการหนัง (รองรับ pagination + filter)"""
    stmt = select(Movie)
    if only_active:
        stmt = stmt.where(Movie.is_active.is_(True))
    if genre:
        stmt = stmt.where(Movie.genre == genre)
    stmt = stmt.order_by(Movie.id.desc()).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def get_movie(db: Session, movie_id: int) -> Movie:
    """ดึงหนังตาม id; raise 404 ถ้าไม่เจอ"""
    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie {movie_id} not found",
        )
    return movie


def create_movie(db: Session, data: MovieCreate) -> Movie:
    movie = Movie(**data.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def update_movie(db: Session, movie_id: int, data: MovieUpdate) -> Movie:
    movie = get_movie(db, movie_id)
    # exclude_unset=True → update เฉพาะ field ที่ส่งมา ไม่ทับด้วย None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return movie


def soft_delete_movie(db: Session, movie_id: int) -> None:
    """ไม่ลบจริง — แค่ set is_active=False (ข้อมูล booking เก่ายังอ้างถึงได้)"""
    movie = get_movie(db, movie_id)
    movie.is_active = False
    db.commit()
