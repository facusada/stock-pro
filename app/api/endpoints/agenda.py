from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.services.agenda_service import proximos_eventos

router = APIRouter()


@router.get("/proximos-eventos")
def agenda_proximos_eventos(
    *,
    db: Session = Depends(get_db),
    dias: int = Query(14, ge=1, le=90),
    _: User = Depends(get_current_active_user),
) -> list[dict]:
    return proximos_eventos(db, dias=dias)
