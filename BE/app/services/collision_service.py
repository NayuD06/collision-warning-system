"""Tính nguy cơ va chạm giữa hai xe bằng điểm tiếp cận gần nhất (CPA).

Giả định hai xe giữ nguyên vận tốc. Tìm thời điểm hai xe gần nhau nhất (TTC) và
khoảng cách lúc đó; nếu khoảng cách nhỏ hơn ngưỡng an toàn thì có nguy cơ va chạm.
"""

import math
from dataclasses import dataclass

from app.utils.geo_utils import velocity_from_heading

SAFE_DISTANCE_M = 3.0
TTC_WARNING_S = 4.0
TTC_DANGER_S = 2.0
_MIN_CLOSING_SPEED = 1e-6


@dataclass(frozen=True)
class VehicleState:
    x: float
    y: float
    speed_kmh: float
    heading_deg: float


@dataclass(frozen=True)
class CollisionAssessment:
    level: str  # "safe" | "warning" | "danger"
    ttc_seconds: float | None
    min_distance_m: float | None


SAFE = CollisionAssessment(level="safe", ttc_seconds=None, min_distance_m=None)


def assess_collision(a: VehicleState, b: VehicleState) -> CollisionAssessment:
    vax, vay = velocity_from_heading(a.speed_kmh, a.heading_deg)
    vbx, vby = velocity_from_heading(b.speed_kmh, b.heading_deg)
    rx, ry = a.x - b.x, a.y - b.y
    vx, vy = vax - vbx, vay - vby

    closing_speed_sq = vx * vx + vy * vy
    if closing_speed_sq < _MIN_CLOSING_SPEED:
        return SAFE  # hai xe đứng yên so với nhau

    ttc = -(rx * vx + ry * vy) / closing_speed_sq
    if ttc < 0:
        return SAFE  # đang rời xa nhau

    min_distance = math.hypot(rx + vx * ttc, ry + vy * ttc)
    if min_distance >= SAFE_DISTANCE_M or ttc >= TTC_WARNING_S:
        return CollisionAssessment("safe", ttc, min_distance)

    level = "danger" if ttc < TTC_DANGER_S else "warning"
    return CollisionAssessment(level, ttc, min_distance)
