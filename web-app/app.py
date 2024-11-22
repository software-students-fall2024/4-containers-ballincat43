"""
Module: a flask application that acts as the interface for user login,
audio recording, and viewing statistics
"""

from flask import Flask, render_template, request, redirect, url_for
import flask_login
from flask_login import login_user, login_required, logout_user
import requests

# instantiate flask app, create key
app = Flask(__name__)
app.secret_key = "tripledoubleholymoly"

# setup flask-login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# simulated database of users, need to implement
users = {"bob123": {"password": "test"}, "jen987": {"password": "foobar"}}


class User(flask_login.UserMixin):  # pylint: disable = too-few-public-methods
    """user class for flask-login"""

    def __init__(self, username: str) -> None:
        self.id = username


@login_manager.user_loader
def user_loader(username):
    """load a user by their username"""
    if username not in users:
        return None
    user = User(username)
    return user


@app.route("/login", methods=["GET", "POST"])
def login():
    """handles login functionality"""
    error = None
    print("HELLO")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # validate input
        if not username or not password:
            error = "Error: Missing username or password"

        elif username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user)

            return redirect(url_for("show_home", username=username))
        else:
            error = "Error: Invalid credentials"

    return render_template("login.html", error=error)


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    """handles account creation interface and functionality"""
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        # validation logic
        if username in users:
            error = "Error: Username already exists, try another!"
        elif not username or not password:
            error = "Error: Username or password left blank."
        elif password != password_confirm:
            error = "Error: Passwords do not match."
        else:
            # Add new user to "database"
            users[username] = {"password": password}
            return redirect(url_for("login"))

    return render_template("create_account.html", error=error)


@app.route("/logout", methods=["POST"])
def logout():
    """handles user logout"""
    logout_user()

    return redirect(url_for("login"))


@login_manager.unauthorized_handler
def unauthorized_handler():
    """handles situation during unauthorized access"""
    return "Unauthorized Access. Please log in.", 401


@app.route("/")
def redirect_login():
    """redirect to login page"""

    return redirect(url_for("login"))


@app.route("/<username>")
@login_required
def show_home(username):
    """show logged-in user's homepage"""

    return render_template("user_home.html", username=username)


@app.route("/<username>/stats")
@login_required
def stats(username):
    """show the user's statistics page"""

    return render_template("stats.html", username=username)


@app.route("/listen/<username>", methods=["POST"])
def listen(username):
    """
    Connect to the machine learning client to process audio.
    """
    print("WENT IN TO FUNCTION")
    if "afile" not in request.files:
        return render_template("user_home.html", username=username, most = str(request.files.keys()), percent = "100%")
    audio = request.files["afile"]
    audio.save("audiofiles/temp.wav")

    # audio.save("audiofiles/temp.wav")
    # file = open("audiofiles/temp.wav", 'r')
    most = ""
    percent = ""
    response = requests.post('http://machine:1000/transcribe')
    if(response.status_code == 200):
        try:
            tfile= open("audiofiles/temp.csv", "r")
            text = tfile.read().split(",")
            most = text[0]
            percent = text[1]
        except:
            print("ERROR")
            most = "error"
        
    return render_template("user_home.html", username=username, most = most, percent = percent)


if __name__ == "__main__":
    print("Starting")
    app.run(host="0.0.0.0", port=5000)