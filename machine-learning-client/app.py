"""
This file contains the Flask app that will act as 'reciever' for
the web-app container.
"""

from flask import Flask, request, jsonify
from pymongo import MongoClient, server_api
from functions import vocab_diversity
import speech_to_text as spt
import os
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
mongo_host = os.getenv("DB_HOST")
db_name = "Data"

mongo_client = MongoClient(mongo_host, port=27017, server_api=server_api.ServerApi('1'))



@app.route("/transcribe", methods=["POST"])
def transcribe():
    """
    This function will recieve input from user's microphone.
    """
    file = open("audiofiles/temp.wav", 'rb')
    
    #text = transcribe(file)
    text = spt.get_transcription()
    #text = "apple apple apple apple"
    
    common, freq = vocab_diversity(text)
    percent = f'{(freq*100)}%'
    result = f'{common},{percent}'

    spt.store(text, common, freq)

    tfile = open("audiofiles/temp.csv", "w")
    tfile.write(result)
    tfile.write("\n")
    tfile.close()

    return ('', 200)


if __name__ == "__main__":
    db = mongo_client[db_name]
    db.SpeechText.insert_one({
        "text": "GOOD MORNING"
    })

    print(db.SpeechText.find_one({
        "text": "GOOD MORNING"
    }))

    app.run(host="0.0.0.0", port=1000)
