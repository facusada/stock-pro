from __future__ import annotations

from datetime import date, datetime, time
from pydantic import BaseModel, ConfigDict


class EventoBase(BaseModel):
    nombre: str
    fecha_evento: date
    hora_evento: time | None = None
    direccion: str | None = None
    notas: str | None = None
    cliente_id: int
    estado: str = "Pendiente"


class EventoCreate(EventoBase):
    pass


class EventoUpdate(BaseModel):
    nombre: str | None = None
    fecha_evento: date | None = None
    hora_evento: time | None = None
    direccion: str | None = None
    notas: str | None = None
    cliente_id: int | None = None
    estado: str | None = None


class EventoRead(EventoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_creacion: datetime
    cliente_nombre: str | None = None
