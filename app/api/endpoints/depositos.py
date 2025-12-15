from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.deposito import DepositoCreate, DepositoRead, DepositoUpdate
from app.services import deposito_service

router = APIRouter()


@router.get("/", response_model=list[DepositoRead])
def listar_depositos(db: Session = Depends(get_db)) -> list[DepositoRead]:
    rows = deposito_service.list_depositos_with_counts(db)
    resultado: list[DepositoRead] = []
    for deposito, cantidad in rows:
        dto = DepositoRead.model_validate(deposito).model_copy(update={"cantidad_productos": int(cantidad)})
        resultado.append(dto)
    return resultado


@router.get("/{deposito_id}", response_model=DepositoRead)
def obtener_deposito(deposito_id: int, db: Session = Depends(get_db)) -> DepositoRead:
    deposito = deposito_service.get_deposito_or_404(db, deposito_id)
    return DepositoRead.model_validate(deposito)


@router.post("/", response_model=DepositoRead, status_code=201)
def crear_deposito(
    deposito_in: DepositoCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> DepositoRead:
    deposito = deposito_service.create_deposito(db, deposito_in)
    return DepositoRead.model_validate(deposito)


@router.put("/{deposito_id}", response_model=DepositoRead)
def actualizar_deposito(
    deposito_id: int,
    deposito_in: DepositoUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> DepositoRead:
    deposito = deposito_service.get_deposito_or_404(db, deposito_id)
    deposito = deposito_service.update_deposito(db, deposito, deposito_in)
    return DepositoRead.model_validate(deposito)


@router.delete("/{deposito_id}", response_model=DepositoRead)
def eliminar_deposito(
    deposito_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> DepositoRead:
    deposito = deposito_service.get_deposito_or_404(db, deposito_id)
    cantidad_productos = deposito_service.count_productos_for_deposito(db, deposito_id)
    dto = DepositoRead.model_validate(deposito).model_copy(update={"cantidad_productos": cantidad_productos})
    deposito_service.delete_deposito(db, deposito)
    return dto
