def validate_comment_form(form):
    errors = []
    text = form.get("text", "").strip()
    if not text:
        errors.append("Kommentti ei voi olla tyhjä")
    return errors
