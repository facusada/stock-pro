from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class AlquilerItemBase(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: Decimal | None = None
    observaciones: str | None = None


class AlquilerItemCreate(AlquilerItemBase):
    pass


class AlquilerItemRead(AlquilerItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    producto_nombre: str | None = None


class AlquilerBase(BaseModel):
    codigo: str
    cliente_id: int
    evento_id: int | None = None
    fecha_desde: datetime
    fecha_hasta: datetime
    estado: str = "Borrador"
    notas: str | None = None


class AlquilerCreate(AlquilerBase):
    items: list[AlquilerItemCreate] = Field(default_factory=list)


class AlquilerUpdate(BaseModel):
    codigo: str | None = None
    cliente_id: int | None = None
    evento_id: int | None = None
    fecha_desde: datetime | None = None
    fecha_hasta: datetime | None = None
    estado: str | None = None
    notas: str | None = None
    items: list[AlquilerItemCreate] | None = None


class AlquilerRead(AlquilerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_creacion: datetime
    cliente_nombre: str | None = None
    evento_nombre: str | None = None
    items: list[AlquilerItemRead] = Field(default_factory=list)
