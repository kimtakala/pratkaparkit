from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    abort,
)

from errors.handlers import register_error_handlers
import config
import db
import users
import items
import comments
from security.session_security import (
    require_login,
    generate_csrf_token,
    verify_csrf_token,
    current_user_id,
)
from werkzeug.security import check_password_hash
from validation.auth_validation import validate_register_form, validate_login_form
from validation.spot_validation import validate_spot_form
from validation.comment_validation import validate_comment_form
import examples.geo_helpers as geo_helpers
from markupsafe import Markup, escape
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["DATABASE"] = config.DATABASE_PATH

db.init_app(app)


@app.template_filter()
def show_lines(content):
    content = str(escape(content))
    return Markup(content.replace("\n", "<br />"))


@app.template_filter()
def helsinki_time(value):
    if value is None or value == "":
        return ""

    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    local_time = value.astimezone(ZoneInfo("Europe/Helsinki"))
    return local_time.strftime("%d.%m.%Y %H:%M")


@app.route("/", methods=["GET"])
def index():
    spots = items.get_all_spots()
    return render_template("index.html", spots=spots)


@app.route("/register", methods=["GET", "POST"])
def register():
    csrf_token = generate_csrf_token()
    if request.method == "POST":
        verify_csrf_token(request.form.get("csrf_token"))
        errors = []
        err = validate_register_form(request.form)
        if err:
            errors.append(err)

        username = request.form["username"]
        password = request.form["password"]

        user = users.get_user_by_username(username)
        if user:
            errors.append("Käyttäjätunnus on jo varattu.")

        if errors:
            return render_template(
                "register.html",
                csrf_token=csrf_token,
                errors=errors,
                form_data=request.form.to_dict(),
            )

        users.create_user(username, password)
        flash("Rekisteröinti onnistui. Kirjaudu sisään.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", csrf_token=csrf_token)


@app.route("/login", methods=["GET", "POST"])
def login():
    csrf_token = generate_csrf_token()
    if request.method == "POST":
        verify_csrf_token(request.form.get("csrf_token"))
        errors = []
        err = validate_login_form(request.form)
        if err:
            errors.append(err)

        user = users.get_user_by_username(request.form.get("username"))
        if not user or not check_password_hash(
            user["password"], request.form.get("password")
        ):
            errors.append("Väärä käyttäjätunnus tai salasana.")

        if errors:
            return render_template(
                "login.html",
                csrf_token=csrf_token,
                errors=errors,
                form_data=request.form.to_dict(),
            )

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        flash("Kirjautuminen onnistui.", "success")
        return redirect(url_for("index"))

    return render_template("login.html", csrf_token=csrf_token)


@app.route("/logout", methods=["POST"])
def logout():
    verify_csrf_token(request.form.get("csrf_token"))
    session.clear()
    flash("Olet kirjautunut ulos.", "success")
    return redirect(url_for("index"))


@app.route("/spots/new", methods=["GET", "POST"])
@require_login
def create_spot():
    csrf_token = generate_csrf_token()
    if request.method == "POST":
        verify_csrf_token(request.form.get("csrf_token"))
        data, err = validate_spot_form(request.form)
        if err:
            flash(err, "error")
            return render_template("spot_form.html", csrf_token=csrf_token, spot=None)

        items.create_spot(
            current_user_id(),
            data["title"],
            data["description"],
            data["lat"],
            data["lon"],
            data["address"],
            data["tags"],
        )
        flash("Parkkipaikka lisätty.", "success")
        return redirect(url_for("index"))

    return render_template("spot_form.html", csrf_token=csrf_token, spot=None)


@app.route("/spots/<int:spot_id>", methods=["GET"])
def spot_detail(spot_id):
    spot = items.get_spot(spot_id)
    if not spot:
        abort(404)

    comments_list = comments.get_comments_for_spot(spot_id)
    csrf_token = generate_csrf_token()

    tile_url = None
    try:
        tile_url = geo_helpers.tile_url(spot["lat"], spot["lon"], 15)
    except Exception:
        pass

    return render_template(
        "spot_detail.html",
        spot=spot,
        comments=comments_list,
        csrf_token=csrf_token,
        current_user_id=current_user_id(),
        tile_url=tile_url,
    )


