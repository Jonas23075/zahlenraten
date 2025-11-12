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
        SELECT s.id, s.player_name, s.attempts, s.created
        FROM scores s
        INNER JOIN (
            SELECT player_name, MIN(attempts) AS best_attempts
            FROM scores
            GROUP BY player_name
        ) AS best_scores
        ON s.player_name = best_scores.player_name
        AND s.attempts = best_scores.best_attempts
        ORDER BY s.attempts ASC, s.created ASC
        LIMIT 10
        """
    ).fetchall()

    return render_template("highscores.html", scores=results)
