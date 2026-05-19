"""Parking spot and comment route pseudocode blueprint."""

from flask import Blueprint

from db.connection import db_query_all, db_query_one, db_execute
from security.session_security import (
    require_login,
    generate_csrf_token,
    verify_csrf_token,
)
from validation.spot_validation import validate_spot_form
from validation.comment_validation import validate_comment_form

spots_bp = Blueprint("spots", __name__)


@spots_bp.route("/", methods=["GET"])
def index():
    """List parking spots (pseudocode)."""
    db_query_all("SELECT ...", ())
    return "TODO: index"


@spots_bp.route("/spots/new", methods=["GET", "POST"])
def create_spot():
    """Create parking spot (pseudocode)."""
    require_login()
    generate_csrf_token()
    verify_csrf_token(None)
    validate_spot_form({})
    db_execute("INSERT ...", ())
    return "TODO: create_spot"


@spots_bp.route("/spots/<int:spot_id>", methods=["GET"])
def spot_detail(spot_id):
    """Show parking spot details and comments (pseudocode)."""
    db_query_one("SELECT ... WHERE id = ?", (spot_id,))
    db_query_all("SELECT ... FROM comment WHERE parking_spot_id = ?", (spot_id,))
    return "TODO: spot_detail"


@spots_bp.route("/spots/<int:spot_id>/edit", methods=["GET", "POST"])
def edit_spot(spot_id):
    """Edit own parking spot (pseudocode)."""
    require_login()
    generate_csrf_token()
    verify_csrf_token(None)
    validate_spot_form({})
    db_execute("UPDATE ... WHERE id = ?", (spot_id,))
    return "TODO: edit_spot"


@spots_bp.route("/spots/<int:spot_id>/delete", methods=["POST"])
def delete_spot(spot_id):
    """Delete own parking spot (pseudocode)."""
    require_login()
    verify_csrf_token(None)
    db_execute("DELETE ... WHERE id = ?", (spot_id,))
    return "TODO: delete_spot"


@spots_bp.route("/spots/<int:spot_id>/comments/new", methods=["POST"])
def create_comment(spot_id):
    """Create comment for a parking spot (pseudocode)."""
    require_login()
    verify_csrf_token(None)
    validate_comment_form({})
    db_execute("INSERT INTO comment(...) VALUES (...)", ())
    return "TODO: create_comment"
