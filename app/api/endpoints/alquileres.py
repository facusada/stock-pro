from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.alquiler import Alquiler
from app.models.user import User
from app.schemas.alquiler import AlquilerCreate, AlquilerRead, AlquilerUpdate
from app.services import alquiler_service

router = APIRouter()


@router.get("/", response_model=list[AlquilerRead])
def listar_alquileres(
    *,
    db: Session = Depends(get_db),
    cliente_id: int | None = None,
    evento_id: int | None = None,
    estado: str | None = None,
    fecha_desde: datetime | None = Query(None),
    fecha_hasta: datetime | None = Query(None),
) -> list[AlquilerRead]:
    alquileres = alquiler_service.list_alquileres(
        db,
        cliente_id=cliente_id,
        evento_id=evento_id,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
    )
    return [_to_read(alquiler) for alquiler in alquileres]


@router.get("/{alquiler_id}", response_model=AlquilerRead)
def obtener_alquiler(alquiler_id: int, db: Session = Depends(get_db)) -> AlquilerRead:
    alquiler = alquiler_service.get_alquiler_or_404(db, alquiler_id)
    return _to_read(alquiler)


@router.post("/", response_model=AlquilerRead, status_code=201)
def crear_alquiler(
    alquiler_in: AlquilerCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> AlquilerRead:
    alquiler = alquiler_service.create_alquiler(db, alquiler_in)
    return _to_read(alquiler)


@router.put("/{alquiler_id}", response_model=AlquilerRead)
def actualizar_alquiler(
    alquiler_id: int,
    alquiler_in: AlquilerUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> AlquilerRead:
    alquiler = alquiler_service.get_alquiler_or_404(db, alquiler_id)
    alquiler = alquiler_service.update_alquiler(db, alquiler, alquiler_in)
    return _to_read(alquiler)


@router.post("/{alquiler_id}/confirmar", response_model=AlquilerRead)
def confirmar_alquiler(
    alquiler_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> AlquilerRead:
    alquiler = alquiler_service.get_alquiler_or_404(db, alquiler_id)
    alquiler = alquiler_service.confirm_alquiler(db, alquiler, usuario_id=current_user.id)
    return _to_read(alquiler)


@router.post("/{alquiler_id}/registrar-devolucion", response_model=AlquilerRead)
def registrar_devolucion(
    alquiler_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> AlquilerRead:
    alquiler = alquiler_service.get_alquiler_or_404(db, alquiler_id)
    alquiler = alquiler_service.registrar_devolucion(db, alquiler, usuario_id=current_user.id)
    return _to_read(alquiler)


@router.delete("/{alquiler_id}", status_code=204)
def eliminar_alquiler(
    alquiler_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> None:
    alquiler = alquiler_service.get_alquiler_or_404(db, alquiler_id)
    alquiler_service.cancelar_alquiler(db, alquiler)


def _to_read(alquiler: Alquiler) -> AlquilerRead:
    dto = AlquilerRead.model_validate(alquiler)
    cliente_nombre = alquiler.cliente.nombre if alquiler.cliente else None
    evento_nombre = alquiler.evento.nombre if alquiler.evento else None
    return dto.model_copy(update={"cliente_nombre": cliente_nombre, "evento_nombre": evento_nombre})
