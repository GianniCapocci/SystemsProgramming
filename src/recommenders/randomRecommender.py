from faker import Faker
import random
from datetime import date, timedelta
from src.schemas import Event
from src.utils.idGenerator import generate_alphanumeric

fake = Faker()


def randomRecommender() -> Event:

    begin_timestamp = fake.date_this_century().isoformat()
    fake_begin_date = date.fromisoformat(begin_timestamp)
    days_to_add = random.randint(1, 14)
    fake_end_date = fake_begin_date + timedelta(days=days_to_add)

    fake_event_id = f"{generate_alphanumeric(8)}-{generate_alphanumeric(4)}-{generate_alphanumeric(4)}-{generate_alphanumeric(4)}-{generate_alphanumeric(12)}"

    fake_data = {
        "begin_timestamp": fake_begin_date,
        "country": fake.country(),
        "end_timestamp": fake_end_date,
        "event_id": fake_event_id,
        "league": fake.word(),
        "participants": [fake.name() for _ in range(random.randint(2, 2))],
        "sport": fake.word()
    }
    return Event(**fake_data)
