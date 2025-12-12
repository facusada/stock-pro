from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DepositoBase(BaseModel):
    nombre: str
    ubicacion: str | None = None
    descripcion: str | None = None


class DepositoCreate(DepositoBase):
    pass


class DepositoUpdate(BaseModel):
    nombre: str | None = None
    ubicacion: str | None = None
    descripcion: str | None = None


class DepositoRead(DepositoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_creacion: datetime
    cantidad_productos: int | None = None
