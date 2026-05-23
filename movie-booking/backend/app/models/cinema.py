from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Cinema(Base, TimestampMixin):
    __tablename__ = "cinemas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    rows: Mapped[int] = mapped_column(Integer, nullable=False)  # จำนวนแถว (A, B, C...)
    cols: Mapped[int] = mapped_column(Integer, nullable=False)  # จำนวนคอลัมน์ (1, 2, 3...)

    showtimes: Mapped[list["Showtime"]] = relationship(  # type: ignore[name-defined]
        back_populates="cinema",
        cascade="all, delete-orphan",
    )

    @property
    def total_seats(self) -> int:
        return self.rows * self.cols