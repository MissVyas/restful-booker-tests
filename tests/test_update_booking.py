import pytest

TIMEOUT = 10


# --- Happy paths -------------------------------------------------------------
@pytest.mark.smoke
def test_update_booking_with_token(http, base_url, auth_token, created_booking, booking_payload):
    booking_id, _ = created_booking
    new_data = booking_payload(firstname="Updated", totalprice=999, depositpaid=False)

    resp = http.put(f"{base_url}/booking/{booking_id}", json=new_data,
                    cookies={"token": auth_token}, timeout=TIMEOUT)

    assert resp.status_code == 200, resp.text
    assert resp.json() == new_data


def test_update_is_persisted(http, base_url, auth_token, created_booking, booking_payload):
    """The PUT response could lie; a fresh GET proves the change was saved."""
    booking_id, _ = created_booking
    new_data = booking_payload(lastname="Persisted")

    http.put(f"{base_url}/booking/{booking_id}", json=new_data,
             cookies={"token": auth_token}, timeout=TIMEOUT)
    fetched = http.get(f"{base_url}/booking/{booking_id}", timeout=TIMEOUT)

    assert fetched.status_code == 200, fetched.text
    assert fetched.json() == new_data


def test_update_booking_with_basic_auth(http, base_url, credentials, created_booking, booking_payload):
    booking_id, _ = created_booking
    new_data = booking_payload(firstname="BasicAuth")

    resp = http.put(f"{base_url}/booking/{booking_id}", json=new_data,
                    auth=(credentials["username"], credentials["password"]), timeout=TIMEOUT)

    assert resp.status_code == 200, resp.text
    assert resp.json()["firstname"] == "BasicAuth"


# --- Auth failures -------------------------------------------------------------

@pytest.mark.parametrize("cookies", [
    pytest.param(None, id="no-token"),
    pytest.param({"token": "invalidtoken123"}, id="invalid-token"),
    pytest.param({"token": ""}, id="empty-token"),
])
def test_update_without_valid_auth_is_forbidden(http, base_url, created_booking, booking_payload, cookies):
    booking_id, original = created_booking

    resp = http.put(f"{base_url}/booking/{booking_id}", json=booking_payload(firstname="Hacked"),
                    cookies=cookies, timeout=TIMEOUT)
    assert resp.status_code == 403, resp.text

    # and nothing changed
    fetched = http.get(f"{base_url}/booking/{booking_id}", timeout=TIMEOUT).json()
    assert fetched == original


# --- Bad input -----------------------------------------------------------------

def test_update_nonexistent_booking(http, base_url, auth_token, booking_payload):
    resp = http.put(f"{base_url}/booking/999999999", json=booking_payload(),
                    cookies={"token": auth_token}, timeout=TIMEOUT)
    assert resp.status_code in (404, 405), resp.text  # check what the API actually returns


def test_put_with_missing_field_is_rejected(http, base_url, auth_token, created_booking, booking_payload):
    """PUT replaces the whole resource, so a missing required field should fail."""
    booking_id, _ = created_booking
    incomplete = booking_payload()
    del incomplete["firstname"]

    resp = http.put(f"{base_url}/booking/{booking_id}", json=incomplete,
                    cookies={"token": auth_token}, timeout=TIMEOUT)
    assert resp.status_code == 400, resp.text

