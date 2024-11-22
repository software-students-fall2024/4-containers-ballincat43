"""
This file contains the functions to perform some
analysis on data recieved.
"""

import re
from pymongo import MongoClient, errors

# starting some functions:


def vocab_diversity(data: str, test: bool = False) -> tuple:
    """
    This function takes in a string and calculates the frequency of
    unique words to total words as well as the most common word. (Words must be
    alphabetic). It returns a tuple of length 2, with the first item being the
    most common word in the given string and the second being the frequency. If
    the string is empty.
    """
    # split into words
    words = parse_text(data)
    di = {}
    total: int = 0
    unique: int = 0
    for w in words:
        w = w.lower()
        if not (str.isalpha(w) or str.isdigit(w)) or len(w) == 0:
            continue
        total += 1
        if w in di:
            di[w] += 1
        else:
            di[w] = 1
            unique += 1  # could also count len(keys) but for performace
    if total == 0:
        freq = 1  # if no words technically all unique
    else:
        freq: float = unique / total
    return most_common_dict(di, test=test), round(freq, 4)


def most_common_dict(word_freq: dict, every: bool = False, test: bool = False):
    """
    Calculates the key mapped to the highest value, if multiple keys
    map to the highest values, then the lowest one lexicographically
    is returned, unless the 'every' flag is set to true, in which case
    all of them are returned as a list.
    """

    coll = None # for linting
    if not test:
        try:
            client = MongoClient("mongodb://db:27017/")
            print("Connected to MongoDB successfully.")
        except errors.ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")

        db = client["transcription_db"]
        coll = db["Stats"]

    m = 0
    if every:
        ms = []
    else:
        ms = ""  # max string
    for k in sorted(word_freq.keys()):
        v = word_freq.get(k)
        if not test and coll.count_documents({"word": k}) != 0:
            old_count: int = coll.find_one({"word": k})["count"]
            coll.replace_one({"word": k}, {"word": k, "count": int(old_count + v)})
        elif not test:
            coll.insert_one({"word": k, "count": int(v)})
        if v > m:
            m = v
            if every:
                ms.append(k)
            else:
                ms = k
    if not test:
        client.close()
    return ms


def parse_text(text: str) -> list:
    """
    This function takes in a string and parses it for
    numbers and alphabetic characters.
    """
    text_list = re.split(r"[^0-9A-Za-z]", text)
    return [word for word in text_list if word != ""]
