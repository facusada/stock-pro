from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.alquiler import Alquiler, AlquilerItem
from app.models.deposito import Deposito
from app.models.producto import Producto


def get_resumen(db: Session, *, dias_historial: int = 90, top_n: int = 5) -> dict:
    now = datetime.now(timezone.utc)
    desde = now - timedelta(days=dias_historial)

    total_productos = db.query(func.count(Producto.id)).scalar() or 0
    stock_total = db.query(func.coalesce(func.sum(Producto.stock_actual), 0)).scalar() or 0
    cantidad_alertas_stock_bajo = (
        db.query(func.count(Producto.id)).filter(Producto.stock_disponible <= Producto.stock_minimo).scalar() or 0
    )
    cantidad_depositos = db.query(func.count(Deposito.id)).scalar() or 0
    ordenes_alquiler_activas = (
        db.query(func.count(Alquiler.id)).filter(Alquiler.estado.in_(["Confirmado", "En curso"])).scalar() or 0
    )

    productos_mas_alquilados = (
        db.query(
            Producto.id.label("producto_id"),
            Producto.nombre,
            func.coalesce(func.sum(AlquilerItem.cantidad), 0).label("total"),
        )
        .join(AlquilerItem, AlquilerItem.producto_id == Producto.id)
        .join(Alquiler, Alquiler.id == AlquilerItem.alquiler_id)
        .filter(Alquiler.fecha_desde >= desde)
        .group_by(Producto.id)
        .order_by(func.sum(AlquilerItem.cantidad).desc())
        .limit(top_n)
        .all()
    )

    productos_mayor_rotura = (
        db.query(Producto.id, Producto.nombre, Producto.estado_fisico)
        .filter(Producto.estado_fisico == "Dañado")
        .order_by(Producto.fecha_actualizacion.desc())
        .limit(top_n)
        .all()
    )

    return {
        "total_productos": total_productos,
        "stock_total": int(stock_total),
        "cantidad_alertas_stock_bajo": cantidad_alertas_stock_bajo,
        "cantidad_depositos": cantidad_depositos,
        "ordenes_alquiler_activas": ordenes_alquiler_activas,
        "productos_mas_alquilados": [
            {"producto_id": row.producto_id, "nombre": row.nombre, "total": int(row.total)}
            for row in productos_mas_alquilados
        ],
        "productos_mayor_rotura": [
            {"producto_id": row.id, "nombre": row.nombre, "estado_fisico": row.estado_fisico}
            for row in productos_mayor_rotura
        ],
    }
