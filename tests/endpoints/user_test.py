import requests
from tests.conftest import base_url


def test_register_user(base_url):
    url = f'{base_url}/register_user'
    data = {
        "user_id": "test_user_id_2",
        "birth_year": 1990,
        "country": "USA",
        "currency": "USD",
        "gender": "male",
        "registration_date": "2023-05-17"
    }
    response = requests.post(url, json=data)

    assert response.status_code == 200


def test_register_user_invalid(base_url):
    url = f'{base_url}/register_user'
    data = {
        "user_id": "test_user_id",
        "birth_year": "1990",
        "country": "USA",
        "currency": "USD",
        "gender": 1,
        "registration_date": "2023-05"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 400
