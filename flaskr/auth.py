import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
from flaskr.db import get_db
from flaskr.security import hash_password, verify_password, check_password_policy, needs_rehash

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        # Passwort-Policy prüfen
        ok, errs = check_password_policy(password)
        if not ok:
            for e in errs:
                flash(e, "error")
            return render_template("register.html")

        if not username:
            error = "Benutzername ist erforderlich."
        elif not password:
            error = "Passwort ist erforderlich."
        elif db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone() is not None:
            error = f"Benutzer {username} existiert bereits."

        if error is None:
            password_hash = hash_password(password)
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password_hash),
            )
            db.commit()
            user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Registrierung erfolgreich", "success")
            return redirect(url_for("game.game"))

        flash(error, "error")

    return render_template("register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        username = username.strip()
        password = password.strip()
        db = get_db()
        error = None
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user is None or not verify_password(password, user["password"]):
            error = "Falscher Benutzername oder Passwort."

        if error is None:
            # Optionales Rehash bei geänderter Methode
            if needs_rehash(user["password"]):
                new_hash = hash_password(password)
                db.execute("UPDATE users SET password = ? WHERE id = ?", (new_hash, user["id"]))
                db.commit()

            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("game.game"))

        flash(error, "error")

    return render_template("login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


@bp.route("/logout")
def logout():
    session.clear()
    flash("Auf wiedersehen", "success")
    return redirect(url_for("auth.login"))
