from enum import StrEnum

from pydantic import BaseModel, Field

from app.schemas.alert_schema import AlertResponse


class RiskLevel(StrEnum):
    SAFE = "safe"
    WARNING = "warning"
    DANGER = "danger"


class VehicleStateIn(BaseModel):
    """Trạng thái tức thời của một xe trên mặt phẳng (đơn vị mét)."""

    plate: str = Field(min_length=1, max_length=20)
    x: float
    y: float
    speed_kmh: float = Field(ge=0, le=300)
    heading_deg: float = Field(ge=0, lt=360, description="0 = hướng bắc (+y), 90 = hướng đông (+x)")


class CollisionCheckRequest(BaseModel):
    vehicle_a: VehicleStateIn
    vehicle_b: VehicleStateIn


class CollisionCheckResponse(BaseModel):
    level: RiskLevel
    ttc_seconds: float | None
    min_distance_m: float | None
    alert: AlertResponse | None = None
