from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.schemas.alert_schema import AlertCreate, AlertLevel


def list_alerts(
    db: Session,
    level: AlertLevel | None = None,
    is_resolved: bool | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[Alert]:
    query = select(Alert).order_by(Alert.id.desc())
    if level is not None:
        query = query.where(Alert.level == level.value)
    if is_resolved is not None:
        query = query.where(Alert.is_resolved == is_resolved)
    return list(db.scalars(query.offset(skip).limit(limit)))


def get_alert(db: Session, alert_id: int) -> Alert:
    alert = db.get(Alert, alert_id)
    if alert is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Không tìm thấy cảnh báo")
    return alert


def create_alert(db: Session, payload: AlertCreate) -> Alert:
    alert = Alert(**payload.model_dump(mode="json"))
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def resolve_alert(db: Session, alert_id: int) -> Alert:
    alert = get_alert(db, alert_id)
    alert.is_resolved = True
    db.commit()
    return alert


def delete_alert(db: Session, alert_id: int) -> None:
    db.delete(get_alert(db, alert_id))
    db.commit()
