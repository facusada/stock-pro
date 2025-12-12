from __future__ import annotations

from datetime import date
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.evento import Evento
from app.schemas.evento import EventoCreate, EventoUpdate


def list_eventos(
    db: Session,
    *,
    estado: str | None = None,
    cliente_id: int | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
) -> Sequence[Evento]:
    query = db.query(Evento)

    if estado:
        query = query.filter(Evento.estado == estado)
    if cliente_id:
        query = query.filter(Evento.cliente_id == cliente_id)
    if fecha_desde:
        query = query.filter(Evento.fecha_evento >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Evento.fecha_evento <= fecha_hasta)

    return query.order_by(Evento.fecha_evento).all()


def get_evento_or_404(db: Session, evento_id: int) -> Evento:
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
    return evento


def create_evento(db: Session, evento_in: EventoCreate) -> Evento:
    evento = Evento(**evento_in.model_dump())
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento


def update_evento(db: Session, evento: Evento, evento_in: EventoUpdate) -> Evento:
    data = evento_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(evento, field, value)
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento


def delete_evento(db: Session, evento: Evento) -> None:
    if evento.alquileres:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Evento con alquileres asociados")
    db.delete(evento)
    db.commit()
