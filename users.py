from werkzeug.security import generate_password_hash, check_password_hash
from db import query_one, execute


def create_user(username, password):
    pass_hash = generate_password_hash(password)
    execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, pass_hash))


def get_user_by_username(username):
    return query_one("SELECT id, username, password FROM users WHERE username = ?", (username,))


def get_user_by_id(user_id):
    return query_one("SELECT id, username FROM users WHERE id = ?", (user_id,))
