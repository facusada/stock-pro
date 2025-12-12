from __future__ import annotations

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MovimientoStock(Base):
    __tablename__ = "movimientos_stock"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"), nullable=False)
    fecha: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    deposito_origen_id: Mapped[int | None] = mapped_column(ForeignKey("depositos.id"))
    deposito_destino_id: Mapped[int | None] = mapped_column(ForeignKey("depositos.id"))
    referencia: Mapped[str | None] = mapped_column(String(255))
    observaciones: Mapped[str | None] = mapped_column(Text)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    producto = relationship("Producto", back_populates="movimientos")
    deposito_origen = relationship("Deposito", foreign_keys=[deposito_origen_id], back_populates="movimientos_origen")
    deposito_destino = relationship("Deposito", foreign_keys=[deposito_destino_id], back_populates="movimientos_destino")
    usuario = relationship("User", back_populates="movimientos")
