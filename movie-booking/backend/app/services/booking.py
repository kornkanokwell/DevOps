import random
import string
from sqlalchemy.orm import Session
from app.models.booking import Booking, BookingSeat, BookingStatus
from app.models.showtime import Showtime
from app.schemas.booking import BookingCreate


def _gen_code(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def create_booking(db: Session, user_id: int, data: BookingCreate) -> Booking:
    showtime = db.get(Showtime, data.showtime_id)
    if not showtime:
        raise ValueError("ไม่พบรอบฉายนี้")

    for seat in data.seats:
        conflict = (
            db.query(BookingSeat)
            .join(Booking)
            .filter(
                BookingSeat.showtime_id == data.showtime_id,
                BookingSeat.seat_row == seat.seat_row,
                BookingSeat.seat_col == seat.seat_col,
                Booking.status != BookingStatus.CANCELLED
            )
            .first()
        )
        if conflict:
            raise ValueError(f"ที่นั่ง {seat.seat_row}{seat.seat_col} ถูกจองแล้ว")

    total = showtime.price * len(data.seats)

    while True:
        code = _gen_code()
        if not db.query(Booking).filter(Booking.booking_code == code).first():
            break

    booking = Booking(
        booking_code=code,
        user_id=user_id,
        showtime_id=data.showtime_id,
        total_price=total,
        status=BookingStatus.CONFIRMED,
    )
    db.add(booking)
    db.flush()  

    for seat in data.seats:
        db.add(
            BookingSeat(
                booking_id=booking.id,
                showtime_id=data.showtime_id,
                seat_row=seat.seat_row,
                seat_col=seat.seat_col,
            )
        )

    db.commit()
    db.refresh(booking)
    
    return booking


def get_user_bookings(db: Session, user_id: int) -> list[Booking]:
    return (
        db.query(Booking)
        .filter(Booking.user_id == user_id)
        .order_by(Booking.id.desc())
        .all()
    )