def validate_register_form(form):
    errors = []
    username = form.get("username", "").strip()
    password = form.get("password", "")
    if len(username) < 3:
        errors.append("Käyttäjätunnuksen pitää olla vähintään 3 merkkiä pitkä.")
    if len(password) < 4:
        errors.append("Salasanan pitää olla vähintään 4 merkkiä pitkä.")
    return errors


def validate_login_form(form):
    errors = []
    username = form.get("username", "").strip()
    password = form.get("password", "")
    if not username:
        errors.append("Käyttäjätunnus puuttuu.")
    if not password:
        errors.append("Salasana puuttuu.")
    return errors
