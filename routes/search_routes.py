"""Search route pseudocode blueprint."""

from flask import Blueprint

from db.connection import db_query_all

search_bp = Blueprint("search", __name__)


@search_bp.route("/search", methods=["GET"])
def search():
    """Search by text and optional bounding box (pseudocode)."""
    db_query_all("SELECT ...", ())
    return "TODO: search"
