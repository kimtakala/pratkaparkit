"""Create demo users and parking spots for large-data testing."""

import random
import string
import uuid

from flask import Flask

import config
import db
import items
import users


def _random_text(prefix, length=8):
    """Return a short random text value with the given prefix."""

    suffix = "".join(random.choices(string.ascii_lowercase, k=length))
    return f"{prefix} {suffix}"


def _create_demo_user(index):
    """Create and return one demo user."""

    username = f"seed_user_{index:04d}_{uuid.uuid4().hex[:8]}"
    password = "seed1234"
    users.create_user(username, password)
    return users.get_user_by_username(username)


def _create_demo_spot(owner_id, index):
    """Create one demo parking spot for the given owner."""

    title = _random_text(f"Seed Spot {index:04d}", 6)
    description = "Generated for large-data testing."
    lat = 60.1699 + random.uniform(-0.25, 0.25)
    lon = 24.9384 + random.uniform(-0.25, 0.25)
    address = _random_text("Seed Address", 10)
    tags = "seed"
    classification_ids = [1] if index % 2 == 0 else [2]
    items.create_spot(
        owner_id,
        {
            "title": title,
            "description": description,
            "lat": lat,
            "lon": lon,
            "address": address,
            "tags": tags,
        },
        classification_ids,
    )


def main(user_count=20, spot_count=1000):
    """Populate the database with demo users and spots."""

    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["DATABASE"] = config.DATABASE_PATH
    db.init_app(app)

    with app.app_context():
        for index in range(user_count):
            _create_demo_user(index)

        user_ids = [
            row["id"] for row in db.query_all("SELECT id FROM users ORDER BY id")
        ]
        for index in range(spot_count):
            owner_id = user_ids[index % len(user_ids)]
            _create_demo_spot(owner_id, index)


if __name__ == "__main__":
    main()
