from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.evento import Evento
from app.models.user import User
from app.schemas.evento import EventoCreate, EventoRead, EventoUpdate
from app.services import evento_service

router = APIRouter()


@router.get("/", response_model=list[EventoRead])
def listar_eventos(
    *,
    db: Session = Depends(get_db),
    estado: str | None = None,
    cliente_id: int | None = None,
    fecha_desde: date | None = Query(None),
    fecha_hasta: date | None = Query(None),
) -> list[EventoRead]:
    eventos = evento_service.list_eventos(
        db,
        estado=estado,
        cliente_id=cliente_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
    )
    return [_to_read(evento) for evento in eventos]


@router.get("/{evento_id}", response_model=EventoRead)
def obtener_evento(evento_id: int, db: Session = Depends(get_db)) -> EventoRead:
    evento = evento_service.get_evento_or_404(db, evento_id)
    return _to_read(evento)


@router.post("/", response_model=EventoRead, status_code=201)
def crear_evento(
    evento_in: EventoCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> EventoRead:
    evento = evento_service.create_evento(db, evento_in)
    return _to_read(evento)


@router.put("/{evento_id}", response_model=EventoRead)
def actualizar_evento(
    evento_id: int,
    evento_in: EventoUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> EventoRead:
    evento = evento_service.get_evento_or_404(db, evento_id)
    evento = evento_service.update_evento(db, evento, evento_in)
    return _to_read(evento)


@router.delete("/{evento_id}", status_code=204)
def eliminar_evento(
    evento_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> None:
    evento = evento_service.get_evento_or_404(db, evento_id)
    evento_service.delete_evento(db, evento)


def _to_read(evento: Evento) -> EventoRead:
    dto = EventoRead.model_validate(evento)
    cliente_nombre = evento.cliente.nombre if evento.cliente else None
    return dto.model_copy(update={"cliente_nombre": cliente_nombre})
