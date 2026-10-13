from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.controllers import alert_controller
from app.core.database import get_db
from app.schemas.alert_schema import AlertCreate, AlertLevel, AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[AlertResponse])
def list_alerts(
    db: DbSession,
    level: AlertLevel | None = None,
    is_resolved: bool | None = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
):
    return alert_controller.list_alerts(db, level, is_resolved, skip, limit)


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(payload: AlertCreate, db: DbSession):
    return alert_controller.create_alert(db, payload)


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: DbSession):
    return alert_controller.get_alert(db, alert_id)


@router.patch("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(alert_id: int, db: DbSession):
    return alert_controller.resolve_alert(db, alert_id)


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(alert_id: int, db: DbSession):
    alert_controller.delete_alert(db, alert_id)
