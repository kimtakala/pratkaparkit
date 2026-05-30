import sqlite3
from flask import g, current_app

def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def db_query_one(sql, params=()):
    cur = get_db_connection().execute(sql, params)
    return cur.fetchone()

def db_query_all(sql, params=()):
    cur = get_db_connection().execute(sql, params)
    return cur.fetchall()

def db_execute(sql, params=()):
    db = get_db_connection()
    cursor = db.execute(sql, params)
    db.commit()
    return cursor

def init_app(app):
    @app.teardown_appcontext
    def close_db(e=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()
