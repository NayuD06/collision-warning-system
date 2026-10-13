import pytest

from app.services.collision_service import VehicleState, assess_collision

SPEED = 36  # km/h = 10 m/s


def crossing_pair(distance_a: float, distance_b: float):
    """Xe A chạy về hướng đông, xe B chạy về hướng bắc, cùng hướng tới gốc toạ độ."""
    a = VehicleState(x=-distance_a, y=0, speed_kmh=SPEED, heading_deg=90)
    b = VehicleState(x=0, y=-distance_b, speed_kmh=SPEED, heading_deg=0)
    return a, b


def test_danger_when_both_reach_crossing_soon():
    result = assess_collision(*crossing_pair(15, 15))
    assert result.level == "danger"
    assert result.ttc_seconds == pytest.approx(1.5)
    assert result.min_distance_m == pytest.approx(0, abs=1e-6)


def test_warning_when_crossing_is_a_few_seconds_away():
    result = assess_collision(*crossing_pair(30, 30))
    assert result.level == "warning"
    assert result.ttc_seconds == pytest.approx(3.0)


def test_safe_when_crossing_is_far_away():
    assert assess_collision(*crossing_pair(100, 100)).level == "safe"


def test_safe_when_vehicles_pass_at_different_times():
    result = assess_collision(*crossing_pair(15, 45))
    assert result.level == "safe"
    assert result.min_distance_m > 20


def test_safe_when_moving_apart():
    a = VehicleState(x=-15, y=0, speed_kmh=SPEED, heading_deg=270)
    b = VehicleState(x=0, y=-15, speed_kmh=SPEED, heading_deg=180)
    assert assess_collision(a, b).level == "safe"


def test_safe_when_same_velocity():
    a = VehicleState(x=0, y=0, speed_kmh=SPEED, heading_deg=90)
    b = VehicleState(x=-10, y=0, speed_kmh=SPEED, heading_deg=90)
    assert assess_collision(a, b).level == "safe"
