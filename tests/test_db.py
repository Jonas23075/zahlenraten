import sqlite3
import pytest

from flaskr.db import get_db, init_db


def test_get_close_db(app):
    """Test that the database connection is properly managed."""
    with app.app_context():
        db = get_db()
        assert db is get_db()  # Same connection within context

    # After context, connection should be closed
    with pytest.raises(sqlite3.ProgrammingError):
        db.execute('SELECT 1')


def test_init_db_command(runner, monkeypatch):
    """Test the init-db command."""
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Datenbank initialisiert.' in result.output
    assert Recorder.called