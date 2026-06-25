import re
import uuid
import unittest

from app import app


class AuthFlowTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def _csrf_token(self, html):
        match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
        self.assertIsNotNone(match)
        return match.group(1)

    def test_register_login_and_logout(self):
        username = f"tester_{uuid.uuid4().hex[:8]}"
        password = "test1234"

        response = self.client.get("/register")
        csrf_token = self._csrf_token(response.get_data(as_text=True))

        response = self.client.post(
            "/register",
            data={
                "username": username,
                "password": password,
                "csrf_token": csrf_token,
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Kirjaudu sisään", response.get_data(as_text=True))

        response = self.client.get("/login")
        csrf_token = self._csrf_token(response.get_data(as_text=True))

        response = self.client.post(
            "/login",
            data={
                "username": username,
                "password": password,
                "csrf_token": csrf_token,
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Kirjaudu ulos", response.get_data(as_text=True))

        response = self.client.get("/")
        csrf_token = self._csrf_token(response.get_data(as_text=True))

        response = self.client.post(
            "/logout",
            data={"csrf_token": csrf_token},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Kirjaudu sisään", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()