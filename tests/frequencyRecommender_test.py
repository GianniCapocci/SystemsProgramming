import unittest
from unittest.mock import MagicMock, patch
from src.recommenders import frequencyRecommender


class TestFrequencyRecommender(unittest.TestCase):

    @patch('src.database.db_util.findUser')
    @patch('src.database.db_util.getUserEvents')
    @patch('src.database.db_util.findSimilarEvents')
    @patch('random.sample')
    def test_frequency_recommender_success(self, mock_random_sample, mock_findSimilarEvents, mock_getUserEvents,
                                           mock_findUser):
        user_id = 1
        n = 2
        cursor = MagicMock()

        mock_findUser.return_value = {
            'user_id': str(user_id),
            'birth_year': 1990,
            'country': 'USA',
            'currency': 'USD',
            'gender': 'male',
            'registration_date': '2022-01-01'
        }

        mock_getUserEvents.return_value = [
            {
                'begin_timestamp': '2024-06-01',
                'country': 'USA',
                'end_timestamp': '2024-06-02',
                'event_id': '1',
                'league': 'NBA',
                'participants': ['team1', 'team2'],
                'sport': 'Basketball'
            },
            {
                'begin_timestamp': '2024-06-03',
                'country': 'USA',
                'end_timestamp': '2024-06-04',
                'event_id': '2',
                'league': 'NBA',
                'participants': ['team3', 'team4'],
                'sport': 'Basketball'
            }
        ]

        mock_findSimilarEvents.return_value = [
            {
                'begin_timestamp': '2024-06-01',
                'country': 'USA',
                'end_timestamp': '2024-06-02',
                'event_id': '1',
                'league': 'NBA',
                'participants': ['team1', 'team2'],
                'sport': 'Basketball'
            },
            {
                'begin_timestamp': '2024-06-03',
                'country': 'USA',
                'end_timestamp': '2024-06-04',
                'event_id': '2',
                'league': 'NBA',
                'participants': ['team3', 'team4'],
                'sport': 'Basketball'
            },
            {
                'begin_timestamp': '2024-06-05',
                'country': 'USA',
                'end_timestamp': '2024-06-06',
                'event_id': '3',
                'league': 'NBA',
                'participants': ['team5', 'team6'],
                'sport': 'Basketball'
            }
        ]

        mock_random_sample.return_value = mock_findSimilarEvents.return_value[:n]

        result = frequencyRecommender(user_id, n, cursor)

        expected_result = [
            {
                'begin_timestamp': '2024-06-01',
                'country': 'USA',
                'end_timestamp': '2024-06-02',
                'event_id': '1',
                'league': 'NBA',
                'participants': ['team1', 'team2'],
                'sport': 'Basketball'
            },
            {
                'begin_timestamp': '2024-06-03',
                'country': 'USA',
                'end_timestamp': '2024-06-04',
                'event_id': '2',
                'league': 'NBA',
                'participants': ['team3', 'team4'],
                'sport': 'Basketball'
            }
        ]

        self.assertEqual(result, expected_result)

    @patch('src.database.db_util.findUser')
    @patch('src.database.db_util.getUserEvents')
    @patch('src.database.db_util.findSimilarEvents')
    def test_frequency_recommender_not_enough_similar_events(self, mock_findSimilarEvents, mock_getUserEvents,
                                                             mock_findUser):
        user_id = 1
        n = 5
        cursor = MagicMock()

        mock_findUser.return_value = {
            'user_id': str(user_id),
            'birth_year': 1990,
            'country': 'USA',
            'currency': 'USD',
            'gender': 'male',
            'registration_date': '2022-01-01'
        }

        mock_getUserEvents.return_value = [
            {
                'begin_timestamp': '2024-06-01',
                'country': 'USA',
                'end_timestamp': '2024-06-02',
                'event_id': '1',
                'league': 'NBA',
                'participants': ['team1', 'team2'],
                'sport': 'Basketball'
            },
            {
                'begin_timestamp': '2024-06-03',
                'country': 'USA',
                'end_timestamp': '2024-06-04',
                'event_id': '2',
                'league': 'NBA',
                'participants': ['team3', 'team4'],
                'sport': 'Basketball'
            }
        ]
        mock_findSimilarEvents.return_value = [
            {
                'begin_timestamp': '2024-06-01',
                'country': 'USA',
                'end_timestamp': '2024-06-02',
                'event_id': '1',
                'league': 'NBA',
                'participants': ['team1', 'team2'],
                'sport': 'Basketball'
            },
            {
                'begin_timestamp': '2024-06-03',
                'country': 'USA',
                'end_timestamp': '2024-06-04',
                'event_id': '2',
                'league': 'NBA',
                'participants': ['team3', 'team4'],
                'sport': 'Basketball'
            },
            {
                'begin_timestamp': '2024-06-05',
                'country': 'USA',
                'end_timestamp': '2024-06-06',
                'event_id': '3',
                'league': 'NBA',
                'participants': ['team5', 'team6'],
                'sport': 'Basketball'
            }
        ]

        result = frequencyRecommender(user_id, n, cursor)
        self.assertIsNone(result)

    @patch('src.database.db_util.findUser')
    @patch('src.database.db_util.getUserEvents')
    def test_frequency_recommender_no_user_events(self, mock_getUserEvents, mock_findUser):
        user_id = 1
        n = 2
        cursor = MagicMock()

        # Mock the db_util methods
        mock_findUser.return_value = {
            'user_id': str(user_id),
            'birth_year': 1990,
            'country': 'USA',
            'currency': 'USD',
            'gender': 'male',
            'registration_date': '2022-01-01'
        }
        mock_getUserEvents.return_value = None

        result = frequencyRecommender(user_id, n, cursor)
        self.assertIsNone(result)

    @patch('src.database.db_util.findUser')
    def test_frequency_recommender_user_not_found(self, mock_findUser):
        user_id = 1
        n = 2
        cursor = MagicMock()

        mock_findUser.return_value = None

        result = frequencyRecommender(user_id, n, cursor)
        self.assertIsNone(result)

    @patch('src.database.db_util.findUser')
    def test_frequency_recommender_exception(self, mock_findUser):
        user_id = 1
        n = 2
        cursor = MagicMock()

        mock_findUser.side_effect = Exception('Database error')

        result = frequencyRecommender(user_id, n, cursor)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
