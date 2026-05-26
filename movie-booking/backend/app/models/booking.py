import enum
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Booking(Base, TimestampMixin):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    showtime_id: Mapped[int] = mapped_column(ForeignKey("showtimes.id", ondelete="CASCADE"))
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, name="booking_status"),
        default=BookingStatus.PENDING,
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="bookings")  # type: ignore[name-defined]
    showtime: Mapped["Showtime"] = relationship(back_populates="bookings")
    seats: Mapped[list["BookingSeat"]] = relationship(
        back_populates="booking",
        cascade="all, delete-orphan",
    )


class BookingSeat(Base):
    __tablename__ = "booking_seats"
    __table_args__ = (
        UniqueConstraint("showtime_id", "seat_row", "seat_col", name="uq_seat_per_showtime"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="CASCADE"))
    # denormalize showtime_id ลงมาเพื่อทำ unique constraint
    showtime_id: Mapped[int] = mapped_column(ForeignKey("showtimes.id", ondelete="CASCADE"))
    seat_row: Mapped[str] = mapped_column(String(2), nullable=False)  # A, B, C, ...
    seat_col: Mapped[int] = mapped_column(Integer, nullable=False)  # 1, 2, 3, ...

    booking: Mapped["Booking"] = relationship(back_populates="seats")