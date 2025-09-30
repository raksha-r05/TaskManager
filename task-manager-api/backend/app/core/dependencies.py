from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db


DbSession = Annotated[AsyncSession, Depends(get_db)]


