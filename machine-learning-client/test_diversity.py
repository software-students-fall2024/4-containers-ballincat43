'''
This file contains tests for the vocab_diversity() function.
'''
from main import vocab_diversity

def test_unique():
    '''
    Tests that a string of unique words returns
    a frequency of 1 and the first word.
    '''
    s = "apple blue car drive eagle flame green house"
    m, f = vocab_diversity(s)
    assert f == 1
    assert m == "apple"

def test_repeat():
    '''
    Tests that a string of the same repeated word gives
    a frequency of 1/total and the correct common word.
    '''
    s = "apple apple apple apple apple"
    m, f = vocab_diversity(s)
    assert f == .2
    assert m == "apple"

def test_none():
    '''
    Tests the functions behavior with an empty string.
    '''
    s = ""
    m, f = vocab_diversity(s)
    assert f == 1
    assert m == ""

def test_reg():
    '''
    Tests the function on a more "normal" input.
    '''
    s = "That coffee is so hot that it burned the paper"
    m, f = vocab_diversity(s)
    assert f == .9
    assert m == "that"
