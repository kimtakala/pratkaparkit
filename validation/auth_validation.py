def validate_register_form(form):
    username = form.get("username", "").strip()
    password = form.get("password", "")
    if len(username) < 3:
        return "Käyttäjänimi liian lyhyt"
    if len(password) < 4:
        return "Salasana liian lyhyt"
    return None

def validate_login_form(form):
    # Just basic check
    return None
