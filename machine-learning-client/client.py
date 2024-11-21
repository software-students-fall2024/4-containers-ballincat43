"""
This file contains the Flask app that will act as 'reciever' for
the web-app container.
"""

from flask import Flask, request, jsonify
from pymongo import MongoClient
from functions import vocab_diversity
import speech_recognition as sprc
import os


app = Flask(__name__)
# mongo_host = os.getenv("DB_HOST")
# db_name = "Data"

# mongo_client = MongoClient(mongo_host, port=27017)



@app.route("/listen", methods=["POST"])
def listen():
    """
    This function will recieve input from user's microphone.
    """
    audio = request.form.get("afile")
    
    #text = transcribe(audio)
    rec = sprc.Recognizer()
    a = rec.record(sprc.AudioFile(audio))
    text = rec.recognize_google_cloud(a)
    
    common, freq = vocab_diversity(text)
    percent = f'{(freq*100)}%'

    return jsonify({"common": common, "freq" : percent})


if __name__ == "__main__":
    # db = mongo_client[db_name]
    # db.SpeechText.insert_one({
    #     "text": "GOOD MORNING"
    # })

    app.run(host="127.0.0.0", port=1000)
