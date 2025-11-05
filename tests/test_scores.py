def test_highscores(client, app):
    """Test the highscores page."""
    with client:
        # Simulate login
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'testuser'

        # Insert some test scores
        with app.app_context():
            from flaskr.db import get_db
            db = get_db()
            db.execute("INSERT INTO scores (player_name, attempts) VALUES (?, ?)", ('alice', 5))
            db.execute("INSERT INTO scores (player_name, attempts) VALUES (?, ?)", ('bob', 3))
            db.execute("INSERT INTO scores (player_name, attempts) VALUES (?, ?)", ('charlie', 7))
            db.commit()

        response = client.get('/scores/highscores')
        assert response.status_code == 200
        assert b'alice' in response.data
        assert b'bob' in response.data
        assert b'charlie' in response.data

        # Check ordering: bob (3 attempts) should come before alice (5)
        data = response.data.decode()
        bob_index = data.find('bob')
        alice_index = data.find('alice')
        assert bob_index < alice_index