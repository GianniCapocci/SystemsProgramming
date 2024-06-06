import requests
from tests.conftest import base_url


def test_register_coupon(base_url):
    url = f'{base_url}/register_coupon'
    data = {
        "coupon_id": "test_coupon_id",
        "user_id": "test_user_id",
        "stake": 50.5,
        "timestamp": "2023-05-17",
        "selections": [
            {"event_id": "test_event_1", "stake": 10.0},
            {"event_id": "test_event_2", "stake": 20.0}
        ]
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200


def test_register_coupon_invalid(base_url):
    url = f'{base_url}/register_coupon'
    data = {
        "coupon_id": "test_coupon_id",
        "user_id": "test_user_id",
        "stake": "50.5",
        "timestamp": "2023-05",
        "selections": "test_invalid"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 400
