from db import query_all, query_one, execute


def get_all_spots():
    return query_all("""
        SELECT
            s.id,
            s.owner_id,
            s.title,
            s.description,
            s.lat,
            s.lon,
            s.address,
            s.tags,
            s.created_at,
            u.username AS owner_name,
            COALESCE(GROUP_CONCAT(c.name, ', '), '') AS classification_names
        FROM parking_spot s
        JOIN users u ON s.owner_id = u.id
        LEFT JOIN item_classifications ic ON s.id = ic.item_id
        LEFT JOIN classifications c ON ic.classification_id = c.id
        GROUP BY s.id
        ORDER BY s.created_at DESC
        """)


def create_spot(owner_id, title, description, lat, lon, address, tags, classification_ids=None):
    cursor = execute(
        "INSERT INTO parking_spot (owner_id, title, description, lat, lon, address, tags) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (owner_id, title, description, lat, lon, address, tags),
    )
    set_item_classifications(cursor.lastrowid, classification_ids or [])
    return cursor


def get_spot(spot_id):
    return query_one(
        """
        SELECT
            s.id,
            s.owner_id,
            s.title,
            s.description,
            s.lat,
            s.lon,
            s.address,
            s.tags,
            s.created_at,
            u.username AS owner_name,
            COALESCE(GROUP_CONCAT(c.name, ', '), '') AS classification_names
        FROM parking_spot s
        JOIN users u ON s.owner_id = u.id
        LEFT JOIN item_classifications ic ON s.id = ic.item_id
        LEFT JOIN classifications c ON ic.classification_id = c.id
        WHERE s.id = ?
        GROUP BY s.id
        """,
        (spot_id,),
    )


def update_spot(spot_id, title, description, lat, lon, address, tags, classification_ids=None):
    cursor = execute(
        "UPDATE parking_spot SET title=?, description=?, lat=?, lon=?, address=?, tags=? WHERE id=?",
        (title, description, lat, lon, address, tags, spot_id),
    )
    set_item_classifications(spot_id, classification_ids or [])
    return cursor


def delete_spot(spot_id):
    return execute("DELETE FROM parking_spot WHERE id = ?", (spot_id,))


def get_spots_by_owner(owner_id):
    return query_all(
        """
        SELECT
            s.id,
            s.owner_id,
            s.title,
            s.description,
            s.lat,
            s.lon,
            s.address,
            s.tags,
            s.created_at,
            COALESCE(GROUP_CONCAT(c.name, ', '), '') AS classification_names
        FROM parking_spot s
        LEFT JOIN item_classifications ic ON s.id = ic.item_id
        LEFT JOIN classifications c ON ic.classification_id = c.id
        WHERE s.owner_id = ?
        GROUP BY s.id
        ORDER BY s.created_at DESC
        """,
        (owner_id,),
    )


def get_classifications():
    return query_all("SELECT id, name FROM classifications ORDER BY name ASC")


def get_item_classification_ids(item_id):
    rows = query_all(
        "SELECT classification_id FROM item_classifications WHERE item_id = ? ORDER BY classification_id ASC",
        (item_id,),
    )
    return [row["classification_id"] for row in rows]


def set_item_classifications(item_id, classification_ids):
    execute("DELETE FROM item_classifications WHERE item_id = ?", (item_id,))
    for classification_id in classification_ids:
        execute(
            "INSERT INTO item_classifications (item_id, classification_id) VALUES (?, ?)",
            (item_id, classification_id),
        )
