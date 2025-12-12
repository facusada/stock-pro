from __future__ import annotations

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_evento: Mapped[Date] = mapped_column(Date, nullable=False)
    hora_evento: Mapped[Time | None] = mapped_column(Time(timezone=False))
    direccion: Mapped[str | None] = mapped_column(String(255))
    notas: Mapped[str | None] = mapped_column(Text)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False, default="Pendiente")
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cliente = relationship("Cliente", back_populates="eventos")
    alquileres = relationship("Alquiler", back_populates="evento")
