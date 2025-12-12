from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MovimientoBase(BaseModel):
    producto_id: int
    fecha: datetime | None = None
    tipo: str
    cantidad: int
    deposito_origen_id: int | None = None
    deposito_destino_id: int | None = None
    referencia: str | None = None
    observaciones: str | None = None
    usuario_id: int | None = None


class MovimientoCreate(MovimientoBase):
    ajuste_positivo: bool | None = None


class MovimientoRead(MovimientoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha: datetime
