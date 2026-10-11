from pathlib import Path
import pytest
from utils.schema import SCHEMA_DIR, generate_schema, assert_matches_schema

SCHEMA_DIR = Path(__file__).parent.parent / "schemas"

@pytest.mark.smoke
def test_get_all_booking_id(http,base_url):
    response = http.get(f'{base_url}/booking')
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert_matches_schema(response.json(),"get_bookings")

@pytest.mark.parametrize("firstname, lastname, expected_status", [
    ("Susan", "Jackson",200),
    ("Jim", None,200),
    ("Mary", "Smith",200),
])
def test_get_all_booking_id_by_name_happy_path(http, base_url,firstname,lastname, expected_status):
    response = http.get(f'{base_url}/booking', params={"firstname": firstname,"lastname": lastname}, timeout=10)
    assert response.status_code == expected_status
    if response.json() != []:
        assert_matches_schema(response.json(), "get_bookings")

@pytest.mark.parametrize('checkin,checkout,expected_status',[
    ("2016-12-10","2020-03-05",200)
])
def test_get_all_booking_id_by_dates(http, base_url,checkin,checkout,expected_status):
    response = http.get(f'{base_url}/booking',params={'check':checkin, 'checkout':checkout},timeout=10)
    assert response.status_code == 200
    assert_matches_schema(response.json(), "get_bookings")


def test_get_bookings_by_id(http,base_url,id=1):
    response=http.get(f'{base_url}/booking/{id}')
    assert response.status_code == 200
    assert_matches_schema(response.json(), "booking")


BOOKING = {
    "firstname": "Jim",
    "lastname": "Brown",
    "totalprice": 111,
    "depositpaid": True,
    "bookingdates": {"checkin": "2018-01-01", "checkout": "2019-01-01"},
    "additionalneeds": "Breakfast",
}

@pytest.mark.parametrize("header, payload", [
    ({"Content-Type": "application/json"}, BOOKING),
])
def test_create_bookings(http,base_url,header,payload):
    resp = http.post(f'{base_url}/booking',headers=header,json=payload)
    assert resp.status_code == 200
    assert_matches_schema(resp.json(),"create_booking")

