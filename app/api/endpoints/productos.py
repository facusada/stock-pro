from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.producto import Producto
from app.models.user import User
from app.schemas.producto import ProductoCreate, ProductoRead, ProductoUpdate
from app.services import producto_service

router = APIRouter()


@router.get("/", response_model=list[ProductoRead])
def listar_productos(
    *,
    db: Session = Depends(get_db),
    search: str | None = Query(None, description="Buscar por nombre o código"),
    categoria: str | None = None,
    tipo_vajilla: str | None = None,
    deposito_principal_id: int | None = None,
    stock_bajo: bool | None = Query(None, description="Solo stock bajo"),
    activo: bool | None = None,
) -> list[ProductoRead]:
    productos = producto_service.list_productos(
        db,
        search=search,
        categoria=categoria,
        tipo_vajilla=tipo_vajilla,
        deposito_principal_id=deposito_principal_id,
        stock_bajo=stock_bajo,
        activo=activo,
    )
    return [_to_read(prod) for prod in productos]


@router.get("/con-stock-bajo", response_model=list[ProductoRead])
def productos_con_stock_bajo(db: Session = Depends(get_db)) -> list[ProductoRead]:
    productos = producto_service.get_low_stock(db)
    return [_to_read(prod) for prod in productos]


@router.get("/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)) -> ProductoRead:
    producto = producto_service.get_producto_or_404(db, producto_id)
    return _to_read(producto)


@router.post("/", response_model=ProductoRead, status_code=201)
def crear_producto(
    producto_in: ProductoCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> ProductoRead:
    producto = producto_service.create_producto(db, producto_in)
    return _to_read(producto)


@router.put("/{producto_id}", response_model=ProductoRead)
def actualizar_producto(
    producto_id: int,
    producto_in: ProductoUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> ProductoRead:
    producto = producto_service.get_producto_or_404(db, producto_id)
    producto = producto_service.update_producto(db, producto, producto_in)
    return _to_read(producto)


@router.delete("/{producto_id}", response_model=ProductoRead)
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> ProductoRead:
    producto = producto_service.get_producto_or_404(db, producto_id)
    producto = producto_service.soft_delete_producto(db, producto)
    return _to_read(producto)


def _to_read(producto: Producto) -> ProductoRead:
    dto = ProductoRead.model_validate(producto)
    deposito_nombre = producto.deposito_principal.nombre if producto.deposito_principal else None
    return dto.model_copy(update={"deposito_nombre": deposito_nombre})
