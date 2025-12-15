from __future__ import annotations

from datetime import datetime, timezone
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.movimiento import MovimientoStock
from app.models.producto import Producto
from app.schemas.movimiento import MovimientoCreate
from app.services import deposito_service

VALID_TYPES = {"INGRESO", "EGRESO", "AJUSTE", "ALQUILER", "DEVOLUCION"}


def list_movimientos(
    db: Session,
    *,
    fecha_desde: datetime | None = None,
    fecha_hasta: datetime | None = None,
    tipo: str | None = None,
    producto_id: int | None = None,
    deposito_id: int | None = None,
) -> Sequence[MovimientoStock]:
    query = db.query(MovimientoStock)

    if fecha_desde:
        query = query.filter(MovimientoStock.fecha >= fecha_desde)
    if fecha_hasta:
        query = query.filter(MovimientoStock.fecha <= fecha_hasta)
    if tipo:
        query = query.filter(MovimientoStock.tipo == tipo.upper())
    if producto_id:
        query = query.filter(MovimientoStock.producto_id == producto_id)
    if deposito_id:
        query = query.filter(
            (MovimientoStock.deposito_origen_id == deposito_id)
            | (MovimientoStock.deposito_destino_id == deposito_id)
        )

    return query.order_by(MovimientoStock.fecha.desc()).all()


def get_movimiento_or_404(db: Session, movimiento_id: int) -> MovimientoStock:
    movimiento = db.query(MovimientoStock).filter(MovimientoStock.id == movimiento_id).first()
    if not movimiento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movimiento no encontrado")
    return movimiento


def create_movimiento(
    db: Session,
    movimiento_in: MovimientoCreate,
    *,
    usuario_id: int | None = None,
    auto_commit: bool = True,
) -> MovimientoStock:
    tipo = movimiento_in.tipo.upper()
    if tipo not in VALID_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de movimiento inválido")
    if movimiento_in.cantidad <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cantidad debe ser positiva")

    producto = db.query(Producto).filter(Producto.id == movimiento_in.producto_id).with_for_update().first()
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    cantidad = movimiento_in.cantidad

    if tipo == "INGRESO":
        producto.stock_actual += cantidad
        producto.stock_disponible += cantidad
    elif tipo == "EGRESO":
        _ensure_stock(producto, cantidad)
        producto.stock_actual -= cantidad
        producto.stock_disponible -= cantidad
    elif tipo == "AJUSTE":
        if movimiento_in.ajuste_positivo is False:
            _ensure_stock(producto, cantidad)
            producto.stock_actual -= cantidad
            producto.stock_disponible = max(producto.stock_disponible - cantidad, 0)
        else:
            producto.stock_actual += cantidad
            producto.stock_disponible += cantidad
    elif tipo == "ALQUILER":
        if producto.stock_disponible < cantidad:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock insuficiente para alquiler")
        producto.stock_rentado += cantidad
        producto.stock_disponible -= cantidad
    elif tipo == "DEVOLUCION":
        if producto.stock_rentado < cantidad:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cantidad devuelta mayor al rentado")
        producto.stock_rentado -= cantidad
        producto.stock_disponible += cantidad

    max_disponible = max(producto.stock_actual - producto.stock_rentado, 0)
    producto.stock_disponible = max(min(producto.stock_disponible, max_disponible), 0)

    movimiento_data = movimiento_in.model_dump(exclude={"ajuste_positivo"})

    default_deposito_id = deposito_service.get_single_deposito_id_if_any(db)
    if default_deposito_id:
        if movimiento_data.get("deposito_origen_id") is None:
            movimiento_data["deposito_origen_id"] = default_deposito_id
        if movimiento_data.get("deposito_destino_id") is None:
            movimiento_data["deposito_destino_id"] = default_deposito_id

    movimiento_data["tipo"] = tipo
    if movimiento_data.get("fecha") is None:
        movimiento_data["fecha"] = datetime.now(timezone.utc)
    if usuario_id:
        movimiento_data["usuario_id"] = usuario_id

    movimiento = MovimientoStock(**movimiento_data)
    db.add(movimiento)
    db.add(producto)

    if auto_commit:
        db.commit()
        db.refresh(movimiento)
    else:
        db.flush()
    return movimiento


def _ensure_stock(producto: Producto, cantidad: int) -> None:
    if producto.stock_actual < cantidad or producto.stock_disponible < cantidad:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock insuficiente")
