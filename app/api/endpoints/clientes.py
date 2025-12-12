from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate
from app.services import cliente_service

router = APIRouter()


@router.get("/", response_model=list[ClienteRead])
def listar_clientes(search: str | None = Query(None, description="Buscar por nombre o email"), db: Session = Depends(get_db)) -> list[ClienteRead]:
    clientes = cliente_service.list_clientes(db, search=search)
    return [ClienteRead.model_validate(cliente) for cliente in clientes]


@router.get("/{cliente_id}", response_model=ClienteRead)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)) -> ClienteRead:
    cliente = cliente_service.get_cliente_or_404(db, cliente_id)
    return ClienteRead.model_validate(cliente)


@router.post("/", response_model=ClienteRead, status_code=201)
def crear_cliente(
    cliente_in: ClienteCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> ClienteRead:
    cliente = cliente_service.create_cliente(db, cliente_in)
    return ClienteRead.model_validate(cliente)


@router.put("/{cliente_id}", response_model=ClienteRead)
def actualizar_cliente(
    cliente_id: int,
    cliente_in: ClienteUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> ClienteRead:
    cliente = cliente_service.get_cliente_or_404(db, cliente_id)
    cliente = cliente_service.update_cliente(db, cliente, cliente_in)
    return ClienteRead.model_validate(cliente)


@router.delete("/{cliente_id}", status_code=204)
def eliminar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> None:
    cliente = cliente_service.get_cliente_or_404(db, cliente_id)
    cliente_service.delete_cliente(db, cliente)
