import pytest
from dashboard.routes import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_status_endpoint(client):
    res = client.get("/api/status")
    assert res.status_code == 200
    data = res.get_json()
    assert "lane_counts" in data
    assert "override" in data

def test_incidents_endpoint(client):
    res = client.get("/api/incidents")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_officers_endpoint(client):
    res = client.get("/api/officers")
    assert res.status_code == 200
    officers = res.get_json()
    assert isinstance(officers, list)
    if officers:
        assert "name" in officers[0]

def test_logs_endpoint(client):
    res = client.get("/api/logs")
    assert res.status_code == 200
    logs = res.get_json()
    assert isinstance(logs, list)
    if logs:
        assert "timestamp" in logs[0]

def test_recommendation_endpoint(client):
    res = client.get("/api/recommendation")
    assert res.status_code == 200
    data = res.get_json()
    assert "lane" in data
    assert "count" in data

def test_override_toggle(client):
    # Activate override
    res1 = client.post("/api/override", json={"enabled": True, "lane": "east"})
    assert res1.status_code == 200
    data1 = res1.get_json()
    assert data1["new_state"]["manual_override"] == True

    # Deactivate override
    res2 = client.post("/api/override", json={"enabled": False, "lane": "east"})
    assert res2.status_code == 200
    data2 = res2.get_json()
    assert data2["new_state"]["manual_override"] == False

def test_simulate_violation(client):
    res = client.post("/api/simulate_violation")
    assert res.status_code == 200
    data = res.get_json()
    assert "lane" in data
    assert data["lane"] in ["north", "south", "east", "west"]

def test_export_report(client):
    res = client.get("/api/export_report")
    assert res.status_code == 200
    assert res.content_type.startswith("text/csv")


def test_status_reflects_override(client):
    client.post("/api/override", json={"enabled": True, "lane": "south"})
    res = client.get("/api/status")
    data = res.get_json()
    assert data["override"]["manual_override"] == True
    assert data["override"]["forced_lane"] == "south"

def test_override_deactivation(client):
    client.post("/api/override", json={"enabled": False, "lane": "south"})
    res = client.get("/api/status")
    data = res.get_json()
    assert data["override"]["manual_override"] is False
    assert data["override"]["forced_lane"] is None
