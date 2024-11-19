import pytest
from main import *

def test_unique():
    s = "apple blue car drive eagle flame green house"
    m, f = vocab_diversity(s)
    assert(f == 1)
    assert(m == "apple")

def test_repeat():
    s = "apple apple apple apple apple"
    m, f = vocab_diversity(s)
    assert(f == .2)
    assert(m == "apple")

def test_none():
    s = ""
    m, f = vocab_diversity(s)
    assert(f == 1)
    assert(m == "")

def test_reg():
    s = "That coffee is so hot that it burned the paper"
    m, f = vocab_diversity(s)
    assert(f == .9)
    assert(m == "that")