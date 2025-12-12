from __future__ import annotations

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    codigo: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    categoria: Mapped[str | None] = mapped_column(String(255), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    unidad_medida: Mapped[str] = mapped_column(String(50), nullable=False)
    tipo_vajilla: Mapped[str] = mapped_column(String(50), nullable=False)
    material: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str | None] = mapped_column(String(50))
    estado_fisico: Mapped[str] = mapped_column(String(50), nullable=False, default="Excelente")
    es_set: Mapped[bool] = mapped_column(Boolean, default=False)
    piezas_por_set: Mapped[int | None] = mapped_column(Integer)
    stock_actual: Mapped[int] = mapped_column(Integer, default=0)
    stock_minimo: Mapped[int] = mapped_column(Integer, default=0)
    stock_rentado: Mapped[int] = mapped_column(Integer, default=0)
    stock_disponible: Mapped[int] = mapped_column(Integer, default=0)
    deposito_principal_id: Mapped[int] = mapped_column(ForeignKey("depositos.id"), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    deposito_principal = relationship("Deposito", back_populates="productos")
    movimientos = relationship("MovimientoStock", back_populates="producto")
    alquiler_items = relationship("AlquilerItem", back_populates="producto")
