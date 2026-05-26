from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.security import create_access_token
from app.database import get_db
from app.models.user import User
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserOut
from app.services.auth import authenticate, register_user
from app.schemas.auth import LoginRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)) -> User:
    """สมัครสมาชิก"""
    return register_user(db, data)


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:

    user = authenticate(
        db,
        LoginRequest(email=form_data.username, password=form_data.password),
    )
    token = create_access_token(subject=user.id)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
