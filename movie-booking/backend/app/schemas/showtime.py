# app/schemas/showtime.py
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from app.schemas.booking import SeatOut  # ดึง SeatOut ที่มีอยู่แล้วมาใช้ได้เลย

class ShowtimeOut(BaseModel):
    id: int
    movie_id: int
    cinema_id: int
    start_time: datetime
    price: Decimal
    booked_seats: list[SeatOut] = []

    model_config = {"from_attributes": True}