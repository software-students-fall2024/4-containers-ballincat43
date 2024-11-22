import os
import assemblyai as aai
from functions import parse_text, most_common_dict, vocab_diversity
from pymongo import MongoClient
from dotenv import load_dotenv

#load environment variables from .env file
load_dotenv()

#retrieve AssemblyAI API Key from environment variables
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not ASSEMBLYAI_API_KEY:
    print("Error: ASSEMBLYAI_API_KEY not found in environment variables.")
    exit(1)

#set AssemblyAI API Key
aai.settings.api_key = ASSEMBLYAI_API_KEY
transcriber = aai.Transcriber()


def get_transcription() -> str:
    """This function will perform the audio transcription"""
    #transcription file path
    audio_file = "audiofiles/temp.wav"

    #transcription configuration
    config = aai.TranscriptionConfig()

    #transcribe 
    print("Starting transcription...")
    transcript = transcriber.transcribe(audio_file, config)
    print("Transcription completed.")

    if transcript.status == aai.TranscriptStatus.error:
        print(f"Transcription failed: {transcript.error}")
        exit(1)

    
    
    return transcript.text

#MONGODB

def store(data: str, common: str, percent: float, words: dict = None):
    """Stores the transcribed text in a mongo database"""

    #initialize MongoDB client to connect to local MongoDB instance
    try:
        client = MongoClient('mongodb://localhost:27017/')
        print("Connected to MongoDB successfully.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

    db = client['transcription_db']

    collection_stats = db['SpeechStats']
    collection_text = db['SpeechText']

    # insert word counts into 'SpeechStats' collection
    try:
        
        collection_stats.insert_one({
            "common": common,
            "freq": percent
        })
    except Exception as e:
        print(f"An error occurred while inserting word counts into MongoDB: {e}")

    # insert transcript into 'SpeechText' collection
    try:
        collection_text.insert_one({
            "textContent": data
        })
    except Exception as e:
        print(f"An error occurred while inserting transcript into MongoDB: {e}")

    client.close()
