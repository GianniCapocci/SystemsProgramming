import unittest
from datetime import date

from src.recommenders.randomRecommender import randomRecommender


class TestRandomRecommender(unittest.TestCase):

    def test_random_recommender(self):
        event = randomRecommender()

        self.assertTrue(hasattr(event, 'begin_timestamp'))
        self.assertTrue(hasattr(event, 'country'))
        self.assertTrue(hasattr(event, 'end_timestamp'))
        self.assertTrue(hasattr(event, 'event_id'))
        self.assertTrue(hasattr(event, 'league'))
        self.assertTrue(hasattr(event, 'participants'))
        self.assertTrue(hasattr(event, 'sport'))

        self.assertIsInstance(event.begin_timestamp, date)
        self.assertIsInstance(event.country, str)
        self.assertIsInstance(event.end_timestamp, date)
        self.assertIsInstance(event.event_id, str)
        self.assertIsInstance(event.league, str)
        self.assertIsInstance(event.participants, list)
        for participant in event.participants:
            self.assertIsInstance(participant, str)
        self.assertIsInstance(event.sport, str)
