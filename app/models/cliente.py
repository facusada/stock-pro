from __future__ import annotations

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    apellido: Mapped[str | None] = mapped_column(String(255))
    razon_social: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    telefono: Mapped[str | None] = mapped_column(String(50))
    direccion: Mapped[str | None] = mapped_column(String(255))
    notas: Mapped[str | None] = mapped_column(Text)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    alquileres = relationship("Alquiler", back_populates="cliente")
    eventos = relationship("Evento", back_populates="cliente")
