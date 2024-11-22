"""
Module: a flask application that acts as the interface for user login,
audio recording, and viewing statistics
"""

from flask import Flask, jsonify, render_template, request, redirect, url_for
import flask_login
from flask_login import login_user, login_required, logout_user
from pymongo import MongoClient, errors
import requests

# instantiate flask app, create key
app = Flask(__name__)
app.secret_key = "tripledoubleholymoly"

# setup flask-login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# simulated database of users, need to implement
users = {
    "bob123": {"password": "test"},
    "jen987": {"password": "foobar"},
    "adminTester": {"password": "testingtesting"},
}

MONGO_CONNECT = True
try:
    client = MongoClient("mongodb://db:27017/")
    print("Connected to MongoDB successfully.")
except errors.ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
    MONGO_CONNECT = False


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

    common = ""
    if username != "adminTester":
        if not MONGO_CONNECT:
            redirect(url_for("show_home", username=username))

        db = client["transcription_db"]
        text_coll = db["Stats"]
        all_t = text_coll.find().sort("count", -1)
        for t in all_t:
            common = t["word"]
            break

    return render_template("stats.html", username=username, word=common)


@app.route("/listen/<username>", methods=["GET", "POST"])
def listen(username):
    """
    Connect to the machine learning client to process audio.
    """

    if request.method == "POST":
        print("WENT IN TO FUNCTION")
        if "afile" not in request.files:
            return render_template(
                "user_home.html",
                username=username,
                most=str(request.files.keys()),
                percent="100%",
            )
        audio = request.files["afile"]
        audio.save("audiofiles/temp.wav")

        # audio.save("audiofiles/temp.wav")
        # file = open("audiofiles/temp.wav", 'r')
        most = ""
        percent = ""
        response = requests.post("http://machine:1000/transcribe", timeout=100000)
        # need time to process the request
        if response.status_code == 200:
            try:
                with open("audiofiles/temp.csv", "r", encoding="ascii") as tfile:
                    text = tfile.readline().split(",")
                    most = text[0]
                    percent = text[1]
                    tfile.close()
            except IOError as e:
                print("ERROR: ", e)
                most = "error"

        return jsonify({"most": most, "percent": percent})

    return render_template(
        "results.html", username=username, most=most, percent=percent
    )


@app.route("/<username>/results", methods=["GET", "POST"])
@login_required
def results(username):
    """Post results"""

    most = request.form.get("most")
    percent = request.form.get("percent")
    return render_template(
        "results.html", username=username, most=most, percent=percent
    )


@app.route("/<username>/clear", methods=["POST"])
@login_required
def clear(username):
    """Clears information from the database"""
    if username != "adminTester":
        if not MONGO_CONNECT:
            redirect(url_for("show_home", username=username))  # send back home
        database = client["transcription_db"]
        coll = database["Stats"]
        coll.delete_many({"word": {"$ne": ""}})

    return redirect(url_for("show_home", username=username))


if __name__ == "__main__":
    print("Starting")
    app.run(host="0.0.0.0", port=5000)
