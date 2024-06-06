import requests
from tests.conftest import base_url


def test_recommend_events(base_url):
    url = f"{base_url}/recommend_events"
    params = {'user_id': 'test_user_id', 'n': 4}
    response = requests.get(url, params=params)

    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

    assert response.status_code == 200
    assert isinstance(response.json(), list)
