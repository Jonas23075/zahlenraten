from flask import Blueprint, render_template
from flaskr.db import get_db
from flaskr.security import login_required

bp = Blueprint("scores", __name__, url_prefix="/scores")

@bp.route("/highscores")
@login_required
def highscores():
    db = get_db()
    results = db.execute(
        """
        SELECT player_name, attempts, created
        FROM scores
        ORDER BY attempts ASC, created ASC
        LIMIT 10
        """
    ).fetchall()

    return render_template("highscores.html", scores=results)
