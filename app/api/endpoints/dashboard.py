from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.services.dashboard_service import get_resumen

router = APIRouter()


@router.get("/resumen")
def dashboard_resumen(
    *,
    db: Session = Depends(get_db),
    dias_historial: int = Query(90, ge=1, le=180),
    top_n: int = Query(5, ge=1, le=20),
    _: User = Depends(get_current_active_user),
) -> dict:
    return get_resumen(db, dias_historial=dias_historial, top_n=top_n)
