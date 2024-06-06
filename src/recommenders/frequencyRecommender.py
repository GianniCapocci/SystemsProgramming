import json
import random
from typing import List
from src.schemas import Event


def frequencyRecommender(user_id: str, n, cursor) -> List[Event]:

    cursor.execute("SELECT * FROM users WHERE user_id = %s", user_id)
    user = cursor.fetchone()
    if not user:
        return []

    cursor.execute("""
        SELECT e.* FROM events e
        JOIN selections s ON e.event_id = s.event_id
        JOIN coupons c ON s.coupon_id = c.coupon_id
        WHERE c.user_id = %s
    """, (user_id,))
    user_events = cursor.fetchall()

    if not user_events:
        return []

    similar_events = []
    for event in user_events:
        cursor.execute("""
            SELECT * FROM events
            WHERE (league = %s OR sport = %s) AND event_id != %s
            AND event_id NOT IN (SELECT event_id FROM selections WHERE coupon_id IN
            (SELECT coupon_id FROM coupons WHERE user_id = %s))
        """, (event['league'], event['sport'], event['event_id'], user_id))
        similar_events.extend(cursor.fetchall())

    cursor.close()

    for event in similar_events:
        event['participants'] = json.loads(event['participants'])

    if len(similar_events) >= 5:
        return random.sample(similar_events, 5)

    return [Event(**event) for event in similar_events]