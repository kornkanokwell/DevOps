from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Showtime(Base, TimestampMixin):
    __tablename__ = "showtimes"

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"))
    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id", ondelete="CASCADE"))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    movie: Mapped["Movie"] = relationship(back_populates="showtimes")  # type: ignore[name-defined]
    cinema: Mapped["Cinema"] = relationship(back_populates="showtimes")  # type: ignore[name-defined]
    bookings: Mapped[list["Booking"]] = relationship(  # type: ignore[name-defined]
        back_populates="showtime",
        cascade="all, delete-orphan",
    )