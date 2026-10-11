import pytest
TIMEOUT = 10

@pytest.mark.smoke
@pytest.mark.parametrize(
    'header', [{'Content-Type': 'application/json'}]
)
def test_delete_booking_jwt(http,base_url,created_booking,auth_token, header,):
    booking_id, _ = created_booking
    resp = http.delete(f"{base_url}/booking/{booking_id}", headers = header ,
                    cookies={"token": auth_token}, timeout=TIMEOUT)


@pytest.mark.smoke
def test_delete_booking_jwt(http,base_url,created_booking,auth_token):
    booking_id, _ = created_booking
    header = {'Content-Type': 'application/json',
                'Authorization': f'Bearer{auth_token}'}
    resp = http.delete(f"{base_url}/booking/{booking_id}", headers = header , timeout=TIMEOUT)
