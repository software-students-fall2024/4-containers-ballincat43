"""
This tests the app.py file.
"""

import pytest
from app import app, User
from flask_login import FlaskLoginClient

@pytest.fixture
def appmake():
    """app fixture to test"""
    app.secret_key = "tripledoubleholymoly"  # set secret key
    app.test_client_class = FlaskLoginClient

def test_index(appmake):
    """tests index redirects"""
    with app.test_client() as client:
        assert client.get("/").status_code == 302  # since immediately redirects


def test_login(appmake):
    """test that login works"""
    with app.test_client() as client:
        assert client.get("/login").status_code == 200


def test_create_account(appmake):
    """testing create account"""
    with app.test_client() as client:
        assert client.get("/create_account").status_code == 200


def test_logout(appmake):
    """testing logout"""
    user = User("bob123")
    with app.test_client(user=user) as client:
        assert client.get("/logout").status_code == 200


def test_username(appmake):
    """Testing username"""
    user = User("bob123")
    with app.test_client(user=user) as client:
        assert client.get("/bob123").status_code == 200


def test_stats(appmake):
    """testing stats"""
    user = User("bob123")
    with app.test_client(user=user) as client:
        assert client.get("/bob123/stats").status_code == 200
