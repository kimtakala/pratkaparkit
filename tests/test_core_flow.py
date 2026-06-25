import re
import unittest
import uuid

from app import app
from db import query_one
import users


class CoreFlowTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def _csrf_token(self, html):
        match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
        self.assertIsNotNone(match)
        return match.group(1)

    def _register_and_login(self):
        username = f"core_{uuid.uuid4().hex[:8]}"
        password = "test1234"

        response = self.client.get("/register")
        csrf_token = self._csrf_token(response.get_data(as_text=True))
        self.client.post(
            "/register",
            data={
                "username": username,
                "password": password,
                "csrf_token": csrf_token,
            },
            follow_redirects=True,
        )

        response = self.client.get("/login")
        csrf_token = self._csrf_token(response.get_data(as_text=True))
        self.client.post(
            "/login",
            data={
                "username": username,
                "password": password,
                "csrf_token": csrf_token,
            },
            follow_redirects=True,
        )
        return username

    def test_create_spot_search_comment_and_profile(self):
        username = self._register_and_login()
        with app.app_context():
            user = users.get_user_by_username(username)
            self.assertIsNotNone(user)

        spot_title = f"Core Spot {uuid.uuid4().hex[:8]}"
        response = self.client.get("/spots/new")
        csrf_token = self._csrf_token(response.get_data(as_text=True))

        response = self.client.post(
            "/spots/new",
            data={
                "title": spot_title,
                "description": "Core flow description",
                "lat": "60.1699",
                "lon": "24.9384",
                "address": "Core Street 1",
                "classifications": ["1"],
                "csrf_token": csrf_token,
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with app.app_context():
            spot = query_one(
                "SELECT id FROM parking_spot WHERE title = ?", (spot_title,)
            )
            self.assertIsNotNone(spot)
            spot_id = spot["id"]

        response = self.client.get(f"/spots/{spot_id}")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(spot_title, html)
        self.assertIn("Asfaltti", html)

        csrf_token = self._csrf_token(html)
        response = self.client.post(
            f"/spots/{spot_id}/comments/new",
            data={"text": "Great spot", "csrf_token": csrf_token},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Great spot", response.get_data(as_text=True))

        response = self.client.get(f"/search?q={spot_title}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(spot_title, response.get_data(as_text=True))

        response = self.client.get(f"/users/{user['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(username, response.get_data(as_text=True))
        self.assertIn(spot_title, response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()