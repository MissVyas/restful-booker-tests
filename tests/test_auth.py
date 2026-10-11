
def test_auth(http,base_url):
    header = {
        'Content-Type' : 'application/json'
    }

    payload = {
        'username' : 'admin',
        'password' : 'password123'
    }
    response = http.post(f'{base_url}/auth', headers = header, json = payload)

    assert response.status_code == 200

    json_response = response.json()

    assert len(json_response) > 0

    assert len(json_response["token"]) > 0

