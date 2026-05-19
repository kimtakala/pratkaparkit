"""Session and CSRF pseudocode helpers."""


def current_user_id():
    """Return session user id or None."""
    pass


def require_login():
    """Redirect to login or abort(403) if user is not authenticated."""
    pass


def generate_csrf_token():
    """Generate and store CSRF token in session."""
    pass


def verify_csrf_token(form_token):
    """Compare submitted CSRF token with session token."""
    pass
