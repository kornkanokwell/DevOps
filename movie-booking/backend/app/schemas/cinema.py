"""Pydantic schemas สำหรับ Cinema"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CinemaBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    rows: int = Field(gt=0, le=26, description="จำนวนแถว (สูงสุด 26 = A-Z)")
    cols: int = Field(gt=0, le=50, description="จำนวนคอลัมน์ต่อแถว")


class CinemaCreate(CinemaBase):
    pass


class CinemaUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    rows: int | None = Field(default=None, gt=0, le=26)
    cols: int | None = Field(default=None, gt=0, le=50)


class CinemaOut(CinemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    total_seats: int  # ดึงจาก @property บน model
    created_at: datetime
