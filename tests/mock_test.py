"""
    test.py
    
    This file tests whether user lists is being appended properly on DB
"""

import unittest
import unittest.mock as mock
from unittest.mock import patch
import os
import sys
import random

sys.path.append(os.path.abspath('../'))
import models
from app import add_user

KEY_INPUT = 'input'
KEY_EXPECTED = 'expected'

INITIAL_USERNAME = 'user1'
INITIAL_SCORE = 100


class AddUserTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 'ian',
                KEY_EXPECTED: ([INITIAL_USERNAME, 'ian'], [INITIAL_SCORE, INITIAL_SCORE]),
            },
        ]
        
        rand = random.randint(0, 500)
        initial_person = models.Person(id=rand, username=INITIAL_USERNAME, score=INITIAL_SCORE)
        self.initial_db_mock = [initial_person]
        self.initial_sc_mock = [INITIAL_SCORE]
    
    def mocked_db_session_add(self, username):
        self.initial_db_mock.append(username)
        self.initial_sc_mock.append(INITIAL_SCORE)
        
    
    def mocked_db_session_commit(self):
        pass
    
    def mocked_person_query_all(self):
        return self.initial_db_mock
    
    def test_success(self):
        for test in self.success_test_params:
            with patch('app.DB.session.add', self.mocked_db_session_add):
                with patch('app.DB.session.commit', self.mocked_db_session_commit):
                    with patch('models.Person.query') as mocked_query:
                        mocked_query.all = self.mocked_person_query_all
                        print('Init:', self.initial_db_mock)
                        actual_result = add_user(test[KEY_INPUT])
                        print('Actual:', actual_result)
                        expected_result = test[KEY_EXPECTED]
                        print('Then:', self.initial_db_mock)
                        print('Expected:', expected_result)
                        
                        self.assertEqual(len(actual_result), len(expected_result))
                        self.assertEqual(actual_result[1], expected_result[1])
                    
if __name__ == '__main__':
    unittest.main()
