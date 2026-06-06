def validate_register_form(form):
    errors = []
    username = form.get("username", "").strip()
    password = form.get("password", "")
    if len(username) < 3:
        errors.append("Käyttäjänimi liian lyhyt")
    if len(password) < 4:
        errors.append("Salasana liian lyhyt")
    return errors

def validate_login_form(form):
    errors = []
    username = form.get("username", "").strip()
    password = form.get("password", "")
    if not username:
        errors.append("Käyttäjätunnus puuttuu")
    if not password:
        errors.append("Salasana puuttuu")
    return errors
