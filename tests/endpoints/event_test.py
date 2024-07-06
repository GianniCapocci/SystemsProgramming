import requests

from tests.conftest import base_url


def test_register_event(base_url):
    url = f'{base_url}/register_event'
    data = {
        "event_id": "test_event_1",
        "begin_timestamp": "2023-05-17",
        "end_timestamp": "2023-05-18",
        "country": "USA",
        "league": "Test League",
        "participants": ["Team A", "Team B"],
        "sport": "Test"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200


def test_register_event_invalid(base_url):
    url = f'{base_url}/register_event'
    data = {
        "begin_timestamp": "2023-05",
        "country": 13,
        "end_timestamp": "2023-05-18",
        "event_id": "test_event_id",
        "league": "Test League",
        "participants": "Team A",
        "sport": "Test"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 400
