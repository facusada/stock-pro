from __future__ import annotations

from fastapi import APIRouter

from app.core.config import settings
from app.api.endpoints import (
    agenda,
    alquileres,
    auth,
    clientes,
    dashboard,
    depositos,
    eventos,
    movimientos,
    productos,
)

api_router = APIRouter(prefix=settings.api_prefix)

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(productos.router, prefix="/productos", tags=["productos"])
api_router.include_router(depositos.router, prefix="/depositos", tags=["depositos"])
api_router.include_router(clientes.router, prefix="/clientes", tags=["clientes"])
api_router.include_router(eventos.router, prefix="/eventos", tags=["eventos"])
api_router.include_router(alquileres.router, prefix="/alquileres", tags=["alquileres"])
api_router.include_router(movimientos.router, prefix="/movimientos", tags=["movimientos"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(agenda.router, prefix="/agenda", tags=["agenda"])
