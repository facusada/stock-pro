from __future__ import annotations

from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.deposito import Deposito
from app.models.producto import Producto
from app.schemas.deposito import DepositoCreate, DepositoUpdate


def list_depositos_with_counts(db: Session) -> Sequence[tuple[Deposito, int]]:
    rows = (
        db.query(Deposito, func.count(Producto.id))
        .outerjoin(Producto, Producto.deposito_principal_id == Deposito.id)
        .group_by(Deposito.id)
        .order_by(Deposito.nombre)
        .all()
    )
    return rows


def get_deposito_or_404(db: Session, deposito_id: int) -> Deposito:
    deposito = db.query(Deposito).filter(Deposito.id == deposito_id).first()
    if not deposito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Depósito no encontrado")
    return deposito


def create_deposito(db: Session, deposito_in: DepositoCreate) -> Deposito:
    deposito = Deposito(**deposito_in.model_dump())
    db.add(deposito)
    db.commit()
    db.refresh(deposito)
    return deposito


def update_deposito(db: Session, deposito: Deposito, deposito_in: DepositoUpdate) -> Deposito:
    data = deposito_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(deposito, field, value)
    db.add(deposito)
    db.commit()
    db.refresh(deposito)
    return deposito


def delete_deposito(db: Session, deposito: Deposito) -> None:
    if deposito.productos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar un depósito con productos asociados",
        )
    db.delete(deposito)
    db.commit()
