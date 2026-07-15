"""Database connection helpers for the Flask app."""

from pathlib import Path
import sqlite3

from flask import current_app, g

SQL_DIR = Path(__file__).resolve().parent / "sql"
SCHEMA_PATH = SQL_DIR / "schema.sql"
INIT_PATH = SQL_DIR / "init.sql"


def get_connection():
    """Return the active SQLite connection for the current request."""

    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def query_one(sql, params=()):
    """Return a single row for the given SQL query."""

    cur = get_connection().execute(sql, params)
    return cur.fetchone()


def query_all(sql, params=()):
    """Return all rows for the given SQL query."""

    cur = get_connection().execute(sql, params)
    return cur.fetchall()


def execute(sql, params=()):
    """Execute a write query and commit the transaction."""

    db = get_connection()
    cursor = db.execute(sql, params)
    db.commit()
    return cursor


def init_schema():
    """Load the database schema and seed rows from sql/ files."""

    with open(SCHEMA_PATH, encoding="utf-8") as schema_file:
        get_connection().executescript(schema_file.read())
    with open(INIT_PATH, encoding="utf-8") as init_file:
        get_connection().executescript(init_file.read())
    get_connection().commit()


def init_app(app):
    """Register teardown handling and initialize the schema."""

    @app.teardown_appcontext
    def close_db(_error=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with app.app_context():
        init_schema()
