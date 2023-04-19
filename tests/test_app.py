import unittest
import json
from api.index import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_random_text(self):
        response = self.app.get('/api')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn("text", data)
        self.assertIsInstance(data["text"], str)
        self.assertGreater(len(data["text"]), 0)

if __name__ == '__main__':
    unittest.main()