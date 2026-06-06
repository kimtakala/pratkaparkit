import sqlite3
from flask import g, current_app


def get_connection():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
	return g.db


def query_one(sql, params=()):
	cur = get_connection().execute(sql, params)
	return cur.fetchone()


def query_all(sql, params=()):
	cur = get_connection().execute(sql, params)
	return cur.fetchall()


def execute(sql, params=()):
	db = get_connection()
	cursor = db.execute(sql, params)
	db.commit()
	return cursor


def init_app(app):
	@app.teardown_appcontext
	def close_db(e=None):
		db = g.pop('db', None)
		if db is not None:
			db.close()

