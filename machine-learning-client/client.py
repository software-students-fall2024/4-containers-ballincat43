"""
This file contains the Flask app that will act as 'reciever' for
the web-app container.
"""
from flask import Flask


app = Flask(__name__)


@app.route("/listen", methods=["POST"])
def listen():
    """
    This function will recieve input from user's microphone.
    """


if __name__ == "__main__":
    app.run(host="127.0.0.0", part=1000)