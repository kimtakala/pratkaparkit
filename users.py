from werkzeug.security import generate_password_hash, check_password_hash
from db import query_one, query_all, execute


def create_user(username, password):
    pass_hash = generate_password_hash(password)
    execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, pass_hash)
    )


def get_user_by_username(username):
    return query_one(
        "SELECT id, username, password FROM users WHERE username = ?", (username,)
    )


def get_user_by_id(user_id):
    return query_one("SELECT id, username FROM users WHERE id = ?", (user_id,))


def get_user_stats(user_id):
    return query_one(
        """
        SELECT
            u.id,
            u.username,
            (SELECT COUNT(*) FROM parking_spot WHERE owner_id = u.id) AS spot_count,
            (SELECT COUNT(*) FROM comment WHERE author_id = u.id) AS comment_count
        FROM users u
        WHERE u.id = ?
        """,
        (user_id,),
    )


def get_user_items(user_id):
    return query_all(
        """
        SELECT
            id,
            owner_id,
            title,
            description,
            lat,
            lon,
            address,
            tags,
            created_at
        FROM parking_spot
        WHERE owner_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )
