from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so Alembic can discover them
from app.models import alquiler, cliente, deposito, evento, movimiento, producto, user  # noqa: E402,F401
