"""DB helper pseudocode for SQLite access."""


def get_db_connection():
    """Open SQLite connection and configure row factory."""
    pass


def db_query_one(sql, params):
    """Run a parameterized SELECT and return one row."""
    pass


def db_query_all(sql, params):
    """Run a parameterized SELECT and return all rows."""
    pass


def db_execute(sql, params):
    """Run INSERT/UPDATE/DELETE and commit transaction."""
    pass