@app.route("/spots/<int:spot_id>/edit", methods=["GET", "POST"])
@require_login
def edit_spot(spot_id):
    spot = items.get_spot(spot_id)
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

        items.update_spot(
            spot_id,
            data["title"],
            data["description"],
            data["lat"],
            data["lon"],
            data["address"],
            data["tags"],
        )
        flash("Päivitetty.", "success")
        return redirect(url_for("spot_detail", spot_id=spot_id))

    return render_template("spot_form.html", csrf_token=csrf_token, spot=spot)


@app.route("/spots/<int:spot_id>/delete", methods=["POST"])
@require_login
def delete_spot(spot_id):
    verify_csrf_token(request.form.get("csrf_token"))
    spot = items.get_spot(spot_id)
    if not spot:
        abort(404)
    if spot["owner_id"] != current_user_id():
        abort(403)

    items.delete_spot(spot_id)
    flash("Parkkipaikka poistettu.", "success")
    return redirect(url_for("index"))


@app.route("/spots/<int:spot_id>/comments/new", methods=["POST"])
@require_login
def create_comment(spot_id):
    verify_csrf_token(request.form.get("csrf_token"))
    err = validate_comment_form(request.form)
    if err:
        flash(err, "error")
    else:
        comments.add_comment(spot_id, current_user_id(), request.form["text"])
        flash("Kommentti lisätty.", "success")
    return redirect(url_for("spot_detail", spot_id=spot_id))


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip()
    min_lat = request.args.get("min_lat", "").strip()
    max_lat = request.args.get("max_lat", "").strip()
    min_lon = request.args.get("min_lon", "").strip()
    max_lon = request.args.get("max_lon", "").strip()
    bbox_error = None

    sql = """
        SELECT
            s.id,
            s.owner_id,
            s.title,
            s.description,
            s.lat,
            s.lon,
            s.address,
            s.tags,
            s.created_at,
            u.username AS owner_name
        FROM parking_spot s
        JOIN users u ON s.owner_id = u.id
        WHERE 1=1
    """
    params = []

    if query:
        sql += " AND (s.title LIKE ? OR s.description LIKE ? OR s.address LIKE ? OR s.tags LIKE ?)"
        like_q = f"%{query}%"
        params.extend([like_q, like_q, like_q, like_q])

    bbox_values = [min_lat, max_lat, min_lon, max_lon]
    if any(bbox_values) and not all(bbox_values):
        bbox_error = "Täytä kaikki koordinaattikentät tai jätä ne kaikki tyhjiksi."
    elif all(bbox_values):
        try:
            min_lat_f = float(min_lat)
            max_lat_f = float(max_lat)
            min_lon_f = float(min_lon)
            max_lon_f = float(max_lon)
            if min_lat_f > max_lat_f or min_lon_f > max_lon_f:
                bbox_error = (
                    "Min-arvon pitää olla pienempi tai yhtä suuri kuin max-arvon."
                )
            else:
                sql += " AND s.lat BETWEEN ? AND ? AND s.lon BETWEEN ? AND ?"
                params.extend([min_lat_f, max_lat_f, min_lon_f, max_lon_f])
        except ValueError:
            bbox_error = "Koordinaattien pitää olla numeroita."

    sql += " ORDER BY s.created_at DESC"
    spots = db.query_all(sql, params)

    return render_template(
        "search.html",
        spots=spots,
        query=query,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        bbox_error=bbox_error,
    )


@app.route("/users/<int:user_id>", methods=["GET"])
def user_profile(user_id):
    user = users.get_user_stats(user_id)
    if not user:
        abort(404)
    user_items = users.get_user_items(user_id)
    return render_template(
        "user_profile.html",
        user=user,
        items=user_items,
        current_user_id=current_user_id(),
    )


register_error_handlers(app)


if __name__ == "__main__":
    app.run(debug=True)
