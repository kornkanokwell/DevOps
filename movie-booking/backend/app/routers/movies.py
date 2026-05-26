from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.database import get_db
from app.models import Movie, User, Showtime
from app.schemas.movie import MovieCreate, MovieOut, MovieUpdate
from app.services import movie as movie_service
from app.models.booking import Booking, BookingSeat, BookingStatus

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("", response_model=list[MovieOut])
def list_movies(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    genre: str | None = None,
) -> list[Movie]:
    return movie_service.list_movies(db, skip=skip, limit=limit, genre=genre)


@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)) -> Movie:
    return movie_service.get_movie(db, movie_id)

@router.get("/{movie_id}/showtimes")
def get_movie_showtimes(movie_id: int, db: Session = Depends(get_db)):
    showtimes = (
        db.query(Showtime)
        .filter(Showtime.movie_id == movie_id)
        .order_by(Showtime.start_time)
        .all()
    )
    
    result = []
    for s in showtimes:
        occupied_seats = (
            db.query(BookingSeat)
            .join(Booking)
            .filter(
                BookingSeat.showtime_id == s.id,
                Booking.status != BookingStatus.CANCELLED
            )
            .all()
        )
        
        booked_seats_list = [
            {"seat_row": seat.seat_row, "seat_col": seat.seat_col}
            for seat in occupied_seats
        ]
        
        result.append({
            "id": s.id,
            "movie_id": s.movie_id,
            "cinema_id": s.cinema_id,
            "start_time": s.start_time.isoformat(),
            "price": float(s.price),
            "booked_seats": booked_seats_list,
        })
        
    return result