"""
This file contains the Flask app that will act as 'reciever' for
the web-app container.
"""
from flask import Flask, render_template, request, redirect


app = Flask(__name__)


@app.route("/listen", methods=["POST"])
def listen():
    """
    This function will recieve input from user's microphone.
    """
