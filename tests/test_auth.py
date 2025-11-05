import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    """Test user registration."""
    # Test successful registration
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'password': 'Testpassword123!'
    })
    assert response.status_code == 302  # Redirect after successful registration

    # Check user was added to database
    with app.app_context():
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', ('testuser',)).fetchone()
        assert user is not None


def test_register_existing_user(client, app):
    """Test registering with existing username."""
    # Create a user first
    with app.app_context():
        db = get_db()
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                   ('existinguser', 'hashedpass'))
        db.commit()

    response = client.post('/auth/register', data={
        'username': 'existinguser',
        'password': 'Newpass123!'
    })
    assert b'existiert bereits' in response.data


def test_login(client, app):
    """Test user login."""
    # Create a test user
    with app.app_context():
        from flaskr.security import hash_password
        db = get_db()
        hashed = hash_password('Testpassword123!')
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                   ('testuser', hashed))
        db.commit()

    # Test successful login
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'Testpassword123!'
    })
    assert response.status_code == 302  # Redirect to game


def test_logout(client, app):
    """Test user logout."""
    with client:
        # Simulate logged in user
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'testuser'

        response = client.get('/auth/logout')
        assert response.status_code == 302  # Redirect

        # Check session is cleared
        with client.session_transaction() as sess:
            assert 'user_id' not in sess


def test_load_logged_in_user(app):
    """Test loading logged in user."""
    with app.test_request_context():
        # No user in session
        app.preprocess_request()
        assert g.user is None

        # User in session
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            # Simulate request
            app.preprocess_request()
            # This is tricky to test directly; may need to adjust