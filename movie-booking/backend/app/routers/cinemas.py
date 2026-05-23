"""Cinema endpoints"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.database import get_db
from app.models import Cinema, User
from app.schemas.cinema import CinemaCreate, CinemaOut, CinemaUpdate
from app.services import cinema as cinema_service

router = APIRouter(prefix="/cinemas", tags=["Cinemas"])


@router.get("", response_model=list[CinemaOut])
def list_cinemas(db: Session = Depends(get_db)) -> list[Cinema]:
    return cinema_service.list_cinemas(db)


@router.get("/{cinema_id}", response_model=CinemaOut)
def get_cinema(cinema_id: int, db: Session = Depends(get_db)) -> Cinema:
    return cinema_service.get_cinema(db, cinema_id)


@router.post("", response_model=CinemaOut, status_code=status.HTTP_201_CREATED)
def create_cinema(
    data: CinemaCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> Cinema:
    return cinema_service.create_cinema(db, data)


@router.patch("/{cinema_id}", response_model=CinemaOut)
def update_cinema(
    cinema_id: int,
    data: CinemaUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> Cinema:
    return cinema_service.update_cinema(db, cinema_id, data)
