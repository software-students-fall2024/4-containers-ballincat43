"""
This file contains the Flask app that will act as 'reciever' for
the web-app container.
"""

from flask import Flask
from pymongo import MongoClient
import os


app = Flask(__name__)
# mongo_host = os.getenv("MONGO_HOST")
# db_name = os.getenv("DB_NAME")

# mongo_client = MongoClient(mongo_host, port=27017)

# db = mongo_client[db_name]
# db.SpeechText.insert_one({
#     "text": "GOOD MORNING"
# })


@app.route("/listen", methods=["POST"])
def listen():
    """
    This function will recieve input from user's microphone.
    """


if __name__ == "__main__":
    app.run(host="127.0.0.0", port=1000)
