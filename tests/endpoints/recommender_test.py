import requests
from tests.conftest import base_url


def test_recommendations(base_url):
    url = f"{base_url}/recommendations"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    recommendation = response.json()
    assert isinstance(recommendation, dict)
