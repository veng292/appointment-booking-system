"""
Pytest tests for the General Appointment Booking System.
Uses a temporary in-memory SQLite database so the production data is untouched.
"""
import json, sys, os, pytest

# Make sure the project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as flask_app


@pytest.fixture()
def client(tmp_path):
    """Create a test Flask client with an isolated temp database."""
    test_db = str(tmp_path / "test_bookings.db")
    flask_app.DATABASE = test_db
    flask_app.app.config["TESTING"] = True
    flask_app.init_db()
    with flask_app.app.test_client() as c:
        yield c


# ── Test 1: Home page loads ────────────────────────────────────────────────
def test_home_page_loads(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Appointment" in res.data


# ── Test 2: Available slots are returned ──────────────────────────────────
def test_slots_endpoint_returns_all_slots(client):
    res = client.get("/api/slots?service_id=doc_general&date=2025-12-01")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "all_slots" in data
    assert len(data["all_slots"]) == 7   # 7 time slots defined
    assert data["booked"] == []          # none booked yet


# ── Test 3: Valid booking succeeds ────────────────────────────────────────
def test_valid_booking_succeeds(client):
    payload = {
        "customer_name": "Test User",
        "contact_number": "9876543210",
        "service_id": "doc_general",
        "appointment_date": "2025-12-01",
        "appointment_time": "10:00 AM",
    }
    res = client.post("/api/book", json=payload)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["success"] is True
    assert data["booking"]["customer_name"] == "Test User"
    assert data["booking"]["service_name"] == "General Consultation"


# ── Test 4: Required fields validation ────────────────────────────────────
def test_missing_fields_rejected(client):
    res = client.post("/api/book", json={})
    assert res.status_code == 400
    data = json.loads(res.data)
    assert data["success"] is False

def test_invalid_contact_number(client):
    payload = {
        "customer_name": "Test User",
        "contact_number": "123",          # too short
        "service_id": "sal_haircut",
        "appointment_date": "2025-12-01",
        "appointment_time": "11:00 AM",
    }
    res = client.post("/api/book", json=payload)
    assert res.status_code == 400
    data = json.loads(res.data)
    assert data["success"] is False
    assert "10 digits" in data["error"]


# ── Test 5: Duplicate booking rejected ────────────────────────────────────
def test_duplicate_booking_rejected(client):
    payload = {
        "customer_name": "Alice",
        "contact_number": "9000000001",
        "service_id": "sal_haircut",
        "appointment_date": "2025-12-05",
        "appointment_time": "10:00 AM",
    }
    res1 = client.post("/api/book", json=payload)
    assert res1.status_code == 200

    payload2 = dict(payload)
    payload2["customer_name"] = "Bob"
    payload2["contact_number"] = "9000000002"
    res2 = client.post("/api/book", json=payload2)
    assert res2.status_code == 409
    data = json.loads(res2.data)
    assert data["success"] is False
    assert "already booked" in data["error"]


# ── Test 6: Different services can share the same time slot ───────────────
def test_different_services_same_slot_allowed(client):
    base = {"appointment_date": "2025-12-10", "appointment_time": "11:00 AM"}

    r1 = client.post("/api/book", json={**base,
        "customer_name": "User1", "contact_number": "9111111111",
        "service_id": "doc_general"})
    r2 = client.post("/api/book", json={**base,
        "customer_name": "User2", "contact_number": "9222222222",
        "service_id": "veh_oil"})

    assert json.loads(r1.data)["success"] is True
    assert json.loads(r2.data)["success"] is True


# ── Test 7: Booking saved in SQLite ───────────────────────────────────────
def test_booking_saved_in_db(client):
    import sqlite3
    payload = {
        "customer_name": "DB Test",
        "contact_number": "9800000000",
        "service_id": "veh_general",
        "appointment_date": "2025-12-15",
        "appointment_time": "02:00 PM",
    }
    res = client.post("/api/book", json=payload)
    assert res.status_code == 200

    with sqlite3.connect(flask_app.DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM bookings WHERE contact_number=?", ("9800000000",)
        ).fetchone()
    assert row is not None
    assert row["customer_name"] == "DB Test"
    assert row["service_name"] == "General Maintenance"
