ALERT = {
    "level": "warning",
    "message": "Cảnh báo: 29A-123.45 và 51G-678.90 có nguy cơ va chạm",
    "vehicle_a_plate": "29A-123.45",
    "vehicle_b_plate": "51G-678.90",
    "ttc_seconds": 3.2,
}


def vehicle(plate: str, x: float, y: float, heading_deg: float) -> dict:
    return {"plate": plate, "x": x, "y": y, "speed_kmh": 36, "heading_deg": heading_deg}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_get_alert(client):
    created = client.post("/api/alerts", json=ALERT)
    assert created.status_code == 201
    body = created.json()
    assert body["id"] > 0
    assert body["is_resolved"] is False
    assert body["created_at"]

    fetched = client.get(f"/api/alerts/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == body


def test_list_alerts_newest_first_with_filters(client):
    client.post("/api/alerts", json=ALERT)
    danger = client.post("/api/alerts", json={**ALERT, "level": "danger"}).json()

    all_alerts = client.get("/api/alerts").json()
    assert [a["level"] for a in all_alerts] == ["danger", "warning"]

    only_danger = client.get("/api/alerts", params={"level": "danger"}).json()
    assert [a["id"] for a in only_danger] == [danger["id"]]

    client.patch(f"/api/alerts/{danger['id']}/resolve")
    unresolved = client.get("/api/alerts", params={"is_resolved": "false"}).json()
    assert [a["level"] for a in unresolved] == ["warning"]


def test_resolve_alert(client):
    alert_id = client.post("/api/alerts", json=ALERT).json()["id"]
    response = client.patch(f"/api/alerts/{alert_id}/resolve")
    assert response.status_code == 200
    assert response.json()["is_resolved"] is True


def test_delete_alert(client):
    alert_id = client.post("/api/alerts", json=ALERT).json()["id"]
    assert client.delete(f"/api/alerts/{alert_id}").status_code == 204
    assert client.get(f"/api/alerts/{alert_id}").status_code == 404


def test_missing_alert_returns_404(client):
    assert client.get("/api/alerts/999").status_code == 404
    assert client.patch("/api/alerts/999/resolve").status_code == 404
    assert client.delete("/api/alerts/999").status_code == 404


def test_invalid_alert_is_rejected(client):
    assert client.post("/api/alerts", json={**ALERT, "level": "critical"}).status_code == 422
    assert client.post("/api/alerts", json={**ALERT, "message": ""}).status_code == 422


def test_collision_check_creates_alert_when_risky(client):
    payload = {
        "vehicle_a": vehicle("29A-123.45", -15, 0, 90),
        "vehicle_b": vehicle("51G-678.90", 0, -15, 0),
    }
    response = client.post("/api/collision-events/check", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["level"] == "danger"
    assert body["alert"]["vehicle_a_plate"] == "29A-123.45"

    alerts = client.get("/api/alerts").json()
    assert [a["id"] for a in alerts] == [body["alert"]["id"]]


def test_collision_check_safe_creates_no_alert(client):
    payload = {
        "vehicle_a": vehicle("29A-123.45", -100, 0, 90),
        "vehicle_b": vehicle("51G-678.90", 0, -100, 0),
    }
    body = client.post("/api/collision-events/check", json=payload).json()
    assert body["level"] == "safe"
    assert body["alert"] is None
    assert client.get("/api/alerts").json() == []
