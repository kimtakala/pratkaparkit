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
            u.username AS owner_name
        FROM parking_spot s
        JOIN users u ON s.owner_id = u.id
        ORDER BY s.created_at DESC
        """)


def create_spot(owner_id, title, description, lat, lon, address, tags):
    return execute(
        "INSERT INTO parking_spot (owner_id, title, description, lat, lon, address, tags) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (owner_id, title, description, lat, lon, address, tags),
    )


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
            u.username AS owner_name
        FROM parking_spot s
        JOIN users u ON s.owner_id = u.id
        WHERE s.id = ?
        """,
        (spot_id,),
    )


def update_spot(spot_id, title, description, lat, lon, address, tags):
    return execute(
        "UPDATE parking_spot SET title=?, description=?, lat=?, lon=?, address=?, tags=? WHERE id=?",
        (title, description, lat, lon, address, tags, spot_id),
    )


def delete_spot(spot_id):
    return execute("DELETE FROM parking_spot WHERE id = ?", (spot_id,))


def get_spots_by_owner(owner_id):
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
        (owner_id,),
    )
