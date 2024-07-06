import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.models.event import Event
from src.models.user import User
from src.recommenders import frequencyRecommender


class TestFrequencyRecommender(unittest.TestCase):

    @patch('src.database.db_util.findUser')
    @patch('src.database.db_util.getUserEvents')
    @patch('src.database.db_util.findSimilarEvents')
    @patch('random.sample')
    def test_frequency_recommender_success(self, mock_random_sample, mock_findSimilarEvents, mock_getUserEvents,
                                           mock_findUser):
        user_id = 'test_user_id'
        n = 2
        session_mock = MagicMock(spec=Session)

        mock_findUser.return_value = User(
            user_id=user_id,
            birth_year=1990,
            country='USA',
            currency='USD',
            gender='male',
            registration_date='2022-01-01'
        )

        mock_getUserEvents.return_value = [
            Event(
                begin_timestamp='2024-06-01',
                country='USA',
                end_timestamp='2024-06-02',
                event_id='test_event_id_1',
                league='NBA',
                participants=['team1', 'team2'],
                sport='Basketball'
            ),
            Event(
                begin_timestamp='2024-06-03',
                country='USA',
                end_timestamp='2024-06-04',
                event_id='test_event_id_2',
                league='NBA',
                participants=['team3', 'team4'],
                sport='Basketball'
            )
        ]

        mock_findSimilarEvents.return_value = [
            {
                'begin_timestamp': '2024-06-01',
                'country': 'USA',
                'end_timestamp': '2024-06-02',
                'event_id': 'test_event_id_3',
                'league': 'NBA',
                'participants': ['team5', 'team6'],
                'sport': 'Basketball'
            },
            {
                'begin_timestamp': '2024-06-03',
                'country': 'USA',
                'end_timestamp': '2024-06-04',
                'event_id': 'test_event_id_4',
                'league': 'NBA',
                'participants': ['team7', 'team8'],
                'sport': 'Basketball'
            },
            {
                'begin_timestamp': '2024-06-01',
                'country': 'USA',
                'end_timestamp': '2024-06-02',
                'event_id': 'test_event_id_5',
                'league': 'NBA',
                'participants': ['team9', 'team10'],
                'sport': 'Basketball'
            },
        ]

        mock_random_sample.return_value = mock_findSimilarEvents.return_value[:n]

        result = frequencyRecommender(user_id, n, session_mock)

        expected_result = [
            {
                'begin_timestamp': '2024-06-01',
                'country': 'USA',
                'end_timestamp': '2024-06-02',
                'event_id': 'test_event_id_3',
                'league': 'NBA',
                'participants': ['team5', 'team6'],
                'sport': 'Basketball'
            },
            {
                'begin_timestamp': '2024-06-03',
                'country': 'USA',
                'end_timestamp': '2024-06-04',
                'event_id': 'test_event_id_4',
                'league': 'NBA',
                'participants': ['team7', 'team8'],
                'sport': 'Basketball'
            }
        ]

        self.assertEqual(result, expected_result)

    @patch('src.database.db_util.findSimilarEvents')
    def test_frequency_recommender_not_enough_similar_events(self, mock_findSimilarEvents):
        user_id = 'test_user_id'
        n = 2
        session_mock = MagicMock(spec=Session)

        mock_findSimilarEvents.return_value = [
            {
                'begin_timestamp': '2024-06-01',
                'end_timestamp': '2024-06-02',
                'event_id': 'test_event_id',
                'league': 'NBA',
                'participants': ['team1', 'team2'],
                'sport': 'Basketball'
            }
        ]

        result = frequencyRecommender(user_id, n, session_mock)

        self.assertEqual(result, [])

    @patch('src.database.db_util.findUser')
    @patch('src.database.db_util.getUserEvents')
    def test_frequency_recommender_no_user_events(self, mock_getUserEvents, mock_findUser):
        user_id = 'test_user_id'
        n = 2
        session_mock = MagicMock(spec=Session)

        mock_findUser.return_value = User(
            user_id=user_id,
            birth_year=1990,
            country='USA',
            currency='USD',
            gender='male',
            registration_date='2022-01-01'
        )
        mock_getUserEvents.return_value = []

        result = frequencyRecommender(user_id, n, session_mock)

        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
