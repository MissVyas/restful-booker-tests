import pytest

@pytest.mark.smoke
def test_ping(http,base_url):
    response = http.get(f"{base_url}/ping", timeout=10)
    assert response.status_code == 201
    assert response.text == "Created"