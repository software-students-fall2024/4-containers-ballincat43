"""This file contains the api that transcribes the collected audio"""

import os
import sys
import assemblyai as aai
from pymongo import MongoClient, errors
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# retrieve AssemblyAI API Key from environment variables
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not ASSEMBLYAI_API_KEY:
    print("Error: ASSEMBLYAI_API_KEY not found in environment variables.")
    sys.exit(1)

# set AssemblyAI API Key
aai.settings.api_key = ASSEMBLYAI_API_KEY
transcriber = aai.Transcriber()


def get_transcription() -> str:
    """This function will perform the audio transcription"""
    # transcription file path
    audio_file = "audiofiles/temp.wav"

    # transcription configuration
    config = aai.TranscriptionConfig()

    # transcribe
    print("Starting transcription...")
    transcript = transcriber.transcribe(audio_file, config)
    print("Transcription completed.")

    if transcript.status == aai.TranscriptStatus.error:
        print(f"Transcription failed: {transcript.error}")
        sys.exit(1)

    return transcript.text


# MONGODB


def store(data: str, common: str, percent: float):
    """Stores the transcribed text in a mongo database"""

    # initialize MongoDB client to connect to local MongoDB instance
    try:
        client = MongoClient("mongodb://db:27017/")
    except errors.ConnectionFailure as e:
        print("Failed to connect to MongoDB: ", e)

    db = client["transcription_db"]

    collection_stats = db["SpeechStats"]
    collection_text = db["SpeechText"]

    # insert word counts into 'SpeechStats' collection

    collection_stats.insert_one({"common": common, "freq": percent})

    # insert transcript into 'SpeechText' collection
    collection_text.insert_one({"textContent": data})

    client.close()
