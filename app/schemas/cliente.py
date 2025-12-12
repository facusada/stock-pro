from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class ClienteBase(BaseModel):
    nombre: str
    apellido: str | None = None
    razon_social: str | None = None
    email: EmailStr | None = None
    telefono: str | None = None
    direccion: str | None = None
    notas: str | None = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    razon_social: str | None = None
    email: EmailStr | None = None
    telefono: str | None = None
    direccion: str | None = None
    notas: str | None = None


class ClienteRead(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_creacion: datetime
