import unittest
from app import create_app


class AppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.test_client = self.app.test_client()

    def test_ping(self):
        response = self.test_client.get('/api/ping')
        assert 'PONG' in response.get_json()['message']


if __name__ == '__main__':
    unittest.main()
