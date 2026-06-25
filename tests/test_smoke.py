import unittest

from app import app


class SmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage_returns_ok(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Pr\xc3\xa4tk\xc3\xa4-parkit", response.data)


if __name__ == "__main__":
    unittest.main()