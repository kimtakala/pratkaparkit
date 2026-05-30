from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from db.connection import db_query_all, db_query_one, db_execute
from security.session_security import require_login, generate_csrf_token, verify_csrf_token, current_user_id
from validation.spot_validation import validate_spot_form
from validation.comment_validation import validate_comment_form
import examples.geo_helpers as geo_helpers

spots_bp = Blueprint("spots", __name__)

@spots_bp.route("/", methods=["GET"])
def index():
    spots = db_query_all("SELECT s.*, u.username as owner_name FROM parking_spot s JOIN users u ON s.owner_id = u.id ORDER BY s.created_at DESC")
    return render_template("index.html", spots=spots)

@spots_bp.route("/spots/new", methods=["GET", "POST"])
@require_login
def create_spot():
    csrf_token = generate_csrf_token()
    if request.method == "POST":
        verify_csrf_token(request.form.get("csrf_token"))
        data, err = validate_spot_form(request.form)
        if err:
            flash(err, "error")
            return render_template("spot_form.html", csrf_token=csrf_token, spot=None)
            
        db_execute(
            "INSERT INTO parking_spot (owner_id, title, description, lat, lon, address, tags) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (current_user_id(), data["title"], data["description"], data["lat"], data["lon"], data["address"], data["tags"])
        )
        flash("Parkkipaikka lisätty.", "success")
        return redirect(url_for("spots.index"))
        
    return render_template("spot_form.html", csrf_token=csrf_token, spot=None)

@spots_bp.route("/spots/<int:spot_id>", methods=["GET"])
def spot_detail(spot_id):
    spot = db_query_one("SELECT s.*, u.username as owner_name FROM parking_spot s JOIN users u ON s.owner_id = u.id WHERE s.id = ?", (spot_id,))
    if not spot:
        abort(404)
        
    comments = db_query_all("SELECT c.*, u.username as author_name FROM comment c JOIN users u ON c.author_id = u.id WHERE c.parking_spot_id = ? ORDER BY c.created_at DESC", (spot_id,))
    csrf_token = generate_csrf_token()
    
    # generate tile url
    tile_url = None
    try:
        tile_url = geo_helpers.tile_url(spot["lat"], spot["lon"], 15)
        
    except Exception:
        pass

    return render_template("spot_detail.html", spot=spot, comments=comments, csrf_token=csrf_token, current_user_id=current_user_id(), tile_url=tile_url)

@spots_bp.route("/spots/<int:spot_id>/edit", methods=["GET", "POST"])
@require_login
def edit_spot(spot_id):
    spot = db_query_one("SELECT * FROM parking_spot WHERE id = ?", (spot_id,))
    if not spot:
        abort(404)
    if spot["owner_id"] != current_user_id():
        abort(403, "Vain omistaja voi muokata.")
        
    csrf_token = generate_csrf_token()
    if request.method == "POST":
        verify_csrf_token(request.form.get("csrf_token"))
        data, err = validate_spot_form(request.form)
        if err:
            flash(err, "error")
            return render_template("spot_form.html", csrf_token=csrf_token, spot=spot)
            
        db_execute(
            "UPDATE parking_spot SET title=?, description=?, lat=?, lon=?, address=?, tags=? WHERE id=?",
            (data["title"], data["description"], data["lat"], data["lon"], data["address"], data["tags"], spot_id)
        )
        flash("Päivitetty.", "success")
        return redirect(url_for("spots.spot_detail", spot_id=spot_id))
        
    return render_template("spot_form.html", csrf_token=csrf_token, spot=spot)

@spots_bp.route("/spots/<int:spot_id>/delete", methods=["POST"])
@require_login
def delete_spot(spot_id):
    verify_csrf_token(request.form.get("csrf_token"))
    spot = db_query_one("SELECT * FROM parking_spot WHERE id = ?", (spot_id,))
    if not spot:
        abort(404)
    if spot["owner_id"] != current_user_id():
        abort(403)
        
    db_execute("DELETE FROM parking_spot WHERE id = ?", (spot_id,))
    flash("Parkkipaikka poistettu.", "success")
    return redirect(url_for("spots.index"))

@spots_bp.route("/spots/<int:spot_id>/comments/new", methods=["POST"])
@require_login
def create_comment(spot_id):
    verify_csrf_token(request.form.get("csrf_token"))
    err = validate_comment_form(request.form)
    if err:
        flash(err, "error")
    else:
        db_execute("INSERT INTO comment (parking_spot_id, author_id, text) VALUES (?, ?, ?)",
                   (spot_id, current_user_id(), request.form["text"]))
        flash("Kommentti lisätty.", "success")
    return redirect(url_for("spots.spot_detail", spot_id=spot_id))
