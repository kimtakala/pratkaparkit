"""Session helpers for login and CSRF protection."""

import secrets
from functools import wraps

from flask import abort, flash, redirect, session, url_for


def current_user_id():
    """Return the logged-in user's ID if present."""

    return session.get("user_id")


def require_login(f):
    """Redirect anonymous users to the login page."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Kirjaudu sisään ensin.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def generate_csrf_token():
    """Return a session-stored CSRF token, creating one if needed."""

    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]


def verify_csrf_token(form_token):
    """Abort with 403 when the submitted CSRF token is invalid."""

    if not form_token or form_token != session.get("csrf_token"):
        abort(403, "CSRF-virhe. Yritä uudelleen.")
