from http.client import responses

import pytest
import requests

BASE_URL = "https://dummy.restapiexample.com"

def test_get_all_emp():

    h1 = {"Accept": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(f"{BASE_URL}/api/v1/employees",headers=h1)
    assert response.status_code == 200
    print(response)
    print(type(response))