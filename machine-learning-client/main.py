"""
This file contains the functions to perform some
analysis on data recieved.
"""

# starting some functions:


def vocab_diversity(data: str) -> tuple:
    """
    This function takes in a string and calculates the frequency of
    unique words to total words as well as the most common word. (Words must be
    alphabetic). It returns a tuple of length 2, with the first item being the
    most common word in the given string and the second being the frequency. If
    the string is empty.
    """
    # split into words
    words = data.split()
    di = {}
    total: int = 0
    unique: int = 0
    for w in words:
        w = w.lower()
        if not str.isalpha(w):
            continue
        total += 1
        if w in di:
            di[w] += 1
        else:
            di[w] = 1
            unique += 1 # could also count len(keys) but for performace
    if total == 0:
        freq = 1 # if no words technically all unique
    else:
        freq: float =  unique / total
    return most_common_dict(di), round(freq, 2)


def most_common_dict(word_freq: dict, every: bool = False):
    """
    Calculates the key mapped to the highest value, if multiple keys
    map to the highest values, then the lowest one lexicographically
    is returned, unless the 'every' flag is set to true, in which case
    all of them are returned as a list.
    """
    m = 0
    if every:
        ms = []
    else:
        ms = "" # max string
    for k in sorted(word_freq.keys()):
        v = word_freq.get(k)
        if v > m:
            m = v
            if every:
                ms.append(k)
            else:
                ms = k
    return ms
