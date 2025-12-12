from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.movimiento import MovimientoCreate, MovimientoRead
from app.services import movimiento_service

router = APIRouter()


@router.get("/", response_model=list[MovimientoRead])
def listar_movimientos(
    *,
    db: Session = Depends(get_db),
    fecha_desde: datetime | None = Query(None),
    fecha_hasta: datetime | None = Query(None),
    tipo: str | None = None,
    producto_id: int | None = None,
    deposito_id: int | None = None,
) -> list[MovimientoRead]:
    movimientos = movimiento_service.list_movimientos(
        db,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        tipo=tipo,
        producto_id=producto_id,
        deposito_id=deposito_id,
    )
    return [MovimientoRead.model_validate(movimiento) for movimiento in movimientos]


@router.get("/{movimiento_id}", response_model=MovimientoRead)
def obtener_movimiento(movimiento_id: int, db: Session = Depends(get_db)) -> MovimientoRead:
    movimiento = movimiento_service.get_movimiento_or_404(db, movimiento_id)
    return MovimientoRead.model_validate(movimiento)


@router.post("/", response_model=MovimientoRead, status_code=201)
def crear_movimiento(
    movimiento_in: MovimientoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> MovimientoRead:
    movimiento = movimiento_service.create_movimiento(db, movimiento_in, usuario_id=current_user.id)
    return MovimientoRead.model_validate(movimiento)
