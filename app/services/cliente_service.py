from __future__ import annotations

from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


def list_clientes(db: Session, search: str | None = None) -> Sequence[Cliente]:
    query = db.query(Cliente)
    if search:
        like = f"%{search}%"
        query = query.filter(
            (Cliente.nombre.ilike(like)) | (Cliente.apellido.ilike(like)) | (Cliente.email.ilike(like))
        )
    return query.order_by(Cliente.nombre).all()


def get_cliente_or_404(db: Session, cliente_id: int) -> Cliente:
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente


def create_cliente(db: Session, cliente_in: ClienteCreate) -> Cliente:
    cliente = Cliente(**cliente_in.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def update_cliente(db: Session, cliente: Cliente, cliente_in: ClienteUpdate) -> Cliente:
    data = cliente_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(cliente, field, value)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def delete_cliente(db: Session, cliente: Cliente) -> None:
    if cliente.alquileres or cliente.eventos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cliente con alquileres o eventos asociados",
        )
    db.delete(cliente)
    db.commit()
