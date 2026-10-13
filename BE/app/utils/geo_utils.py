import math


def velocity_from_heading(speed_kmh: float, heading_deg: float) -> tuple[float, float]:
    """Đổi tốc độ (km/h) + hướng la bàn (0 = bắc, 90 = đông) thành vector vận tốc (m/s)."""
    speed_ms = speed_kmh / 3.6
    rad = math.radians(heading_deg)
    return speed_ms * math.sin(rad), speed_ms * math.cos(rad)
