from src.database import db_util
from src.recommenders.frequencyRecommender import frequencyRecommender as freqRecommender
from src.recommenders.randomRecommender import randomRecommender as randRecommender


def wrapperRecommender(user_id: str, n: int, session):
    try:
        user = db_util.findUser(user_id, session)
        if user is not None:
            if n >= 0:
                return freqRecommender(user_id, n, session)
            else:
                return randRecommender()
    except Exception as e:
        print(f"Exception from wrapperRecommender: {e}")
        return []
