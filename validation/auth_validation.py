"""Validation helpers for authentication forms."""


def validate_register_form(form):
    """Validate the registration form and return a list of errors."""

    errors = []
    username = form.get("username", "").strip()
    password = form.get("password", "")
    if len(username) < 3:
        errors.append("Käyttäjätunnuksen pitää olla vähintään 3 merkkiä pitkä.")
    if len(password) < 4:
        errors.append("Salasanan pitää olla vähintään 4 merkkiä pitkä.")
    return errors


def validate_login_form(form):
    """Validate the login form and return a list of errors."""

    errors = []
    username = form.get("username", "").strip()
    password = form.get("password", "")
    if not username:
        errors.append("Käyttäjätunnus puuttuu.")
    if not password:
        errors.append("Salasana puuttuu.")
    return errors
