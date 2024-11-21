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

#transcription file path
audio_file = "/Users/bohanhou/Desktop/test.m4a"

#transcription configuration
config = aai.TranscriptionConfig()

#transcribe 
print("Starting transcription...")
transcript = transcriber.transcribe(audio_file, config)
print("Transcription completed.")

if transcript.status == aai.TranscriptStatus.error:
    print(f"Transcription failed: {transcript.error}")
    exit(1)

#output paths
output_folder = "/Users/bohanhou/Desktop/SWE_P4"
transcript_file = os.path.join(output_folder, "transcript.txt")
word_count_file = os.path.join(output_folder, "count.txt")

os.makedirs(output_folder, exist_ok=True)

#write to file
with open(transcript_file, 'w') as f:
    f.write(transcript.text + '\n')

#perform functions
most_common_word, diversity, word_freqs = vocab_diversity(transcript.text)

#sort word frequencies in descending order
sorted_word_counts = dict(sorted(word_freqs.items(), key=lambda item: item[1], reverse=True))

#write word counts to file
with open(word_count_file, 'w') as f:
    for word, count in sorted_word_counts.items():
        f.write(f"{word}: {count}\n")

#print results
print(f"Most common word: {most_common_word}")
print(f"Vocabulary diversity: {diversity}")
for word, count in sorted_word_counts.items():
    print(f"{word}: {count}")

#MONGODB

#initialize MongoDB client to connect to local MongoDB instance
try:
    client = MongoClient('mongodb://localhost:27017/')
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    exit(1)

db = client['transcription_db']

collection_stats = db['SpeechStats']
collection_text = db['SpeechText']

word_documents = [
    {"word": word, "count": count}
    for word, count in sorted_word_counts.items()
]

transcript_document = {
    "transcript": transcript.text
}

#insert word counts into 'SpeechStats' collection
try:
    print("Inserting word counts into MongoDB...")
    result = collection_stats.insert_many(word_documents)
    print(f"Inserted {len(result.inserted_ids)} word count documents into 'SpeechStats'.")
except Exception as e:
    print(f"An error occurred while inserting word counts into MongoDB: {e}")

#insert transcript into 'SpeechText' collection
try:
    print("Inserting transcript into MongoDB...")
    result = collection_text.insert_one(transcript_document)
    print(f"Inserted transcript document with ID: {result.inserted_id} into 'SpeechText'.")
except Exception as e:
    print(f"An error occurred while inserting transcript into MongoDB: {e}")

client.close()