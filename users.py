"""Database helpers for users and profile data."""

from werkzeug.security import generate_password_hash

from db import execute, query_all, query_one


def create_user(username, password):
    """Create a user account with a hashed password."""

    password_hash = generate_password_hash(password)
    execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password_hash),
    )


def get_user_by_username(username):
    """Return one user row by username."""

    return query_one(
        "SELECT id, username, password FROM users WHERE username = ?", (username,)
    )


def get_user_by_id(user_id):
    """Return one user row by ID."""

    return query_one("SELECT id, username FROM users WHERE id = ?", (user_id,))


def get_user_stats(user_id):
    """Return profile statistics for one user."""

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


def get_user_items(user_id, limit=None, offset=0):
    """Return parking spots created by one user."""

    sql = """
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
        """
    params = [user_id]
    if limit is not None:
        sql += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
    return query_all(sql, params)
