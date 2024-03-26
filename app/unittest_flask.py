import unittest
from unittest.mock import patch, MagicMock
import time
from flask import json
from app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.db = MagicMock()

    def test_check_pattern(self):
        with patch('app.db', self.db):
            with patch('app.process_log_file') as mock_process_log_file:
                response = self.app.post('/check-pattern', data=json.dumps({'filename': 'test.log'}),
                                         content_type='application/json')
                time.sleep(1)  # Wait for 1 second to allow process_log_file to be called
                self.assertEqual(response.status_code, 202)
                mock_process_log_file.assert_called_once()

    def test_get_searched_logs(self):
        with patch('app.db', self.db):
            self.db.logs.find.return_value = [{'log_file_name': 'test.log'}]
            response = self.app.get('/searched-logs')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.get_data())
            self.assertEqual(data['log_names'], ['test.log'])

    def test_delete_log_by_name(self):
        with patch('app.db', self.db):
            response = self.app.delete('/delete-log?log_file_name=test.log')
            self.assertEqual(response.status_code, 200)
            self.db.logs.delete_one.assert_called_once_with({'log_file_name': 'test.log'})

    def test_delete_log_by_id(self):
        with patch('app.db', self.db):
            response = self.app.delete('/delete-log?log_id=123')
            self.assertEqual(response.status_code, 200)
            self.db.logs.delete_one.assert_called_once_with({'_id': '123'})

if __name__ == '__main__':
    unittest.main()