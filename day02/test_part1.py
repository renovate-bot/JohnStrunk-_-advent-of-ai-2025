"""Unit tests for is_invalid_id from part1 (Day 2 Part 1)."""

from day02.part1 import is_invalid_id


def test_is_invalid_id_part1():
    """
    Test is_invalid_id for Day 2 Part 1 rules.

    Only numbers with even length and first half == second half are invalid.
    """
    assert is_invalid_id(1212) is True  # '12' repeated
    assert is_invalid_id(123123) is True  # '123' repeated
    assert is_invalid_id(1111) is True  # '11' repeated
    assert is_invalid_id(1234) is False  # not repeated
    assert is_invalid_id(12341234) is True  # '1234' repeated
    assert is_invalid_id(123123123) is False  # odd length
    assert is_invalid_id(111111) is True  # '111' repeated
    assert is_invalid_id(1122) is False  # not repeated
    assert is_invalid_id(11) is True  # '1' repeated
    assert is_invalid_id(22) is True  # '2' repeated
    assert is_invalid_id(99) is True  # '9' repeated
    assert is_invalid_id(1010) is True  # '10' repeated
    assert is_invalid_id(1011) is False  # not repeated
    assert is_invalid_id(1001) is False  # not repeated
    assert is_invalid_id(123456) is False  # not repeated
    assert is_invalid_id(123321) is False  # not repeated
    assert is_invalid_id(12345678) is False  # not repeated
