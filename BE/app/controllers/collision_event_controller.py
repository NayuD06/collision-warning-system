from sqlalchemy.orm import Session

from app.controllers import alert_controller
from app.schemas.alert_schema import AlertCreate, AlertLevel, AlertResponse
from app.schemas.collision_event_schema import (
    CollisionCheckRequest,
    CollisionCheckResponse,
    RiskLevel,
    VehicleStateIn,
)
from app.services.collision_service import VehicleState, assess_collision


def _to_state(vehicle: VehicleStateIn) -> VehicleState:
    return VehicleState(vehicle.x, vehicle.y, vehicle.speed_kmh, vehicle.heading_deg)


def check_collision(db: Session, payload: CollisionCheckRequest) -> CollisionCheckResponse:
    """Đánh giá nguy cơ va chạm; nếu có nguy cơ thì lưu luôn một cảnh báo."""
    a, b = payload.vehicle_a, payload.vehicle_b
    result = assess_collision(_to_state(a), _to_state(b))
    response = CollisionCheckResponse(
        level=RiskLevel(result.level),
        ttc_seconds=result.ttc_seconds,
        min_distance_m=result.min_distance_m,
    )
    if response.level is RiskLevel.SAFE:
        return response

    label = "NGUY HIỂM" if response.level is RiskLevel.DANGER else "Cảnh báo"
    alert = alert_controller.create_alert(
        db,
        AlertCreate(
            level=AlertLevel(result.level),
            message=(
                f"{label}: {a.plate} và {b.plate} có nguy cơ va chạm "
                f"sau {result.ttc_seconds:.1f}s"
            ),
            vehicle_a_plate=a.plate,
            vehicle_b_plate=b.plate,
            ttc_seconds=result.ttc_seconds,
        ),
    )
    response.alert = AlertResponse.model_validate(alert)
    return response
