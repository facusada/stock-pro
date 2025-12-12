from __future__ import annotations

from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate


def get_producto_or_404(db: Session, producto_id: int) -> Producto:
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return producto


def list_productos(
    db: Session,
    *,
    search: str | None = None,
    categoria: str | None = None,
    tipo_vajilla: str | None = None,
    deposito_principal_id: int | None = None,
    stock_bajo: bool | None = None,
    activo: bool | None = None,
) -> Sequence[Producto]:
    query = db.query(Producto)

    if search:
        like = f"%{search}%"
        query = query.filter((Producto.nombre.ilike(like)) | (Producto.codigo.ilike(like)))
    if categoria:
        query = query.filter(Producto.categoria == categoria)
    if tipo_vajilla:
        query = query.filter(Producto.tipo_vajilla == tipo_vajilla)
    if deposito_principal_id:
        query = query.filter(Producto.deposito_principal_id == deposito_principal_id)
    if stock_bajo:
        query = query.filter(Producto.stock_disponible <= Producto.stock_minimo)
    if activo is not None:
        query = query.filter(Producto.activo == activo)

    return query.order_by(Producto.nombre).all()


def create_producto(db: Session, producto_in: ProductoCreate) -> Producto:
    if db.query(Producto).filter(Producto.codigo == producto_in.codigo).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Código de producto duplicado")

    data = producto_in.model_dump()
    if data.get("stock_disponible") is None:
        data["stock_disponible"] = max(data.get("stock_actual", 0) - data.get("stock_rentado", 0), 0)

    producto = Producto(**data)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def update_producto(db: Session, producto: Producto, producto_in: ProductoUpdate) -> Producto:
    update_data = producto_in.model_dump(exclude_unset=True)

    if "codigo" in update_data and update_data["codigo"] != producto.codigo:
        if db.query(Producto).filter(Producto.codigo == update_data["codigo"], Producto.id != producto.id).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Código de producto duplicado")

    for field, value in update_data.items():
        setattr(producto, field, value)

    if "stock_disponible" not in update_data:
        if {"stock_actual", "stock_rentado"} & update_data.keys():
            producto.stock_disponible = max(producto.stock_actual - producto.stock_rentado, 0)

    if producto.stock_disponible < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock disponible no puede ser negativo")

    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def soft_delete_producto(db: Session, producto: Producto) -> Producto:
    producto.activo = False
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def get_low_stock(db: Session) -> Sequence[Producto]:
    return (
        db.query(Producto)
        .filter(Producto.activo.is_(True))
        .filter(Producto.stock_disponible <= Producto.stock_minimo)
        .order_by(Producto.stock_disponible)
        .all()
    )
