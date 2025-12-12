from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRead
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=UserRead)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> User:
    return auth_service.create_user(db, user_in)


@router.post("/login", response_model=Token)
def login_usuario(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    token = auth_service.create_user_token(user)
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_active_user)) -> User:
    return current_user
