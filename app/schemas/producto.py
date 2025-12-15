from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProductoBase(BaseModel):
    nombre: str
    codigo: str
    categoria: str | None = None
    descripcion: str | None = None
    unidad_medida: str
    tipo_vajilla: str
    material: str
    color: str | None = None
    estado_fisico: str = "Excelente"
    es_set: bool = False
    piezas_por_set: int | None = None
    stock_actual: int = 0
    stock_minimo: int = 0
    deposito_principal_id: int | None = None
    activo: bool = True


class ProductoCreate(ProductoBase):
    stock_rentado: int = 0
    stock_disponible: int | None = None


class ProductoUpdate(BaseModel):
    nombre: str | None = None
    codigo: str | None = None
    categoria: str | None = None
    descripcion: str | None = None
    unidad_medida: str | None = None
    tipo_vajilla: str | None = None
    material: str | None = None
    color: str | None = None
    estado_fisico: str | None = None
    es_set: bool | None = None
    piezas_por_set: int | None = None
    stock_actual: int | None = None
    stock_minimo: int | None = None
    stock_rentado: int | None = None
    stock_disponible: int | None = None
    deposito_principal_id: int | None = None
    activo: bool | None = None


class ProductoRead(ProductoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    deposito_principal_id: int
    stock_rentado: int
    stock_disponible: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    deposito_nombre: str | None = None
