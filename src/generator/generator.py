import os
import random
import sys
import time
import uuid
from datetime import timedelta, date
from typing import List

import requests
from faker import Faker

from src.models.coupon import Coupon
from src.models.event import Event
from src.models.user import User

fake = Faker()

sports_leagues = {
    "Soccer": ["Champions League", "FIFA", "La Liga", "Premier League"],
    "Basketball": ["NBA", "EuroLeague", "NCAA"],
    "Baseball": ["MLB", "Nippon League", "KBO"],
    "Tennis": ["ATP", "WTA", "Grand Slam"],
    "MMA": ["UFC", "Bellator", "ONE Championship"],
    "Swimming": ["FINA World Championships", "Olympics"],
}


def generate_dummy_event():
    begin_timestamp = fake.date_this_century().isoformat()
    fake_begin_date = date.fromisoformat(begin_timestamp)
    days_to_add = random.randint(1, 14)
    fake_end_date = fake_begin_date + timedelta(days=days_to_add)
    sport = random.choice(list(sports_leagues.keys()))
    league = random.choice(sports_leagues[sport])

    return Event(
        event_id=str(fake.uuid4()),
        begin_timestamp=fake_begin_date,
        country=fake.country(),
        end_timestamp=fake_end_date,
        league=league,
        participants=[fake.name() for _ in range(random.randint(2, 2))],
        sport=sport
    )


def generate_dummy_user():
    return User(
        user_id=str(fake.uuid4()),
        birth_year=int(fake.year()),
        country=fake.country(),
        currency=fake.currency_code(),
        gender=fake.random_element(elements=('male', 'female')),
        registration_date=fake.date()
    )


def generate_dummy_selection(event_id: str):
    return {
        'event_id': event_id,
        'odds': round(random.uniform(1, 15), 2)
    }


def generate_dummy_coupon(user_id: str, events: List[Event]) -> Coupon:
    selections = [generate_dummy_selection(event.event_id) for event in events]
    return Coupon(
        coupon_id=str(uuid.uuid4()),
        user_id=user_id,
        stake=round(fake.random_int(10, 1000), 2),
        timestamp=fake.date_this_decade(),
        selections=selections
    )


def send_dummy_data(n: int):
    total_events = 0
    user_url = 'http://127.0.0.1:5000/register_user'
    event_url = 'http://127.0.0.1:5000/register_event'
    coupon_url = 'http://127.0.0.1:5000/register_coupon'

    for i in range(n):
        dummy_user = generate_dummy_user()
        print("Sent User:", dummy_user.to_dict())

        user_response = requests.post(user_url, json=dummy_user.to_dict())
        print('User response:', user_response.status_code)

        events = [generate_dummy_event() for _ in range(random.randint(1, 5))]
        total_events += len(events)

        for event in events:
            print("Sent Event:", event.to_dict())
            event_response = requests.post(event_url, json=event.to_dict())
            print('Event response:', event_response.status_code)

        time.sleep(2)
        dummy_coupon = generate_dummy_coupon(dummy_user.user_id, events)
        print("Sent Coupon:", dummy_coupon.to_dict())
        coupon_response = requests.post(coupon_url, json=dummy_coupon.to_dict())
        print('Coupon response:', coupon_response.status_code)

    print("Total Events:", total_events)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        send_dummy_data(int(sys.argv[1]))
    else:
        print("Usage: python3 src/generator/generator.py [number of events]")
