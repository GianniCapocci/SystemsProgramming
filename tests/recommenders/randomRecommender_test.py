import unittest
from datetime import datetime
from src.recommenders.randomRecommender import randomRecommender


class TestRandomRecommender(unittest.TestCase):

    def test_random_recommender(self):
        events = randomRecommender()

        self.assertEqual(len(events), 1)
        event = events[0]

        self.assertTrue('id' in event)
        self.assertTrue('event_id' in event)
        self.assertTrue('begin_timestamp' in event)
        self.assertTrue('end_timestamp' in event)
        self.assertTrue('country' in event)
        self.assertTrue('league' in event)
        self.assertTrue('participants' in event)
        self.assertTrue('sport' in event)

        self.assertIsInstance(event['id'], int)
        self.assertIsInstance(event['begin_timestamp'], str)
        self.assertIsInstance(event['country'], str)
        self.assertIsInstance(event['end_timestamp'], str)
        self.assertIsInstance(event['event_id'], str)
        self.assertIsInstance(event['league'], str)
        self.assertIsInstance(event['participants'], list)
        for participant in event['participants']:
            self.assertIsInstance(participant, str)
        self.assertIsInstance(event['sport'], str)

        try:
            datetime.strptime(event['begin_timestamp'], '%Y-%m-%d')
            datetime.strptime(event['end_timestamp'], '%Y-%m-%d')
        except ValueError:
            self.fail(f"{event['begin_timestamp']} is not in ISO format YYYY-MM-DD")
