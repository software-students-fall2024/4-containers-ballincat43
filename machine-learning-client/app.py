"""
This file contains the Flask app that will act as 'reciever' for
the web-app container.
"""

from flask import Flask
import speech_to_text as spt
from functions import vocab_diversity


app = Flask(__name__)


@app.route("/transcribe", methods=["POST"])
def transcribe():
    """
    This function will recieve input from user's microphone.
    """

    #  text = transcribe(file)
    text = spt.get_transcription()
    #  text = "apple apple apple apple"

    common, freq = vocab_diversity(text)
    percent = f'{(freq*100)}%'
    result = f'{common},{percent}'

    spt.store(text, common, freq)

    with open("audiofiles/temp.csv", 'w', encoding="utf-8") as tfile:
        tfile.write(result)
        tfile.write("\n")
        tfile.close()

    return ('', 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1000)
