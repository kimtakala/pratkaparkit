import re
import unittest
import uuid

from app import app


class ValidationFeedbackTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def _csrf_token(self, html):
        match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
        self.assertIsNotNone(match)
        return match.group(1)

    def _register_and_login(self):
        username = f"validator_{uuid.uuid4().hex[:8]}"
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

    def test_register_shows_multiple_errors(self):
        response = self.client.get("/register")
        csrf_token = self._csrf_token(response.get_data(as_text=True))

        response = self.client.post(
            "/register",
            data={
                "username": "ab",
                "password": "x",
                "csrf_token": csrf_token,
            },
        )
        html = response.get_data(as_text=True)
        self.assertIn("Käyttäjätunnuksen pitää olla vähintään 3 merkkiä pitkä.", html)
        self.assertIn("Salasanan pitää olla vähintään 4 merkkiä pitkä.", html)
        self.assertIn('value="ab"', html)

    def test_spot_form_shows_multiple_errors_and_keeps_input(self):
        self._register_and_login()

        response = self.client.get("/spots/new")
        csrf_token = self._csrf_token(response.get_data(as_text=True))

        response = self.client.post(
            "/spots/new",
            data={
                "title": "",
                "description": "Test description",
                "lat": "abc",
                "lon": "24.9384",
                "address": "Test Address",
                "csrf_token": csrf_token,
            },
        )
        html = response.get_data(as_text=True)
        self.assertIn("Otsikko puuttuu.", html)
        self.assertIn("Leveysaste: Koordinaatti ei ole kelvollisessa muodossa.", html)
        self.assertIn("Test description", html)
        self.assertIn("Test Address", html)


if __name__ == "__main__":
    unittest.main()