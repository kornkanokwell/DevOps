"""Movie endpoints"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.database import get_db
from app.models import Movie, User
from app.schemas.movie import MovieCreate, MovieOut, MovieUpdate
from app.services import movie as movie_service

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("", response_model=list[MovieOut])
def list_movies(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    genre: str | None = None,
) -> list[Movie]:
    """ดึงรายการหนังที่กำลังฉาย (public)"""
    return movie_service.list_movies(db, skip=skip, limit=limit, genre=genre)


@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)) -> Movie:
    return movie_service.get_movie(db, movie_id)


@router.post("", response_model=MovieOut, status_code=status.HTTP_201_CREATED)
def create_movie(
    data: MovieCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),  # ⭐ require admin
) -> Movie:
    """เพิ่มหนังใหม่ — admin เท่านั้น"""
    return movie_service.create_movie(db, data)


@router.patch("/{movie_id}", response_model=MovieOut)
def update_movie(
    movie_id: int,
    data: MovieUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> Movie:
    """แก้ไขหนัง — admin เท่านั้น"""
    return movie_service.update_movie(db, movie_id, data)


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> None:
    """Soft delete (set is_active=False) — admin เท่านั้น"""
    movie_service.soft_delete_movie(db, movie_id)
