"""
This file contains tests for the parse_text() function.
"""
from main import parse_text


def test_none():
    """
    This will test that a string with no alnum chars
    returns an empty list.
    """
    s = "&&#*$((@&#$^#)@)(#    )"
    expect = []
    assert parse_text(s) == expect


def test_spaces():
    """
    This will test for a string only separated by spaces.
    """
    s = "coffee is the best drink ever"
    expect = ["coffee", "is", "the", "best", "drink", "ever"]
    assert parse_text(s) == expect


def test_testing():
    """
    This will test a sample audio recording.
    """
    s = "Testing, testing. 1, 2, 3. 1, 2, 3.\
        Fat Fox, Brown cat. The car is fast."
    expect = [
        "Testing",
        "testing",
        "1",
        "2",
        "3",
        "1",
        "2",
        "3",
        "Fat",
        "Fox",
        "Brown",
        "cat",
        "The",
        "car",
        "is",
        "fast",
    ]
    assert parse_text(s) == expect


def test_arbitrary():
    """
    This will test that it works with arbitrary separators.
    """
    s = "Coffee, is the. best. drink. EVER!!!"
    expect = ["Coffee", "is", "the", "best", "drink", "EVER"]
    assert parse_text(s) == expect
