from __future__ import annotations

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Alquiler(Base):
    __tablename__ = "alquileres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    evento_id: Mapped[int | None] = mapped_column(ForeignKey("eventos.id"))
    fecha_desde: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    fecha_hasta: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False, default="Borrador")
    notas: Mapped[str | None] = mapped_column(Text)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cliente = relationship("Cliente", back_populates="alquileres")
    evento = relationship("Evento", back_populates="alquileres")
    items = relationship("AlquilerItem", back_populates="alquiler", cascade="all, delete-orphan")


class AlquilerItem(Base):
    __tablename__ = "alquiler_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    alquiler_id: Mapped[int] = mapped_column(ForeignKey("alquileres.id"), nullable=False)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[float | None] = mapped_column(Numeric(10, 2))
    observaciones: Mapped[str | None] = mapped_column(Text)

    alquiler = relationship("Alquiler", back_populates="items")
    producto = relationship("Producto", back_populates="alquiler_items")
