import json
import random
from typing import List
from src.database import db_util
from src.schemas import Event


def frequencyRecommender(user_id, n, cursor):
    try:
        user = db_util.findUser(user_id, cursor)
        if user:
            user_events = db_util.getUserEvents(user_id, cursor)
            if user_events:
                similar_events = db_util.findSimilarEvents(user_id, user_events, cursor)
                if len(similar_events) >= n:
                    return random.sample(similar_events, n)
    except Exception as e:
        print(f"Exception: {e}")
        return None
    return None




# def frequencyRecommender(user_id: str, n, cursor) -> List[Event]:
#     user = db_util.findUser(user_id, cursor)
#     similar_events = []
#     if user:
#         user_events = db_util.getUserEvents(user_id, cursor)
#         if user_events:
#             similar_events = db_util.findSimilarEvents()
#             if similar_events:
#                 return similar_events
#             else:
#                 return []
#         else:
#             return []
#     else:
#         return []
#
#     cursor.close()
#
#     for event in similar_events:
#         event['participants'] = json.loads(event['participants'])
#
#     if len(similar_events) >= n:
#         return random.sample(similar_events, n)
#
#     return [Event(**event) for event in similar_events]
