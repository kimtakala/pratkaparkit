"""Database helpers for comments."""

from db import execute, query_all


def get_comments_for_spot(spot_id):
    """Return comments for one parking spot in reverse chronological order."""

    return query_all(
        """
        SELECT
            c.id,
            c.parking_spot_id,
            c.author_id,
            c.text,
            c.created_at,
            u.username AS author_name
        FROM comment c
        JOIN users u ON c.author_id = u.id
        WHERE c.parking_spot_id = ?
        ORDER BY c.created_at DESC
        """,
        (spot_id,),
    )


def add_comment(spot_id, author_id, text):
    """Insert a new comment for a parking spot."""

    return execute(
        "INSERT INTO comment (parking_spot_id, author_id, text) VALUES (?, ?, ?)",
        (spot_id, author_id, text),
    )
