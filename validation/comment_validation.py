"""Validation helpers for comment forms."""


def validate_comment_form(form):
    """Validate a comment form and return a list of errors."""

    errors = []
    text = form.get("text", "").strip()
    if not text:
        errors.append("Kommentti ei voi olla tyhjä.")
    return errors
