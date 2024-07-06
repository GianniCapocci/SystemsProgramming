import random
from typing import List

from src.database import db_util


def frequencyRecommender(user_id, n, session) -> List[dict]:
    try:
        similar_events = db_util.findSimilarEvents(user_id, session)
        if n == 0:
            return similar_events
        if len(similar_events) >= n:
            return random.sample(similar_events, n)
        else:
            return []
    except Exception as e:
        print(f"Exception: {e}")
        return []
