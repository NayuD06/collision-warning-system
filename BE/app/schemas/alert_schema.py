from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class AlertLevel(StrEnum):
    WARNING = "warning"
    DANGER = "danger"


class AlertCreate(BaseModel):
    level: AlertLevel
    message: str = Field(min_length=1, max_length=255)
    vehicle_a_plate: str | None = Field(default=None, max_length=20)
    vehicle_b_plate: str | None = Field(default=None, max_length=20)
    ttc_seconds: float | None = Field(default=None, ge=0)


class AlertResponse(AlertCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_resolved: bool
    created_at: datetime
