"""Database helpers for parking spots and classifications."""

from db import execute, query_all, query_one


def get_all_spots(limit=None, offset=0):
    """Return parking spots ordered from newest to oldest."""

    sql = """
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
        """
    params = []
    if limit is not None:
        sql += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
    return query_all(sql, params)


def search_spots(query_text="", min_lat="", max_lat="", min_lon="", max_lon=""):
    """Search parking spots by text and optional bounding box."""

    sql = """
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
    """
    conditions = []
    params = []

    if query_text:
        like_query = f"%{query_text}%"
        conditions.append(
            "(s.title LIKE ? OR s.description LIKE ? OR s.address LIKE ? OR s.tags LIKE ?)"
        )
        params.extend([like_query, like_query, like_query, like_query])

    bbox_values = [min_lat, max_lat, min_lon, max_lon]
    if all(bbox_values):
        conditions.append("s.lat BETWEEN ? AND ? AND s.lon BETWEEN ? AND ?")
        params.extend([float(min_lat), float(max_lat), float(min_lon), float(max_lon)])

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " GROUP BY s.id ORDER BY s.created_at DESC"
    return query_all(sql, params)


def create_spot(owner_id, spot_data, classification_ids=None):
    """Create a new parking spot and attach classifications."""

    cursor = execute(
        """
        INSERT INTO parking_spot (owner_id, title, description, lat, lon, address, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            owner_id,
            spot_data["title"],
            spot_data["description"],
            spot_data["lat"],
            spot_data["lon"],
            spot_data["address"],
            spot_data["tags"],
        ),
    )
    set_item_classifications(cursor.lastrowid, classification_ids or [])
    return cursor


def get_spot(spot_id):
    """Return one parking spot with owner and classification data."""

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


def update_spot(spot_id, spot_data, classification_ids=None):
    """Update a parking spot and replace its classifications."""

    cursor = execute(
        """
        UPDATE parking_spot
        SET title=?, description=?, lat=?, lon=?, address=?, tags=?
        WHERE id=?
        """,
        (
            spot_data["title"],
            spot_data["description"],
            spot_data["lat"],
            spot_data["lon"],
            spot_data["address"],
            spot_data["tags"],
            spot_id,
        ),
    )
    set_item_classifications(spot_id, classification_ids or [])
    return cursor


def delete_spot(spot_id):
    """Delete a parking spot and its classification links."""

    return execute("DELETE FROM parking_spot WHERE id = ?", (spot_id,))


def get_spots_by_owner(owner_id):
    """Return parking spots created by one user."""

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
    """Return all classifications for spot forms."""

    return query_all("SELECT id, name FROM classifications ORDER BY name ASC")


def get_item_classification_ids(item_id):
    """Return classification IDs attached to one parking spot."""

    rows = query_all(
        """
        SELECT classification_id
        FROM item_classifications
        WHERE item_id = ?
        ORDER BY classification_id ASC
        """,
        (item_id,),
    )
    return [row["classification_id"] for row in rows]


def set_item_classifications(item_id, classification_ids):
    """Replace the classifications linked to one parking spot."""

    execute("DELETE FROM item_classifications WHERE item_id = ?", (item_id,))
    for classification_id in classification_ids:
        execute(
            "INSERT INTO item_classifications (item_id, classification_id) VALUES (?, ?)",
            (item_id, classification_id),
        )
