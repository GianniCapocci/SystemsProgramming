from src.database import db_util
from src.recommenders.frequencyRecommender import frequencyRecommender as freqRecommender
from src.recommenders.randomRecommender import randomRecommender as randRecommender


def wrapperRecommender(user_id: str, n, cursor):
    try:
        user = db_util.findUser(user_id, cursor)
        if user is not None:
            events = db_util.findSimilarEvents()
            if events >= n:
                return freqRecommender(user_id, n, cursor)
            else:
                return randRecommender()
    except Exception as e:
        print(f"Exception from wrapperRecommender: {e}")
        return None
