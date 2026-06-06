from db import query_all, execute


def get_comments_for_spot(spot_id):
    return query_all("SELECT c.*, u.username as author_name FROM comment c JOIN users u ON c.author_id = u.id WHERE c.parking_spot_id = ? ORDER BY c.created_at DESC", (spot_id,))


def add_comment(spot_id, author_id, text):
    return execute("INSERT INTO comment (parking_spot_id, author_id, text) VALUES (?, ?, ?)", (spot_id, author_id, text))
