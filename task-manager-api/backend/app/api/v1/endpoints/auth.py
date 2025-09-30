from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import AsyncSessionLocal
from ....core.models import User
from ....core.schemas import Token
from ....core.security import create_access_token, verify_password
from ....core.config import get_settings


router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    async with AsyncSessionLocal() as session:
        user = await _authenticate_user(session, form_data.username, form_data.password)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
        settings = get_settings()
        token = create_access_token(str(user.id), timedelta(minutes=settings.access_token_expires_minutes))
        return Token(access_token=token)


async def _authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user and verify_password(password, user.hashed_password):
        return user
    return None


