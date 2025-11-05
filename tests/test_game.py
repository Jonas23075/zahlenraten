import pytest
from flask import session


def test_game_get(client, app):
    """Test GET request to game page."""
    with client:
        # Simulate login
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'testuser'

        response = client.get('/game/')
        assert response.status_code == 200
        assert b'Zahlenraten' in response.data


def test_game_guess_too_low(client, app):
    """Test guessing too low."""
    with client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'testuser'
            sess['number'] = 50  # Set target number

        response = client.post('/game/', data={'guess': '30'})
        assert response.status_code == 200
        assert b'zu niedrig' in response.data


def test_game_guess_too_high(client, app):
    """Test guessing too high."""
    with client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'testuser'
            sess['number'] = 50

        response = client.post('/game/', data={'guess': '70'})
        assert response.status_code == 200
        assert b'zu hoch' in response.data


def test_game_guess_correct(client, app):
    """Test guessing correctly."""
    with client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'testuser'
            sess['number'] = 50

        response = client.post('/game/', data={'guess': '50'})
        assert response.status_code == 200
        assert b'Richtig' in response.data

        # Check if score was saved
        with app.app_context():
            from flaskr.db import get_db
            db = get_db()
            score = db.execute('SELECT * FROM scores WHERE player_name = ?', ('testuser',)).fetchone()
            assert score is not None
            assert score['attempts'] == 1


def test_game_invalid_guess(client, app):
    """Test invalid guess input."""
    with client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'testuser'

        response = client.post('/game/', data={'guess': 'abc'})
        assert response.status_code == 200
        # Should not update attempts for invalid input