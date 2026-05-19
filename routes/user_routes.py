"""User profile route pseudocode blueprint."""

from flask import Blueprint

from db.connection import db_query_one, db_query_all

users_bp = Blueprint("users", __name__)


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def user_profile(user_id):
    """Show user profile and stats (pseudocode, VP3-ready)."""
    db_query_one("SELECT ... WHERE id = ?", (user_id,))
    db_query_all("SELECT ... WHERE owner_id = ?", (user_id,))
    return "TODO: user_profile"
