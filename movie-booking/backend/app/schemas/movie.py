"""Pydantic schemas สำหรับ Movie"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class MovieBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    poster_url: str | None = Field(default=None, max_length=500)
    duration_minutes: int = Field(gt=0, le=600)
    genre: str = Field(min_length=1, max_length=100)
    rating: str = Field(min_length=1, max_length=10)  # G, PG, PG-13, R
    release_date: date


class MovieCreate(MovieBase):
    """ใช้ตอน POST — ทุก field จำเป็น"""


class MovieUpdate(BaseModel):
    """ใช้ตอน PATCH — ทุก field optional"""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    poster_url: str | None = Field(default=None, max_length=500)
    duration_minutes: int | None = Field(default=None, gt=0, le=600)
    genre: str | None = Field(default=None, min_length=1, max_length=100)
    rating: str | None = Field(default=None, min_length=1, max_length=10)
    release_date: date | None = None
    is_active: bool | None = None


class MovieOut(MovieBase):
    """response ส่งกลับ client"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
