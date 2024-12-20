"""
This file contains tests for the vocab_diversity() function.
"""

from functions import vocab_diversity, most_common_dict


def test_unique():
    """
    Tests that a string of unique words returns
    a frequency of 1 and the first word.
    """
    s = "apple blue car drive eagle flame green house"
    m, f = vocab_diversity(s, True)
    assert f == 1
    assert m == "apple"


def test_repeat():
    """
    Tests that a string of the same repeated word gives
    a frequency of 1/total and the correct common word.
    """
    s = "apple apple apple apple apple"
    m, f = vocab_diversity(s, True)
    assert f == 0.2
    assert m == "apple"


def test_none():
    """
    Tests the functions behavior with an empty string.
    """
    s = ""
    m, f = vocab_diversity(s, True)
    assert f == 1
    assert m == ""


def test_reg():
    """
    Tests the function on a more "normal" input.
    """
    s = "That coffee is so hot that it burned the paper"
    m, f = vocab_diversity(s, True)
    assert f == 0.9
    assert m == "that"


def test_strange():
    """Tests for when a word is not counted."""
    s = "num1"
    m, f = vocab_diversity(s, True)
    assert f == 1
    assert m == ""


def test_every():
    """Tests the every flag of most_common_dict"""
    s = {
        "apple": 2,
        "coffee": 2,
    }
    assert most_common_dict(s, every=True, test=True) == ["apple", "coffee"]
