"""
This tests the app.py file.
"""

from flask_login import FlaskLoginClient
from app import app, User


app.secret_key = "tripledoubleholymoly"
app.test_client_class = FlaskLoginClient
app.config["Testing"] = True


def test_index():
    """tests index redirects"""
    with app.test_client() as client:
        assert client.get("/").status_code == 302  # since immediately redirects


def test_login():
    """test that login works"""
    with app.test_client() as client:
        assert client.get("/login").status_code == 200


def test_create_account():
    """testing create account"""
    with app.test_client() as client:
        assert client.get("/create_account").status_code == 200


def test_logout():
    """testing logout"""
    user = User("bob123")
    with app.test_client(user=user) as client:
        assert client.get("/logout").status_code == 200


def test_username():
    """Testing username"""
    user = User("bob123")
    with app.test_client(user=user) as client:
        assert client.get("/bob123").status_code == 200


def test_stats():
    """testing stats"""
    user = User("bob123")
    with app.test_client(user=user) as client:
        assert client.get('/bob123/stats').status_code == 200
