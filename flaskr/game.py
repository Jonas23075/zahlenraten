from flask import Blueprint, render_template, request, session, flash
from random import randint
from .security import login_required

bp = Blueprint("game", __name__, url_prefix="/game")


@bp.route("/", methods=("GET", "POST"))
@login_required
def game():
    # Stelle sicher, dass alles existiert
    if "number" not in session:
        session["number"] = randint(1, 100)

    if "attempts" not in session:
        session["attempts"] = 0

    if "guesses" not in session:
        session["guesses"] = []# Liste der bisherigen Tipps (Zahl, Status)

    message = None

    if request.method == "POST":
        guess = request.form.get("guess")
        if guess and guess.isdigit():
            guess = int(guess)
            session["attempts"] += 1

            if guess < session["number"]:
                message = "Deine Zahl ist zu niedrig!"
                session["guesses"].append((guess, "low"))
            elif guess > session["number"]:
                message = "Deine Zahl ist zu hoch!"
                session["guesses"].append((guess, "high"))
            else:
                message = f"Richtig! Die Zahl war {session['number']}. Versuche: {session['attempts']}"
                flash(message, "success")
                           # ✅ Score speichern
                from flaskr.db import get_db
                db = get_db()
                db.execute(
                   "INSERT INTO scores (player_name, attempts) VALUES (?, ?)",
                   (session.get("username"), session["attempts"])
                )
                db.commit()
                           # Reset
                session.pop("number", None)
                session.pop("attempts", None)
                session.pop("guesses", None)
                return render_template("game.html", message=message, guesses=[], attempts=0)

    return render_template("game.html", message=message, guesses=session["guesses"], attempts=session["attempts"])
