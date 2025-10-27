import sqlite3
import click
from flask import current_app, g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    # users (optional, für Login)
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # scores
    db.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            attempts INTEGER NOT NULL,
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.execute("CREATE INDEX IF NOT EXISTS idx_scores_attempts ON scores(attempts)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_scores_created ON scores(created DESC)")
    db.commit()

@click.command("init-db")
def init_db_command():
    """Initialisiert die Datenbanktabellen."""
    init_db()
    click.echo("✅ Datenbank initialisiert.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
