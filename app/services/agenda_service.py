from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.evento import Evento


def proximos_eventos(db: Session, *, dias: int = 14) -> list[dict]:
    hoy = date.today()
    limite = hoy + timedelta(days=dias)

    eventos = (
        db.query(Evento)
        .filter(Evento.fecha_evento >= hoy)
        .filter(Evento.fecha_evento <= limite)
        .order_by(Evento.fecha_evento)
        .all()
    )

    resultados: list[dict] = []
    for evento in eventos:
        resultados.append(
            {
                "evento_id": evento.id,
                "nombre": evento.nombre,
                "fecha_evento": evento.fecha_evento,
                "hora_evento": evento.hora_evento,
                "estado": evento.estado,
                "cliente": evento.cliente.nombre if evento.cliente else None,
                "alquileres": [
                    {
                        "alquiler_id": alquiler.id,
                        "codigo": alquiler.codigo,
                        "estado": alquiler.estado,
                        "fecha_desde": alquiler.fecha_desde,
                        "fecha_hasta": alquiler.fecha_hasta,
                    }
                    for alquiler in evento.alquileres
                ],
            }
        )
    return resultados
