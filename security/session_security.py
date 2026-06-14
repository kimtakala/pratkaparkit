from functools import wraps
from flask import session, redirect, url_for, abort, request, flash, url_for
import secrets


def current_user_id():
    return session.get("user_id")


def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Kirjaudu sisään ensin.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def generate_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]


def verify_csrf_token(form_token):
    if not form_token or form_token != session.get("csrf_token"):
        abort(403, "CSRF-virhe. Yritä uudelleen.")
