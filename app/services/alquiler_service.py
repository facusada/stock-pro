from __future__ import annotations

from datetime import datetime
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.alquiler import Alquiler, AlquilerItem
from app.schemas.alquiler import AlquilerCreate, AlquilerUpdate
from app.schemas.movimiento import MovimientoCreate
from app.services.movimiento_service import create_movimiento


def list_alquileres(
    db: Session,
    *,
    cliente_id: int | None = None,
    evento_id: int | None = None,
    estado: str | None = None,
    fecha_desde: datetime | None = None,
    fecha_hasta: datetime | None = None,
) -> Sequence[Alquiler]:
    query = db.query(Alquiler)

    if cliente_id:
        query = query.filter(Alquiler.cliente_id == cliente_id)
    if evento_id:
        query = query.filter(Alquiler.evento_id == evento_id)
    if estado:
        query = query.filter(Alquiler.estado == estado)
    if fecha_desde:
        query = query.filter(Alquiler.fecha_desde >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Alquiler.fecha_hasta <= fecha_hasta)

    return query.order_by(Alquiler.fecha_desde.desc()).all()


def get_alquiler_or_404(db: Session, alquiler_id: int) -> Alquiler:
    alquiler = db.query(Alquiler).filter(Alquiler.id == alquiler_id).first()
    if not alquiler:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alquiler no encontrado")
    return alquiler


def create_alquiler(db: Session, alquiler_in: AlquilerCreate) -> Alquiler:
    if db.query(Alquiler).filter(Alquiler.codigo == alquiler_in.codigo).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Código de alquiler duplicado")
    if alquiler_in.estado != "Borrador":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden crear alquileres en borrador; use /confirmar para avanzar",
        )

    items = [AlquilerItem(**item.model_dump()) for item in alquiler_in.items]
    alquiler = Alquiler(
        codigo=alquiler_in.codigo,
        cliente_id=alquiler_in.cliente_id,
        evento_id=alquiler_in.evento_id,
        fecha_desde=alquiler_in.fecha_desde,
        fecha_hasta=alquiler_in.fecha_hasta,
        estado=alquiler_in.estado,
        notas=alquiler_in.notas,
        items=items,
    )
    db.add(alquiler)
    db.commit()
    db.refresh(alquiler)
    return alquiler


def update_alquiler(db: Session, alquiler: Alquiler, alquiler_in: AlquilerUpdate) -> Alquiler:
    data = alquiler_in.model_dump(exclude_unset=True)
    items_payload = data.pop("items", None)

    for field, value in data.items():
        setattr(alquiler, field, value)

    if items_payload is not None:
        alquiler.items.clear()
        for item in items_payload:
            alquiler.items.append(AlquilerItem(**item))

    db.add(alquiler)
    db.commit()
    db.refresh(alquiler)
    return alquiler


def confirm_alquiler(db: Session, alquiler: Alquiler, usuario_id: int | None = None) -> Alquiler:
    if alquiler.estado != "Borrador":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El alquiler ya fue confirmado")
    if not alquiler.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El alquiler no tiene ítems")

    for item in alquiler.items:
        movimiento = MovimientoCreate(
            producto_id=item.producto_id,
            tipo="ALQUILER",
            cantidad=item.cantidad,
            referencia=alquiler.codigo,
        )
        create_movimiento(db, movimiento, usuario_id=usuario_id, auto_commit=False)

    alquiler.estado = "Confirmado"
    db.add(alquiler)
    db.commit()
    db.refresh(alquiler)
    return alquiler


def registrar_devolucion(db: Session, alquiler: Alquiler, usuario_id: int | None = None) -> Alquiler:
    if alquiler.estado not in {"Confirmado", "En curso"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Solo alquileres activos pueden devolverse")
    if not alquiler.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El alquiler no tiene ítems")

    for item in alquiler.items:
        movimiento = MovimientoCreate(
            producto_id=item.producto_id,
            tipo="DEVOLUCION",
            cantidad=item.cantidad,
            referencia=f"DEV-{alquiler.codigo}",
        )
        create_movimiento(db, movimiento, usuario_id=usuario_id, auto_commit=False)

    alquiler.estado = "Finalizado"
    db.add(alquiler)
    db.commit()
    db.refresh(alquiler)
    return alquiler


def cancelar_alquiler(db: Session, alquiler: Alquiler) -> None:
    if alquiler.estado != "Borrador":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Solo borradores pueden eliminarse")
    db.delete(alquiler)
    db.commit()
