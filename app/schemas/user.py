from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: str = "operador"
    activo: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    nombre: str | None = None
    rol: str | None = None
    activo: bool | None = None
    password: str | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_creacion: datetime

