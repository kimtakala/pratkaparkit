from flask import Blueprint, render_template, abort
from db.connection import db_query_one, db_query_all

users_bp = Blueprint("users", __name__)

@users_bp.route("/users/<int:user_id>", methods=["GET"])
def user_profile(user_id):
    user = db_query_one("SELECT * FROM users WHERE id = ?", (user_id,))
    if not user:
        abort(404)
    spots = db_query_all("SELECT * FROM parking_spot WHERE owner_id = ? ORDER BY created_at DESC", (user_id,))
    # Minimitaso
    return f"Käyttäjän {user['username']} profiili. Lisätyt paikat: {len(spots)}"
