import random
from datetime import date, timedelta
from typing import List

from faker import Faker

from src.generator.generator import sports_leagues
from src.models.event import Event

fake = Faker()


def randomRecommender() -> List[dict]:
    begin_timestamp = fake.date_this_century().isoformat()
    fake_begin_date = date.fromisoformat(begin_timestamp)
    days_to_add = random.randint(1, 14)
    fake_end_date = fake_begin_date + timedelta(days=days_to_add)
    sport = random.choice(list(sports_leagues.keys()))
    league = random.choice(sports_leagues[sport])

    fake_data = {
        "id": random.randint(1, 9999),
        "event_id": fake.uuid4(),
        "begin_timestamp": fake_begin_date,
        "end_timestamp": fake_end_date,
        "country": fake.country(),
        "league": league,
        "participants": [fake.name() for _ in range(random.randint(2, 2))],
        "sport": sport
    }
    return [Event(**fake_data).to_dict()]
