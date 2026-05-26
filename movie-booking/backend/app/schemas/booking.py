from decimal import Decimal
from pydantic import BaseModel
from app.models.booking import BookingStatus


class SeatIn(BaseModel):
    seat_row: str
    seat_col: int


class BookingCreate(BaseModel):
    showtime_id: int
    seats: list[SeatIn]


class SeatOut(BaseModel):
    seat_row: str
    seat_col: int

    model_config = {"from_attributes": True}


class BookingOut(BaseModel):
    id: int
    booking_code: str
    showtime_id: int
    total_price: Decimal
    status: BookingStatus
    seats: list[SeatOut]

    model_config = {"from_attributes": True}