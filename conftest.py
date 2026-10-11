import os
import uuid

import requests
import pytest
from requests import session


DEFAULT_BASE_URL = "https://restful-booker.herokuapp.com"
TIMEOUT = 10

def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default = os.getenv("BASE_URL", DEFAULT_BASE_URL),
        help="Base URL of the Restful-Brooker API"
    )

@pytest.fixture(scope="session")
def http():
    with requests.session() as Session:
        yield Session

@pytest.fixture(scope="session")
def base_url(request) -> str:
    return request.config.getoption("--base-url").rstrip("/")

@pytest.fixture(scope="session")
def credentials() -> dict:
    return {
        "username": os.getenv("RB_USERNAME", "admin"),
        "password": os.getenv("RB_PASSWORD", "password123")
    }

@pytest.fixture(scope="session")
def auth_token(http, base_url, credentials) -> str:
    resp = http.post(f"{base_url}/auth", json=credentials, timeout=TIMEOUT)
    assert resp.status_code == 200, f"Auth setup failed: {resp.text}"
    token = resp.json().get("token")
    assert token, f"Auth setup returned no token: {resp.text}"
    return token


# ---------------------------------------------------------------------------
# Per-test setup (default scope="function"): fresh for every test
# ---------------------------------------------------------------------------
@pytest.fixture
def booking_payload():
    """Factory for a valid booking body; override fields as needed."""

    def _make(**overrides) -> dict:
        payload = {
            "firstname": f"Test-{uuid.uuid4().hex[:8]}",
            "lastname": "Automation",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {"checkin": "2026-12-01", "checkout": "2026-12-03"},
            "additionalneeds": "Breakfast",
        }
        payload.update(overrides)
        return payload

    return _make


@pytest.fixture
def created_booking(http, base_url, auth_token, booking_payload):
    """Creates a booking before the test, deletes it after (even if the test fails)."""
    payload = booking_payload()
    resp = http.post(f"{base_url}/booking", json=payload, timeout=TIMEOUT)
    assert resp.status_code == 200, f"Booking setup failed: {resp.text}"
    booking_id = resp.json()["bookingid"]

    yield booking_id, payload

    http.delete(f"{base_url}/booking/{booking_id}",
                cookies={"token": auth_token}, timeout=TIMEOUT)

