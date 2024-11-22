"""
This tests the app.py file.
"""

from flask_login import FlaskLoginClient
from app import app, User


app.secret_key = "tripledoubleholymoly"
app.test_client_class = FlaskLoginClient


def test_index():
    """tests index redirects"""
    with app.test_client() as client:
        assert client.get("/").status_code == 302  # since immediately redirects


def test_login():
    """test that login works"""
    with app.test_client() as client:
        assert client.get("/login").status_code == 200
        assert client.post("/login", data={
            "username": "bob123",
            "password": "test",
        }).status_code == 302  # if user exits, should redirect to homepage
        assert client.post("/login", data={
            "username": "penguin",
            "password": "antarctica",
        }).status_code == 200
        # if user doesn't exist, will render template with success instead of 302
        assert client.post("/login", data={
            "username": "bob123",
            "password": None,
        }).status_code == 200
        assert client.post("/login", data={
            "username": None,
            "password": "test",
        }).status_code == 200


def test_create_account():
    """testing create account"""
    with app.test_client() as client:
        assert client.get("/create_account").status_code == 200
        assert client.post("/create_account", data={
            "username": "nyc",
            "password": "ny",
            "password_confirm": "ny",
        }).status_code == 302  # if successful should redirect to login
        assert client.post("/create_account", data={
            "username": "nyc",
            "password": "ny",
            "password_confirm": "pa",
        }).status_code == 200  # will render template instead
        assert client.post("/create_account", data={
            "username": "bob123",
            "password": "ny",
            "password_confirm": "ny",
        }).status_code == 200  # will render template instead
        assert client.post("/create_account", data={
            "username": None,
            "password": None,
            "password_confirm": "ny",
        }).status_code == 200  # will render template instead

def test_logout():
    """testing logout"""
    user = User("bob123")
    with app.test_client(user=user) as client:
        assert client.get("/logout").status_code == 200
        assert client.post("/logout").status_code == 302


def test_username():
    """Testing username"""
    user = User("bob123")
    with app.test_client(user=user) as client:
        assert client.get("/bob123").status_code == 200
    with app.test_client() as client:
        assert client.get("/bob123").status_code == 401


def test_stats():
    """testing stats"""
    user = User("adminTester")
    with app.test_client(user=user) as client:
        assert client.get("/adminTester/stats").status_code == 200


def test_results():
    """testing results"""
    user = User("adminTester")
    with app.test_client(user=user) as client:
        assert client.post("/adminTester/results", data={
            "most": "apple",
            "percent": "100%",
        }).status_code == 200  # will render template instead

def test_listen():
    """testing listen"""
    user = User("adminTester")
    with app.test_client(user=user) as client:
        assert client.get("/listen/adminTester").status_code == 500  # should not work
        assert client.post("/listen/adminTester").status_code == 200


def test_clear():
    """testing clear"""
    user = User("adminTester")
    with app.test_client(user=user) as client:
        assert client.post("/adminTester/clear").status_code == 302
