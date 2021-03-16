"""
    unit_test.py
    
    This file tests if scores are being added properly
"""

import unittest
import os
import sys
import random

sys.path.append(os.path.abspath('../'))
import models
from app import add_user_to_list

KEY_INPUT = 'input'
KEY_EXPECTED = 'expected'

#update_score(user1, user2) => [101, 99]

class UpdateScoreTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: 'admin',
                KEY_EXPECTED: [KEY_INPUT],
            },
        ]
        
        self.failure_test_params = [
            {
                KEY_INPUT: 'admin',
                KEY_EXPECTED: ['test', 'ian'],
            },
            {
                KEY_INPUT: 'admin',
                KEY_EXPECTED: ['a'],
            },
        ]
    
    
    def test_update_success(self):
        for test in self.success_test_params:
            actual_result = add_user_to_list(KEY_INPUT)
            
            expected_result = test[KEY_EXPECTED]
            
            self.assertEqual(actual_result, expected_result)
            self.assertEqual(actual_result[0], expected_result[0])
            
    def test_update_failure(self):
        for test in self.failure_test_params:
            actual_result = add_user_to_list(KEY_INPUT)
            
            expected_result = test[KEY_EXPECTED]
            
            self.assertNotEqual(actual_result, expected_result)
            self.assertNotEqual(actual_result[0], expected_result[0])
            
if __name__ == '__main__':
    unittest.main()