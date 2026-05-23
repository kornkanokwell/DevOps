"""User response schemas"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import UserRole


class UserOut(BaseModel):
    """ส่งให้ client — ไม่มี hashed_password"""

    model_config = ConfigDict(from_attributes=True)  # อ่านจาก SQLAlchemy obj ได้

    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
