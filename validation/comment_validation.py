def validate_comment_form(form):
    text = form.get("text", "").strip()
    if not text:
        return "Kommentti ei voi olla tyhjä"
    return None
