import pytest


@pytest.fixture
def base_url():
    return 'http://127.0.0.1:5000'


KAFKA_TEST_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'test-group',
    'auto.offset.reset': 'earliest'
}

TEST_CONSUMER_TOPIC = 'users'
TEST_PRODUCER_TOPIC = 'users'
