from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from security.session_security import generate_csrf_token, verify_csrf_token
from validation.auth_validation import validate_register_form, validate_login_form
from db.connection import db_query_one, db_execute

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    csrf_token = generate_csrf_token()
    if request.method == "POST":
        verify_csrf_token(request.form.get("csrf_token"))
        err = validate_register_form(request.form)
        if err:
            flash(err, "error")
            return render_template("register.html", csrf_token=csrf_token)
        
        username = request.form["username"]
        password = request.form["password"]
        
        # Check if exists
        user = db_query_one("SELECT id FROM users WHERE username = ?", (username,))
        if user:
            flash("Käyttäjätunnus on jo varattu.", "error")
            return render_template("register.html", csrf_token=csrf_token)
            
        pass_hash = generate_password_hash(password)
        db_execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, pass_hash))
        flash("Rekisteröinti onnistui. Kirjaudu sisään.", "success")
        return redirect(url_for("auth.login"))
        
    return render_template("register.html", csrf_token=csrf_token)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    csrf_token = generate_csrf_token()
    if request.method == "POST":
        verify_csrf_token(request.form.get("csrf_token"))
        err = validate_login_form(request.form)
        
        user = db_query_one("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        if not user or not check_password_hash(user["password"], request.form.get("password")):
            flash("Väärä käyttäjätunnus tai salasana.", "error")
            return render_template("login.html", csrf_token=csrf_token)
            
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        flash("Kirjautuminen onnistui.", "success")
        return redirect(url_for("spots.index"))
        
    return render_template("login.html", csrf_token=csrf_token)

@auth_bp.route("/logout", methods=["POST"])
def logout():
    verify_csrf_token(request.form.get("csrf_token"))
    session.clear()
    flash("Olet kirjautunut ulos.", "success")
    return redirect(url_for("spots.index"))
