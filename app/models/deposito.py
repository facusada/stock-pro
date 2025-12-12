from __future__ import annotations

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Deposito(Base):
    __tablename__ = "depositos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    ubicacion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    productos = relationship("Producto", back_populates="deposito_principal")
    movimientos_origen = relationship(
        "MovimientoStock", foreign_keys="MovimientoStock.deposito_origen_id", back_populates="deposito_origen"
    )
    movimientos_destino = relationship(
        "MovimientoStock", foreign_keys="MovimientoStock.deposito_destino_id", back_populates="deposito_destino"
    )
